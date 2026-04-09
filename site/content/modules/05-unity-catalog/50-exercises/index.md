---
title: "Exercises: Unity Catalog"
summary: "Set up a namespace, configure access controls, trace lineage, and query audit logs — all in a Databricks workspace with Unity Catalog enabled."
weight: 50
type: exercise
tags:
  - unity-catalog
  - access-control
  - lineage
  - audit
---

## Unity Catalog hands-on (SQL, Databricks workspace)

This exercise runs in a Databricks SQL editor on a workspace with Unity Catalog enabled. A free 14-day trial workspace includes Unity Catalog. You cannot run these exercises locally — Unity Catalog requires the managed Databricks control plane.

Open `modules/05-unity-catalog/exercises/05_unity_catalog.sql` in a Databricks SQL editor and work through each section in order.

### What you will do

1. **Explore** the existing metastore — see what catalogs and schemas exist by default
2. **Create** a catalog (`learning`) and schema (`sensors`) to establish your own namespace
3. **Create** a managed Delta table (`gold_hourly_stats`) with sample turbine data
4. **Grant and revoke** permissions — verify that access is denied before a GRANT and allowed after
5. **Add metadata** — column comments, table tags for discoverability
6. **Trace lineage** — run a query and observe the lineage graph in Catalog Explorer
7. **Query audit logs** — find your own recent activity in `system.access.audit`

### Prerequisites

- A Databricks workspace with Unity Catalog enabled (free trial works)
- Access to a SQL warehouse (serverless or pro)
- Permission to create catalogs (workspace admin, or granted `CREATE CATALOG` on the metastore)

### After running

You should be able to answer these reflection questions (they appear at the end of the SQL file):

- What is the difference between `GRANT` on a table vs. `GRANT` on a schema? When would you use each?
- You find in the audit log that a user queried a CEII table they should not have access to. What do you do? What in UC prevents this in the future?
- What is the difference between the `learning` catalog you created and the `main` catalog that exists by default?
- A new data engineer joins the team. What is the minimum set of grants they need to work with the sensors schema?
