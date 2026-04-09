---
title: "Knowledge Test: Unity Catalog"
summary: "Validate your understanding of the three-level namespace, access control, lineage, audit, and how Unity Catalog compares to the alternatives."
weight: 99
type: test
tags:
  - unity-catalog
  - governance
  - access-control
  - lineage
  - audit
---

## Oral questions

**Must know cold:**

1. Explain the three-level Unity Catalog namespace. What is a metastore, a catalog, and a schema? Give a concrete example of how the wind utility would structure theirs — include at least two catalogs and three schemas.

2. What is the difference between Unity Catalog and the legacy Hive Metastore? Name three specific capabilities UC provides that HMS does not.

3. A NERC CIP auditor asks: "Who has accessed CEII data in the last 90 days?" Walk through exactly how you would answer this using Unity Catalog. Which system table do you query? What columns matter?

4. Explain column masking with a concrete example. Your `turbine_readings` table has `latitude` and `longitude` columns that are CEII. How do you make them visible to CEII-cleared engineers and invisible to everyone else — without creating separate views?

5. What is data lineage in Unity Catalog? Give a scenario where it prevents a production incident. (Hint: schema change on a Bronze table.)

6. What is the difference between a managed table and an external table? When would a regulated wind utility prefer external tables for Bronze data, and why?

**Know the shape:**

7. What are system tables in Unity Catalog? Name two specific tables and what you would query each one for. (Two sentences each.)

8. A customer is migrating from Hive Metastore to Unity Catalog. Name the single biggest category of pain they will hit and explain why it is harder than it sounds. (Pick one: mount points, permissions, or table history loss.)

9. What is Delta Sharing and how does it relate to Unity Catalog? Give one example of cross-organization data sharing for the wind utility.

## Code challenge

Complete `modules/05-unity-catalog/exercises/05_unity_catalog.sql` in a Databricks SQL editor.

You should be able to:

- [ ] Create a catalog and schema successfully
- [ ] Create a managed Gold table and insert sample data
- [ ] Show that the table has no grants initially, then add and verify a GRANT
- [ ] Add column comments and table tags for discoverability
- [ ] Run a query and find the lineage in Catalog Explorer (Lineage tab)
- [ ] Query `system.access.audit` and find at least one entry for your own session

## The interview question

Practice until fluent:

> "A wind utility says they cannot adopt Databricks because NERC requires them to prove who has access to CEII. How do you respond?"

A strong answer covers: Unity Catalog provides table-level, column-level, and row-level access control. CEII columns (like turbine GPS coordinates) can be masked using column masking functions so non-cleared analysts see NULL while cleared engineers see the actual values. Every data access is logged in `system.access.audit` — the utility can query "who accessed this table in the last 90 days" with a SQL statement. Data lineage traces compliance reports back to source data automatically. All of this is queryable and auditable, not a manual spreadsheet.

Flag the migration caveat: if the utility already has Databricks with Hive Metastore, there is a non-trivial migration to Unity Catalog. Set expectations on timeline and plan for parallel operation during the transition.

## Bonus: the "why not Snowflake?" answer

If the interviewer follows up with "Snowflake has governance too — why Unity Catalog?":

- Acknowledge that Snowflake's governance is mature and simpler for SQL-only workloads
- The difference is scope: UC governs Spark pipelines, ML models (MLflow), streaming, and SQL — not just the SQL analytics layer
- Delta Sharing is an open protocol; Snowflake's sharing is Snowflake-to-Snowflake (or requires Snowflake Open Catalog / Polaris for external access)
- UC is open source (Apache 2.0); Snowflake's governance is proprietary
- Be honest: if the customer only needs SQL analytics, Snowflake's governance is arguably simpler to operate
