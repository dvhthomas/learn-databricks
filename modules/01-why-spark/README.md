# Module 1: Why Spark Exists

**Status:** planned  
**Databricks environment:** Community Edition (free)  
**Local code:** none — exercises run in Databricks notebooks

## The question this module answers

Your sensor-analytics project handles 1M readings/day on one machine with DuckDB.
Why does a company like Databricks exist? What problem is Spark actually solving,
and when do you genuinely need it?

## Core concepts

### Distributed compute in one paragraph

Spark distributes both data and computation across a cluster of machines. A
**driver** coordinates the work; **executors** do it. When your data is too large
for one machine — or your computation is parallelizable enough that the distributed
overhead is worth paying — Spark wins. Below that threshold, a single-node tool
like DuckDB beats it on every dimension: speed, simplicity, cost.

### The DAG and lazy evaluation

Spark builds a **Directed Acyclic Graph (DAG)** of your transformations and only
executes when you call an action (`.show()`, `.write()`, `.count()`). Before that,
nothing runs. This lets Spark optimize the whole plan — reordering operations,
pushing filters down, combining steps — before touching any data.

Practical implication: if your job is slow, the bottleneck is usually at an action,
not a transformation.

### The shuffle: the expensive operation

A **shuffle** happens when Spark must redistribute data across executors — during
a `groupBy`, `join`, or `distinct`. Data is written to disk, transferred over the
network, and re-read. Shuffles are:

- The most common cause of slow Spark jobs
- The most common cause of out-of-memory failures
- What you're minimizing when someone says "optimize your Spark code"

Being able to explain this clearly is more valuable than memorizing Spark configs.

### Transformations vs. actions

| Transformations (lazy) | Actions (trigger execution) |
|---|---|
| `filter()`, `select()`, `groupBy()` | `show()`, `count()`, `write()` |
| `join()`, `withColumn()`, `map()` | `collect()`, `take()`, `save()` |
| Build the plan | Execute the plan |

### What Databricks adds on top of Spark

- **Cluster management** — auto-scaling, spot instance handling, no Hadoop ops
- **Photon engine** — vectorized query execution (think DuckDB's approach, distributed)
- **Collaborative notebooks** — version-controlled, multi-language (Python/SQL/Scala/R)
- **Job scheduler** — run notebooks and scripts on a schedule or trigger
- **Delta Lake integration** — the storage layer (Module 2)

## The honest DuckDB vs. Spark comparison

| | DuckDB | Apache Spark |
|---|---|---|
| Best for | < ~1TB, single machine | Multi-TB, distributed |
| Startup | Milliseconds | Minutes |
| Complexity | Low | High |
| Cost | Free | Cluster compute |
| Databricks uses it? | Yes, in DBSQL serverless | Yes, core engine |

For sensor-analytics at 1M readings/day: DuckDB wins. At 1B readings/day across
10,000 sensor types with 50 concurrent analysts: Spark wins. Knowing where the
line is makes you credible to engineers who've seen both misused.

## Reading

- **Start here:** [Databricks: What is Apache Spark?](https://www.databricks.com/spark/about) — 10 min
- **Go deeper:** Learning Spark, 2nd Ed., Ch. 1–3 (O'Reilly — preview available free)
- **The original vision:** [Spark CACM paper](https://cacm.acm.org/magazines/2016/11/209116-apache-spark/fulltext) — read intro + architecture, skip the math
- **Photon:** [Introducing Photon](https://www.databricks.com/blog/2022/04/11/introducing-photon-the-next-generation-query-engine-on-the-databricks-lakehouse-platform.html)

## Hands-on exercise

See [`exercises/`](exercises/) — Databricks notebook to upload and run.

The exercise runs the same sensor data aggregation in both DuckDB and PySpark,
then has you examine the Spark UI to find the shuffle.

## What to write on your blog

> *"I ran the same sensor query in DuckDB and PySpark. DuckDB won. Here's why
> that's not a bug — it's the point."*

Anchor on the trade-off, not the tutorial. The consulting insight is knowing
*when* each tool is the right choice.
