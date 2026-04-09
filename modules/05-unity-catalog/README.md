# Module 5: Unity Catalog

**Status:** planned  
**Databricks environment:** Free trial workspace (14 days — Unity Catalog requires full workspace)  
**Local code:** none — all exercises run in Databricks

## The question this module answers

You have Bronze, Silver, and Gold Delta tables running in DLT. Anyone with workspace
access can read anything. There's no audit trail. You can't prove to your security
team who has access to what. How does a regulated enterprise adopt Databricks?

Unity Catalog is the answer. It's often what enterprises are actually buying.

## Core concepts

### The three-level namespace

```
Metastore  (one per region — shared across ALL workspaces)
└── Catalog  (project, team, or environment boundary)
    └── Schema  (logical grouping, like a database)
        └── Table / View / Function / Volume
```

A fully qualified table reference: `prod.sensors.gold_hourly_stats`

The metastore is shared. A data analyst in the analytics workspace and an ML
engineer in the ML workspace see the same catalog, governed by the same policies.
This is the fundamental difference from the legacy Hive Metastore, which was
siloed per workspace.

### What Unity Catalog governs

**Access control** at every level:

```sql
-- Grant a team read access to a schema
GRANT SELECT ON SCHEMA prod.sensors TO `data-analysts@company.com`;

-- Restrict a sensitive table within that schema
REVOKE SELECT ON TABLE prod.sensors.silver_raw FROM `data-analysts@company.com`;

-- Column-level: mask PII for a group
-- Row-level: filter by region so each team only sees their data
```

**Data lineage** — automatically tracked across notebooks, SQL queries, DLT
pipelines, and jobs. Before you alter a schema, you can answer "what downstream
tables and dashboards will break?" with a graph, not with grep.

**Audit logs** — every query, every access change, every schema modification is
logged. Searchable. Exportable. This is what SOC 2 and HIPAA auditors want.

**Data discovery** — search for tables, add descriptions, tag columns with
`pii: true` or `sla: gold`. Data consumers can find what they need without
asking a data engineer.

### Managed vs. external tables

- **Managed tables:** Databricks owns the data lifecycle. DROP TABLE = data deleted.
- **External tables:** You own the data in cloud storage. DROP TABLE = metadata only.

For regulated industries, external tables are common — the data stays in your
cloud account under your policies, Databricks just governs access to it.

### The migration story

Most existing Databricks customers are migrating from the legacy Hive Metastore
to Unity Catalog. This migration is non-trivial — table permissions, storage
credentials, and compute policies all change. Understanding the migration pain
(and how to reduce it) is practical consulting knowledge that comes up constantly.

## Why this matters for the role

Enterprise deals often stall on governance, not performance. "Can you prove who
has access to our customer data?" is a question that Spark performance numbers
don't answer. Unity Catalog does. Being fluent here is directly tied to the
consulting value you bring.

## Reading

- [Unity Catalog overview](https://docs.databricks.com/en/data-governance/unity-catalog/index.html) — read the full overview page
- [Hive Metastore migration guide](https://docs.databricks.com/en/data-governance/unity-catalog/migrate.html) — skim for the customer migration story
- [Column and row-level security](https://docs.databricks.com/en/data-governance/unity-catalog/row-and-column-filters.html)
- [System tables](https://docs.databricks.com/en/administration-guide/system-tables/index.html) — audit logs and lineage as queryable Delta tables
- [Databricks Data Intelligence Platform positioning](https://www.databricks.com/product/data-intelligence-platform)

## Hands-on exercise

See [`exercises/`](exercises/) — a structured walkthrough in a Databricks notebook.

You'll create a Unity Catalog metastore, register your Gold table, set explicit
grants, add tags, and examine lineage and audit logs.

## What to write on your blog

The posture shift is the story: from "everyone with workspace access can read
everything" to "nothing is readable without an explicit grant." That's not just
a technical change — it's a governance culture change. Write about what that
means for an enterprise data team and why it's hard to adopt.
