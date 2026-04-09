---
title: "Module 6: Databricks SQL"
summary: "15 analysts each have their own CSV extracts. Reports disagree. The CFO asks why the capacity factor is different in every meeting."
status: in-progress
weight: 6
tags:
  - databricks-sql
  - sql-warehouse
  - photon
  - snowflake
  - bi-tools
prerequisites:
  - 1
  - 2
  - 5
last_refreshed: "2026-04-08"
---

Your wind utility has reliable data pipelines, governed tables, and clean medallion layers. But the 15 analysts who actually build the reports and dashboards are frustrated. They don't use notebooks. They use SQL, Tableau, and Excel. Their experience on the platform is what determines whether the CFO considers the Databricks investment worthwhile.

Right now, each analyst has their own process: download CSVs, load into local tools, build reports. The fleet capacity factor shows up differently in every meeting because each analyst applied slightly different filters. The CFO is losing confidence in the data.

**Databricks SQL (DBSQL) is the analyst-facing query layer.** It provides SQL warehouses — dedicated compute endpoints optimized for BI workloads — that connect to the same governed Delta tables the engineers write to. Analysts query Gold tables through SQL, Tableau, or PowerBI. Everyone hits the same data, through the same governance layer.

This is where the Snowflake comparison becomes unavoidable. Every DBSQL conversation eventually turns into "so how does this compare to Snowflake?" You need a nuanced, honest answer. Snowflake is genuinely better at some things — its SQL interface is more mature, its concurrency scaling is more straightforward, and its ecosystem of SQL tools is deeper. Databricks' advantage is the unified platform: the same data, from ingestion through ML, without ETL between systems.

This module teaches DBSQL from the analyst's perspective — not the engineer's — because that's the viewpoint that matters for platform adoption.

## Prerequisites

Complete [Module 5: Unity Catalog]({{< ref "05-unity-catalog" >}}). Analysts query through the governance layer — you need to understand what they're connecting to.

## Exercises

Exercises live in [`modules/06-databricks-sql/exercises/`](https://github.com/dvhthomas/learn-databricks/tree/main/modules/06-databricks-sql/exercises). You'll write SQL queries against wind turbine data, examine query plans, and compare the experience with Snowflake's model.
