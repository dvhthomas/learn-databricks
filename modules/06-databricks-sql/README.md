# Module 6: Databricks SQL

**Status:** planned  
**Databricks environment:** Free trial workspace  
**Local code:** optional — `uv run python exercises/query_dbsql.py` (requires workspace)

## The question this module answers

Your Gold table exists, it's governed by Unity Catalog, and your data engineers
love it. But the 20 SQL analysts on the team have never opened a notebook. They
want a BI tool and a SQL editor. How does Databricks serve them?

## Core concepts

### What a SQL warehouse is

A SQL warehouse is a compute endpoint optimized for SQL analytics — not Spark
jobs, not notebooks, just SQL. It's serverless: it starts in ~2 seconds, scales
automatically to handle concurrent users, and shuts down when idle. You pay
for what you use.

From an analyst's perspective: connect your BI tool, write SQL, get results.
It feels like any other data warehouse.

From an architecture perspective: it's Photon (Databricks' vectorized engine)
running against Delta tables governed by Unity Catalog.

### Photon: why DBSQL is fast

Photon is a rewritten query execution engine that Databricks ships alongside Spark.
Key difference: **vectorized execution** — it processes data in column-oriented batches
rather than row by row. This is the same approach DuckDB uses, applied at
distributed scale.

For SQL analytics (filters, aggregations, joins on large tables), Photon can be
5–10x faster than vanilla Spark. This is what made DBSQL competitive with Snowflake
on SQL workloads.

### The Snowflake comparison

This is unavoidable. Every DBSQL conversation eventually becomes one:

| | Databricks SQL | Snowflake |
|---|---|---|
| Core identity | SQL layer on lakehouse | SQL warehouse, period |
| Startup time | ~2s serverless | ~1s |
| Concurrency | Good, still closing the gap | Excellent, mature |
| Storage format | Delta Lake (open) | Proprietary + Iceberg |
| ML integration | Native — same platform | Cortex AI (newer) |
| Data sharing | Delta Sharing | Native Secure Data Sharing (more mature) |
| Governance | Unity Catalog | Native, longer track record |
| Pricing | DBU per second | Credit per second |
| Best for | Engineering + analytics unified | SQL-first teams |

**The honest answer for customers:** Snowflake is still better at pure SQL analytics
workloads with high concurrency. Databricks wins when you also need data engineering
and ML on the same platform and same data. Many enterprises have both.

### Data optimization features worth knowing

- **Z-ordering:** Sort data within Parquet files by frequently filtered columns.
  Speeds up queries like `WHERE sensor_id = 'sensor_0001'` by skipping files.
- **Liquid clustering:** Newer, automatic approach — replaces Z-ordering. Databricks
  handles re-clustering in the background as data grows. Prefer this for new tables.
- **Result caching:** Identical queries return cached results without re-executing.
  Transparent to the analyst. Major for dashboard performance.
- **Predictive I/O:** Pre-fetches data based on query patterns. Also transparent.

### BI tool connectivity

DBSQL exposes JDBC/ODBC and a REST API. Works with Tableau, Power BI, Looker,
Sigma, ThoughtSpot, and most others via Partner Connect (one-click setup in the UI).

## Reading

- [Databricks SQL documentation](https://docs.databricks.com/en/sql/index.html)
- [Photon engine](https://www.databricks.com/blog/2022/04/11/introducing-photon-the-next-generation-query-engine-on-the-databricks-lakehouse-platform.html)
- [Liquid clustering](https://docs.databricks.com/en/delta/clustering.html)
- [Neutral Databricks vs. Snowflake comparison](https://www.fivetran.com/blog/databricks-vs-snowflake)

## Hands-on exercise

See [`exercises/`](exercises/) for two parts:

1. **`06_dbsql_queries.sql`** — build a dashboard on your Gold table in the
   Databricks SQL editor. Replaces the Flask dashboard from sensor-analytics
   without writing a single line of application code.

2. **`query_dbsql.py`** — optional Python script that queries DBSQL from your
   local machine using the `databricks-sql-connector`. Shows how a downstream
   app would consume DBSQL programmatically.

## What to write on your blog

Build the same dashboard twice: the Flask app in sensor-analytics, and the DBSQL
version. Time both. Count the lines of infrastructure code. The gap is the platform
value proposition — and it's also the trade-off (you gave up real-time push updates
and custom logic). That's the consulting conversation.
