---
title: "Migrating from Hive Metastore and the alternatives"
summary: "The painful reality of Hive-to-UC migration, and an honest comparison with AWS Glue Data Catalog, Apache Polaris, and Snowflake's built-in governance."
weight: 4
type: lecture
tags:
  - unity-catalog
  - hive-metastore
  - migration
  - aws-glue
  - apache-polaris
  - snowflake
  - governance
sources:
  - https://docs.databricks.com/aws/en/data-governance/unity-catalog/migrate
  - https://www.databricks.com/blog/enterprise-scale-governance-migrating-hive-metastore-unity-catalog
  - https://medium.com/slalom-blog/tips-and-tricks-for-migrating-from-hive-metastore-to-unity-catalog-d0a18944ac2b
  - https://estuary.dev/blog/iceberg-catalog-apache-polaris-vs-unity-catalog/
  - https://www.databricks.com/blog/open-sourcing-unity-catalog
  - https://docs.unitycatalog.io/
last_refreshed: "2026-04-08"
---

## The question

Your wind utility already has Databricks. You have been using the legacy Hive Metastore for two years. Tables are registered, pipelines are running, analysts know where to find data. Now Databricks says you need to migrate to Unity Catalog for governance, lineage, and compliance.

How painful is this migration? What breaks? And while you are at it — is Unity Catalog actually the best option, or should you be looking at AWS Glue, Apache Polaris, or Snowflake?

## The Hive Metastore to Unity Catalog migration

<div class="definition">
<strong>Hive Metastore (HMS)</strong>
The legacy metadata service in Databricks, inherited from the Apache Hive project. Each Databricks workspace had its own HMS instance, storing table definitions, schemas, and basic permissions. It uses a single-level namespace (database.table) and workspace-scoped permissions. Still functional but no longer receives new features — Unity Catalog is the replacement.[^1]
</div>

### What changes architecturally

The migration from HMS to Unity Catalog is not a simple table copy. It is a governance model change:

| Aspect | Hive Metastore | Unity Catalog |
|---|---|---|
| Scope | Per-workspace | Per-account (shared across workspaces) |
| Namespace | `database.table` (two levels) | `catalog.schema.table` (three levels) |
| Permissions | Workspace-local groups | Account-level groups (Entra ID, Okta, etc.) |
| Lineage | None | Automatic, column-level |
| Audit | None built-in | `system.access.audit` |
| Column/row security | Views only | Native column masks, row filters |
| Storage | Mount points, DBFS | External locations, managed storage |

### The three categories of pain

Based on what enterprises report during migration, the pain falls into three buckets:[^2]

**1. Mount points and DBFS paths.** Legacy Databricks setups typically use `dbfs:/mnt/datalake/scada/` to reference data. Unity Catalog does not use mount points — it uses external locations registered at the metastore level. Every pipeline that references `dbfs:/mnt/` needs to be rewritten to use `s3://` or `abfss://` paths, or to reference UC-managed tables by their three-part name. For a wind utility with 50 notebooks and 20 jobs, this is tedious but mechanical.

**2. Permission model differences.** HMS permissions were workspace-scoped. A group `analysts` in workspace A is different from `analysts` in workspace B. Unity Catalog uses account-level groups — typically federated from your identity provider (Entra ID, Okta). The migration requires mapping workspace-local groups to account-level groups, which means coordinating with your identity team. For a 200-person organization, this is a project in itself.[^3]

**3. Table history loss.** When you upgrade a Hive table to Unity Catalog using `CREATE TABLE ... CLONE`, the Delta transaction history does not migrate. Time travel queries against pre-migration versions fail. For compliance use cases — "show me what this table looked like on January 15" — this is a real loss. The workaround is to keep the original table accessible during a transition period, but that means maintaining two governance models temporarily.[^1]

### The UPGRADE command

Databricks provides the `UPGRADE` command to migrate tables in place:

```sql
-- Upgrade a single table from the legacy hive_metastore
-- to a Unity Catalog schema
CREATE TABLE wind_prod.scada.turbine_readings
  CLONE hive_metastore.sensors.turbine_readings;
```

For external tables (data stays in place, only metadata moves):

```sql
-- Sync the Hive external table to UC without copying data
SYNC TABLE wind_prod.scada.turbine_readings
  FROM hive_metastore.sensors.turbine_readings;
```

The `SYNC TABLE` approach is less disruptive for external tables because it does not copy data — it registers the existing storage location in Unity Catalog. But it requires that the storage location is registered as an external location in UC first, which means setting up storage credentials and external location objects.[^1]

### Migration strategy: do not big-bang it

The practical advice from organizations that have done this migration:[^2]

1. **Run HMS and UC in parallel.** Unity Catalog can coexist with the legacy Hive Metastore. Tables in `hive_metastore.*` remain accessible while you migrate.
2. **Migrate by pipeline, not by table.** Migrate an entire pipeline (Bronze through Gold) at once, so lineage is continuous within UC.
3. **Start with new tables in UC.** Any new table should be created in Unity Catalog from day one. This prevents the migration backlog from growing.
4. **Budget for permission redesign.** This is the part that takes longer than expected. You are not just copying permissions — you are redesigning them for a three-level hierarchy with account-level groups.
5. **Test downstream consumers.** BI dashboards, ML pipelines, and scheduled jobs all reference tables by name. Changing from `hive_metastore.sensors.readings` to `wind_prod.scada.turbine_readings` breaks every downstream reference.

### What if migration goes wrong?

The good news: HMS and UC coexist during migration. You do not flip a switch — you migrate table by table. If a migrated table has issues:

1. **For CLONE migrations** — The original HMS table is untouched. Drop the UC clone (`DROP TABLE wind_prod.scada.turbine_readings`) and you are back to the HMS version. The trade-off: the clone has no transaction history from before the clone operation, so any time travel queries against pre-clone versions will not work on the UC copy.
2. **For SYNC (external tables)** — The external location is now registered in UC, but the underlying data has not moved. To revert, remove the UC table registration. The data files remain at their original S3/ABFSS location, and the HMS external table definition still points to them.
3. **For UPGRADE (in-place)** — This is the least reversible option. The table is now owned by UC. To revert, you would need to re-register the table in HMS manually (`CREATE TABLE hive_metastore.sensors.turbine_readings USING DELTA LOCATION 's3://wind-lake/scada/turbine_readings/'`). Delta transaction history is preserved in the `_delta_log/`, so the data itself is safe — the risk is in the metadata layer, not the data layer.

Recommended approach: migrate non-critical tables first (dev and sandbox schemas). Run both HMS and UC paths in parallel for a week. Validate that queries return identical results by comparing row counts and checksums on key columns. Then migrate production tables. Keep the HMS registrations alive during a validation window — you can always drop them after the team confirms UC is working correctly.[^1]

### How long does migration take?

For the wind utility (estimated ~50 tables across Bronze/Silver/Gold, 15 analysts, 3 data engineers):

- **Catalog and schema creation:** 1 day. This is mechanical — create the `wind_prod` catalog, create `scada`, `fleet_analytics`, and `governance` schemas, set up storage credentials and external locations. Well-documented in Databricks migration guides.[^2]
- **Table migration:** 1-2 weeks. CLONE or SYNC each table, verify row counts and schema match. The actual commands are fast — a SYNC of an external table is near-instant because no data moves. The time is in testing each table after migration.
- **Permission recreation:** 1 week. Map HMS workspace-local groups to UC account-level groups. Write GRANT statements for each group-schema combination. Test with each analyst role to confirm they can access what they should and cannot access what they should not. This step often surfaces permission inconsistencies that existed in HMS but were never noticed.
- **Notebook and job path updates:** 1-2 weeks. Find-and-replace `hive_metastore.` with `wind_prod.` in every notebook, job, and dashboard. This is the longest tail — you will find references in unexpected places (hardcoded in ML feature pipelines, embedded in BI tool connection strings, cached in analyst notebooks that have not been run in months).
- **Parallel validation:** 1 week. Run old and new paths simultaneously, compare results. This is the step that catches edge cases — a notebook that uses `spark.sql("USE hive_metastore.sensors")` implicitly, a job that references a table by two-part name without the catalog prefix.

Total: 4-6 weeks with a dedicated data engineer. The pain is proportional to the number of notebooks, dashboards, and jobs that reference HMS paths, not the number of tables. An organization with 50 tables but 200 notebooks will take longer than one with 100 tables but 30 notebooks.[^3]

## Honest comparison: Unity Catalog vs. the alternatives

Unity Catalog is not the only data governance option. Here is an honest assessment of the alternatives, including where they are genuinely better.

### UC vs. AWS Glue Data Catalog

<div class="definition">
<strong>AWS Glue Data Catalog</strong>
Amazon's managed metadata service that acts as a central repository for table definitions, schemas, and partition information. It is compatible with the Apache Hive Metastore API, which means tools that speak to Hive (including Spark, Presto, and Athena) can use Glue as their catalog.[^4]
</div>

| Dimension | Unity Catalog | AWS Glue Data Catalog |
|---|---|---|
| Cloud support | AWS, Azure, GCP | AWS only |
| Access control | Table, column, row level | Table level (via Lake Formation) |
| Lineage | Automatic, column-level | Requires AWS Lake Formation + manual setup |
| Audit | Built-in system tables | CloudTrail (storage-level, not semantic) |
| Compute coupling | Databricks (+ Iceberg REST API clients) | Any AWS compute (Athena, EMR, Redshift Spectrum) |
| Open source | Yes (Apache 2.0) | No |

**When Glue is better:** If your wind utility is all-in on AWS and uses Athena, EMR, and Redshift Spectrum, Glue is the natural catalog — it integrates natively with every AWS analytics service. Adding Unity Catalog means adding Databricks as a dependency.

**When UC is better:** If you need cross-cloud governance (the wind utility has Azure in the corporate office and AWS for the SCADA platform), column/row-level security, or automatic lineage, Glue cannot match UC's capabilities without bolting on Lake Formation and additional tooling.

### UC vs. Apache Polaris (Snowflake's open catalog)

<div class="definition">
<strong>Apache Polaris</strong>
An open-source catalog for Apache Iceberg tables, originally developed by Snowflake and contributed to the Apache Software Foundation. It implements the Iceberg REST Catalog API and focuses on multi-engine interoperability for Iceberg-native workloads. Snowflake also offers a managed version called Snowflake Open Catalog.[^5]
</div>

| Dimension | Unity Catalog | Apache Polaris |
|---|---|---|
| Table format | Delta Lake + Iceberg (via UniForm and native Iceberg) | Iceberg only |
| Access control | Full RBAC with column/row security | Basic RBAC (via Iceberg REST API permissions) |
| Lineage | Automatic, column-level | Not included (external tooling needed) |
| Audit | Built-in system tables | Not included |
| Open source | Yes (Apache 2.0, LF AI & Data) | Yes (Apache 2.0, ASF) |
| Maturity | Production since 2021, OSS since 2024 | Incubating, earlier stage |

**The philosophical difference:** Polaris is a *catalog* — it stores table metadata and handles access to Iceberg tables. Unity Catalog is a *governance platform* — it adds lineage, audit, column masking, row filtering, governed tags, and AI asset management on top of the catalog function.

**When Polaris is better:** If your organization has standardized on Iceberg (not Delta Lake), uses multiple engines (Trino, Flink, Spark, Snowflake), and wants the thinnest possible catalog layer without vendor coupling, Polaris is a more focused tool. It does one thing and does it openly.

**When UC is better:** If you need the governance capabilities (lineage, audit, fine-grained security) and are using Databricks for any workload, UC provides a more complete solution. The gap is closing for Iceberg support — as of 2025, UC supports Iceberg managed tables and the Iceberg REST Catalog API, meaning external engines like Trino and Snowflake can read from UC-governed tables.[^6]

### UC vs. Snowflake's built-in governance

This is the comparison that comes up in every customer conversation.

| Dimension | Unity Catalog | Snowflake Governance |
|---|---|---|
| Access control | GRANT/REVOKE + column masks + row filters | GRANT/REVOKE + column masking + row access policies |
| Lineage | Automatic, column-level | Access History + Object Dependencies (similar scope) |
| Audit | system.access.audit | ACCOUNT_USAGE.ACCESS_HISTORY |
| Data sharing | Delta Sharing (open protocol) | Snowflake Marketplace + direct sharing (Snowflake-to-Snowflake) |
| Compute + governance coupling | Separate (UC governs, DBSQL/Spark computes) | Integrated (governance is part of the Snowflake platform) |
| Multi-engine support | Any Iceberg REST API client | Snowflake only (for governed access) |
| Open source | Yes | No |

**When Snowflake is genuinely better:** Snowflake's governance is simpler to set up and operate because it is integrated into a single platform. There is no "migration to UC" step — governance is on by default. For a SQL-heavy analytics workload with no ML or streaming requirements, Snowflake's governance is mature, well-documented, and requires less operational overhead.

**When UC is better:** When you need to govern data across multiple engines (Spark for ETL, DBSQL for analytics, MLflow for ML), across multiple clouds, or when you want to share data outside your platform using an open protocol. Delta Sharing lets your wind utility share anonymized fleet performance data with a turbine manufacturer who uses Snowflake, Trino, or pandas — without requiring them to have a Databricks account.

**The honest take for the wind utility:** If the utility only needs SQL analytics and their data fits in Snowflake, Snowflake's governance is simpler and arguably better for that use case. But the utility also has streaming SCADA pipelines (Spark), a vibration prediction model (MLflow), and DLT pipelines for data quality — and they need to govern all of it, not just the SQL layer. That is where UC's broader scope matters.

## When Unity Catalog is overkill

Not every organization needs Unity Catalog. It adds complexity that is only justified when you have:

- **Compliance requirements** (NERC CIP, SOC 2, HIPAA, GDPR) that demand auditable access control and lineage
- **Multiple teams** that need different levels of data access
- **Multiple workspaces** or cloud environments that need shared governance
- **Data sharing requirements** across organizational boundaries

If you are a 3-person data team, single cloud, no compliance mandate, and your data fits in a single workspace — the overhead of Unity Catalog's permission model, storage credentials, and external locations may not be worth it. A well-organized Hive Metastore with workspace-level access controls might be sufficient.

This is an important thing to say in customer conversations. Recommending Unity Catalog to a 5-person startup with no regulatory requirements is over-engineering. Recommending it to a 500-turbine wind utility under NERC CIP is table stakes.

## The open source angle

Unity Catalog was open-sourced in June 2024 under the Apache 2.0 license and donated to the Linux Foundation's LF AI & Data.[^7] The open-source version includes:

- The three-level namespace and metadata management
- Table, volume, function, and model registration
- Compatibility with the Hive Metastore API and Iceberg REST Catalog API
- Multi-format support (Delta, Iceberg via UniForm, Parquet, CSV)

What the open-source version does *not* include (as of early 2026): the full governance features (column masks, row filters, system tables for audit) that require the Databricks-managed version. This is the typical open-core model — the catalog is open, the enterprise governance is proprietary.

For the wind utility, the practical implication: you can evaluate Unity Catalog's namespace model and API without a Databricks contract. But the governance features that answer the NERC auditor's questions require the managed service.

[^1]: [Upgrade Hive tables and views to Unity Catalog](https://docs.databricks.com/aws/en/data-governance/unity-catalog/migrate) — Official migration documentation.
[^2]: [Enterprise-Scale Governance: Migrating from Hive Metastore to Unity Catalog](https://www.databricks.com/blog/enterprise-scale-governance-migrating-hive-metastore-unity-catalog) — Databricks blog on migration patterns.
[^3]: [Tips and tricks for migrating from Hive metastore to Unity Catalog](https://medium.com/slalom-blog/tips-and-tricks-for-migrating-from-hive-metastore-to-unity-catalog-d0a18944ac2b) — Slalom consulting blog on real-world migration experience.
[^4]: [AWS Glue Data Catalog](https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html) — AWS documentation.
[^5]: [Iceberg Catalog Showdown: Apache Polaris vs Unity Catalog](https://estuary.dev/blog/iceberg-catalog-apache-polaris-vs-unity-catalog/) — Estuary blog comparing the two catalogs.
[^6]: [What's new with Databricks Unity Catalog at Data + AI Summit 2025](https://www.databricks.com/blog/whats-new-databricks-unity-catalog-data-ai-summit-2025) — Iceberg managed tables and REST Catalog API support.
[^7]: [Open sourcing Unity Catalog](https://www.databricks.com/blog/open-sourcing-unity-catalog) — Databricks announcement of the OSS release.
