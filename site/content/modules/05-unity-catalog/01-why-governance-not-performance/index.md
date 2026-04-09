---
title: "Why governance — not performance — sells Databricks"
summary: "NERC auditors ask three questions your data lake can't answer. That gap — not Spark speed — is what drives most enterprise Databricks deals."
weight: 1
type: lecture
tags:
  - unity-catalog
  - governance
  - nerc-cip
  - ceii
  - compliance
sources:
  - https://docs.databricks.com/aws/en/data-governance/unity-catalog/
  - https://www.nerc.com/standards/reliability-standards/cip
  - https://www.utilitydive.com/news/duke-fined-10m-for-cybersecurity-lapses-since-2015/547528/
  - https://www.databricks.com/blog/open-sourcing-unity-catalog
  - https://www.securityweek.com/us-energy-firm-fined-10-million-security-failures/
  - https://www.industrialdefender.com/blog/what-is-nerc-cip
last_refreshed: "2026-04-08"
---

## The question

Your wind utility's data platform is humming. Delta tables are ACID-compliant. The medallion layers are clean. DLT pipelines catch bad data automatically. Then a letter arrives from NERC — the North American Electric Reliability Corporation — announcing a CIP compliance audit.

The auditor asks three questions:

1. **Who has access to your CEII data?** Show me a list. Show me when it was last reviewed. Show me who approved each entry.
2. **What is the lineage of your quarterly capacity report?** The number says 1.2 TWh. Trace that back to the raw SCADA readings. Every transformation, every filter, every aggregation.
3. **What changed and when?** On March 15, someone modified the Gold table that feeds the compliance dashboard. Who was it? What did they change? Was it authorized?

You look at your S3 bucket, your IAM roles, your Parquet files organized by date. You cannot answer a single one of these questions.

This is not a hypothetical. This is why enterprises buy Databricks.

## $10 million in concrete stakes

<div class="definition">
<strong>CEII (Critical Energy Infrastructure Information)</strong>
Specific engineering, vulnerability, and operational data about energy infrastructure — including generation capacity, grid topology, and physical security details — that FERC designates as requiring restricted access. For a wind utility, this includes turbine GPS coordinates, substation connection points, and generation capacity data that could reveal grid vulnerabilities.[^1]
</div>

In 2019, Duke Energy agreed to pay $10 million to settle 127 NERC CIP violations spanning 2015 to 2018. Thirteen of those violations were classified as "serious," and NERC stated they "collectively posed a serious risk to the security and reliability of the Bulk Power System."[^2] The root causes were not exotic cyberattacks. NERC cited "lack of management engagement, support, and accountability," organizational silos, and deficient processes.[^3]

Translation: Duke did not have adequate controls over who could access what, and they could not prove their compliance posture to auditors. The technology existed. The governance did not.

This is the gap Unity Catalog fills. Not faster queries — governed access, tracked lineage, and immutable audit trails.

## The three questions your data lake cannot answer

Consider what your sensor-analytics pipeline looks like at the 500-turbine scale. You have Bronze tables landing raw SCADA data every 10 minutes. Silver tables clean and validate it. Gold tables aggregate it for analyst dashboards and compliance reports. The data lives in S3, organized as Delta tables.

Now try to answer the auditor's questions with just S3 and IAM:

```mermaid
graph TD
    subgraph "What the auditor asks"
        Q1["Who has access<br/>to CEII data?"]
        Q2["What is the lineage<br/>of this report?"]
        Q3["What changed<br/>and when?"]
    end

    subgraph "What S3 + IAM can tell you"
        A1["IAM role X has<br/>s3:GetObject on<br/>the whole bucket"]
        A2["¯\\_(ツ)_/¯"]
        A3["S3 access logs exist<br/>but they're object-level,<br/>not table-level"]
    end

    Q1 --> A1
    Q2 --> A2
    Q3 --> A3

    style A1 fill:#f9d6d6
    style A2 fill:#f9d6d6
    style A3 fill:#f9d6d6
```

### Question 1: Who has access?

IAM operates at the storage layer — buckets, prefixes, objects. Your CEII data (turbine GPS coordinates, substation connections, generation capacity) lives in specific columns across dozens of tables. IAM cannot say "analyst Jane can see the `avg_power_kw` column but not the `latitude` and `longitude` columns in `wind_prod.scada.turbine_readings`." IAM sees files, not columns.[^4]

Worse, IAM roles are typically shared. The `data-analyst-role` might grant access to the entire `scada/` prefix. When the auditor asks "which specific people can see CEII data," you are reverse-engineering role assignments, group memberships, and assumed roles across multiple AWS accounts. This is not a governance posture. This is an incident response exercise.

### Question 2: What is the lineage?

The quarterly capacity report says your fleet produced 1.2 TWh. The auditor wants to see the chain: raw 10-minute readings from 500 turbines, cleaned to remove sensor errors, aggregated to hourly, aggregated to monthly, summed across the fleet. Which pipeline produced each step? What filters were applied? Were any readings excluded?

S3 has no concept of lineage. Your data files know nothing about where they came from. You could reconstruct this from job logs, notebook revision history, and Git commits — but that requires days of detective work, not a query. And the auditor is sitting across the table right now.

### Question 3: What changed?

Delta Lake gives you table versioning — you can see *that* the Gold table changed on March 15 and *what* the data looked like before and after. But Delta's transaction log does not record *who* made the change, *why* they made it, or whether they had authorization. The `commitInfo` field in the Delta log records the cluster ID and notebook path, not the human identity and their permission chain.

## Why "just use IAM roles" is not governance

IAM is access *control* — it decides whether a request is allowed or denied. Governance is the broader system: access control plus lineage plus audit plus discovery plus classification. Here is why the distinction matters for regulated industries:

| Requirement | IAM alone | Unity Catalog |
|---|---|---|
| Control access to a table | Approximate (via bucket/prefix) | Exact (table, column, row level) |
| Know who accessed CEII data last month | Possible with CloudTrail, but requires mapping object paths to table semantics | Built-in: `system.access.audit` |
| Trace a report back to source data | Not supported | Automatic column-level lineage |
| Prove access was reviewed quarterly | Manual process | Queryable permissions + audit trail |
| Mask GPS coordinates for non-CEII-cleared analysts | Not possible at storage layer | Column masking functions |

The fundamental mismatch: IAM governs *storage*. Unity Catalog governs *data*. Storage is buckets and objects. Data is tables, columns, rows, and the relationships between them. NERC auditors care about data, not storage.[^5]

## What Unity Catalog actually is

<div class="definition">
<strong>Unity Catalog</strong>
Databricks' centralized governance layer for all data and AI assets. It provides a three-level namespace (catalog, schema, table), fine-grained access control (including column masking and row filtering), automatic data lineage tracking, and immutable audit logs — all queryable through SQL. Open-sourced under Apache 2.0 in June 2024 and hosted at the Linux Foundation's LF AI & Data.[^6]
</div>

Unity Catalog sits between your users and your data. Every query, every access, every permission change passes through it. This is not optional overhead — it is the governance layer that lets you answer the auditor's three questions:

1. **Who has access?** `SHOW GRANTS ON TABLE wind_prod.scada.turbine_readings;` — returns every principal with access, at what level, granted by whom.
2. **What is the lineage?** Catalog Explorer shows the full graph from source tables through transformations to downstream dashboards, captured automatically at runtime.
3. **What changed?** `SELECT * FROM system.access.audit WHERE action_name = 'alterTable' AND request_params.full_name_arg = 'wind_prod.scada.gold_hourly_stats';` — returns who changed the table, when, and what the change was.

## The enterprise buying conversation

Most Databricks enterprise deals now hinge on Unity Catalog, not on Spark performance or Delta Lake features. The conversation in the room is rarely "can your engine run our queries fast enough." It is almost always some version of:

- "Can you prove to our compliance team who has access to regulated data?"
- "Can we govern data across our three cloud accounts and two business units?"
- "Our Snowflake instance handles SQL fine, but we need lineage and audit for our ML pipelines too."

Understanding this is critical for anyone in a customer-facing role. When a wind utility evaluates Databricks, the SCADA pipeline's performance requirements might be satisfied by DuckDB on a single VM. What DuckDB cannot provide is the governance posture that lets the utility pass a NERC CIP audit. That is the value proposition.

The next lecture covers the organizational structure that makes this governance possible: the three-level namespace.

[^1]: [FERC CEII Regulations](https://www.ferc.gov/enforcement-legal/ceii) — FERC defines CEII under 18 CFR 388.113.
[^2]: [Duke Energy fined $10M for cybersecurity lapses](https://www.utilitydive.com/news/duke-fined-10m-for-cybersecurity-lapses-since-2015/547528/) — Utility Dive, 2019.
[^3]: [U.S. Energy Firm Fined $10 Million for Security Failures](https://www.securityweek.com/us-energy-firm-fined-10-million-security-failures/) — SecurityWeek, 2019.
[^4]: [Unity Catalog overview](https://docs.databricks.com/aws/en/data-governance/unity-catalog/) — Databricks documentation on governance scope.
[^5]: [NERC CIP Standards](https://www.nerc.com/standards/reliability-standards/cip) — Full list of Critical Infrastructure Protection standards.
[^6]: [Open sourcing Unity Catalog](https://www.databricks.com/blog/open-sourcing-unity-catalog) — Databricks blog, June 2024.
