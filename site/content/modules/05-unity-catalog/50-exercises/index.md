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

---

## Governance ROI cost model (CalcMark)

Unity Catalog is included in Databricks Premium tier — there is no separate SKU. So what does governance actually cost to *operate*, and how does that compare to the cost of a NERC CIP violation?

Open `modules/05-unity-catalog/exercises/governance-roi.cm` and run it:

```bash
cm eval governance-roi.cm -v
```

### What the model covers

1. **The cost of Unity Catalog governance** — engineer time managing permissions and audit logs, system table storage, staff training. Spoiler: it is about $13K/year.
2. **The cost of NOT having governance** — NERC CIP penalty structure, real-world settlements (Duke Energy's $10M for 127 violations), and what a first audit looks like when your access controls live in a spreadsheet.
3. **The DIY alternative** — building governance from Atlan/Alation + custom engineering. Works, but costs about 5x more than UC governance.
4. **The break-even question** — UC pays for itself if it prevents one NERC finding every 57 years. The business case is not subtle.
5. **Scaling to 1,000 turbines** — governance costs scale sublinearly (ABAC policies, not per-user grants), but regulatory risk scales superlinearly.

### What to do with it

- Read through the assumptions and sources. Do you agree with the numbers? Change any that seem wrong and rerun.
- Set `likely_findings = 1` — even one finding justifies decades of UC governance spend.
- Set `governance_hours_weekly = 4` (the upper end) — does the break-even change meaningfully?
- Compare `total_governance_ongoing` to `diy_total`. When would you choose DIY governance over Unity Catalog?

### Reflection

After running the model, you should be able to answer:

- Why is the break-even calculation almost irrelevant to the actual decision?
- A customer says "we already have Atlan for our data catalog, why do we need Unity Catalog?" What is the honest answer?
- What governance capabilities does Unity Catalog provide that a standalone catalog like Atlan cannot?
