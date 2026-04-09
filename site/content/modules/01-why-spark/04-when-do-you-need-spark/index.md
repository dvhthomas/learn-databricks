---
title: "When do you actually need Spark — and when don't you?"
summary: "The honest comparison with DuckDB and other single-node tools, and where Databricks fits in the picture"
weight: 4
type: lecture
tags:
  - spark-vs-duckdb
  - databricks
  - when-to-use
sources:
  - https://duckdb.org/why_duckdb
  - https://www.databricks.com/product/databricks-sql
  - https://www.databricks.com/blog/2022/04/11/introducing-photon-the-next-generation-query-engine-on-the-databricks-lakehouse-platform.html
last_refreshed: ""
---

## The question

Your team processes 500GB of sensor data daily. An engineer suggests setting up a Spark cluster. Another says DuckDB on a single beefy machine would be simpler and faster. Who's right?

This is a question you'll face constantly — as a practitioner making infrastructure decisions, or in a conversation with someone evaluating Databricks. The credible answer isn't "always use Spark." It's knowing where the crossover point is.

## The case for NOT using Spark

Here's an uncomfortable truth that Databricks sales engineers won't lead with: for most datasets at most companies, a single machine is faster, cheaper, and simpler than a Spark cluster.

<div class="definition">
<strong>DuckDB</strong>
An embedded analytical database (like SQLite, but for analytics). It runs in a single process on a single machine, processes data in a columnar format, and is optimized for analytical queries on datasets that fit on one node. It requires zero infrastructure — no cluster, no configuration, no server.
</div>

DuckDB (and similar tools like Polars) represents a different philosophy: instead of distributing the computation, make a single machine as efficient as possible.

Consider a concrete scenario: your sensor-analytics pipeline processes 1 million readings per day. That's roughly 100MB of Parquet data per day, or ~36GB per year. Let's run the same aggregation both ways:

**DuckDB:**
```python
import duckdb

result = duckdb.sql("""
    SELECT sensor_id, avg(value) as avg_reading
    FROM read_parquet('sensors/*.parquet')
    WHERE units = 'degrees_c'
    GROUP BY sensor_id
    ORDER BY avg_reading DESC
""").fetchdf()
```
- Startup time: milliseconds
- Query time on 36GB: ~10-30 seconds
- Infrastructure: none
- Cost: $0

**PySpark:**
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col

spark = SparkSession.builder.getOrCreate()
result = (
    spark.read.parquet("sensors/")
    .filter(col("units") == "degrees_c")
    .groupBy("sensor_id")
    .agg(avg("value").alias("avg_reading"))
    .orderBy("avg_reading", ascending=False)
)
result.show()
```
- Startup time: 30 seconds to several minutes (cluster must start)
- Query time on 36GB: ~15-60 seconds (depends on cluster size)
- Infrastructure: a Spark cluster (managed or self-hosted)
- Cost: $2-10/hour for a small cluster on Databricks

For this workload, DuckDB wins on every dimension. It's faster (no startup overhead), simpler (no cluster), and free.

## Where the crossover happens

So when does Spark actually become the right tool? There are three inflection points:

### Data volume beyond one machine

Modern machines with 256GB-1TB of RAM can handle surprisingly large datasets. DuckDB can query datasets much larger than RAM by streaming from disk. But there's a practical ceiling around **1-5TB** for interactive queries on a single machine. Beyond that, you need to distribute.

A sensor network with 10,000 sensor types recording every second generates ~300GB/day — roughly 100TB/year. After two years, no single machine handles this well. This is where Spark earns its keep.

### Concurrent access

This is the inflection point people underestimate. DuckDB runs in a single process. If 30 analysts all need to query the same dataset interactively, they can't share a DuckDB instance effectively.

Spark (through Databricks SQL) can serve dozens or hundreds of concurrent users against the same data, with query isolation and resource management. For organizations with large analyst teams, this is often the deciding factor — not raw data volume.

### Complex multi-step pipelines

If your data processing is a single query, single-node tools are often sufficient. But production data platforms rarely involve just one query. They involve:

- Ingesting from multiple sources (APIs, files, streams)
- Cleaning and validating at multiple stages
- Joining across datasets
- Feeding multiple downstream consumers (dashboards, ML models, reports)

Spark's ability to express these pipelines in a single framework — with scheduling, monitoring, and lineage tracking through Databricks — becomes genuinely valuable at this complexity level.

## The honest comparison

| | DuckDB / single-node | Spark / Databricks |
|---|---|---|
| **Best for** | < ~1-5TB, small teams, simple pipelines | Multi-TB, many concurrent users, complex pipelines |
| **Startup time** | Milliseconds | Minutes (cluster startup) |
| **Complexity** | Low — one process, no infrastructure | High — cluster management, configuration tuning |
| **Cost at small scale** | Free | $2-50/hour (cluster compute) |
| **Cost at large scale** | Impossible (data doesn't fit) | Scales linearly with data and users |
| **Concurrency** | Limited (single process) | High (shared cluster, query isolation) |
| **Ecosystem** | Standalone tool | Part of a full platform (governance, ML, BI) |

The honest summary: **DuckDB is better for small-to-medium datasets with small teams. Spark is better for large datasets, many concurrent users, or complex multi-step pipelines. The crossover point is higher than most people think.**

## Where Databricks fits

Spark is an open-source engine. You can run it yourself on AWS EMR, Google Dataproc, or your own machines. So why do companies pay Databricks?

<div class="definition">
<strong>Databricks</strong>
A managed platform built around Apache Spark. It adds cluster management, collaborative notebooks, a job scheduler, Delta Lake for storage, Unity Catalog for governance, and Databricks SQL for analyst-facing queries. The pitch: you get Spark's power without Spark's operational pain.
</div>

What Databricks adds on top of open-source Spark:

**You don't manage clusters.** Starting, sizing, autoscaling, and terminating clusters is handled for you. On open-source Spark, cluster management is a full-time job (literally — many companies have a "Spark platform team").

**Photon.** Databricks' native C++ execution engine that replaces parts of the JVM-based Spark engine. For SQL-heavy workloads, Photon can be 2-8x faster than open-source Spark. This is a genuine competitive advantage, not marketing.

**Collaborative notebooks.** Multi-language notebooks (Python, SQL, Scala, R) with version control, shared state, and scheduled execution. This is where data engineers and data scientists do their daily work.

**The rest of the platform.** Delta Lake (Module 2), Unity Catalog (Module 5), Databricks SQL (Module 6), MLflow (Module 7) — Spark is the engine, but the platform around it is what enterprise buyers actually care about.

## The question you need to answer fluently

If someone asks "why not just use DuckDB?" or "when do you actually need Spark?", here's the shape of a good answer:

> "DuckDB is the right tool when your data fits on one machine and your team is small. It's faster to start, simpler to operate, and genuinely better for that use case. Spark becomes the right tool when you cross one of three thresholds: data that exceeds what one machine can handle, enough concurrent users that you need a shared query engine, or pipeline complexity that benefits from a unified platform. Databricks makes Spark operational by managing the infrastructure and wrapping it with governance, SQL analytics, and ML tooling."

That's an answer that builds trust because it's honest about when Spark ISN'T the right tool. Knowing the boundaries of a technology is more credible than being an unconditional advocate.

**Key takeaway: Spark isn't always better than single-node tools. DuckDB beats Spark for small-to-medium data with small teams. Spark earns its keep at the intersection of large data, many concurrent users, and complex pipelines. Databricks earns its keep by making Spark operational and wrapping it with a full data platform. Knowing where these crossover points are is more valuable than being a Spark evangelist.**
