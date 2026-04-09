---
title: "What makes Spark jobs slow?"
summary: "The shuffle — the single most important concept for understanding Spark performance"
weight: 3
type: lecture
tags:
  - shuffle
  - performance
  - stages
sources:
  - https://spark.apache.org/docs/latest/rdd-programming-guide.html#shuffle-operations
  - https://www.databricks.com/blog/2022/04/11/introducing-photon-the-next-generation-query-engine-on-the-databricks-lakehouse-platform.html
last_refreshed: ""
---

## The question

Your Spark job processes 1TB of sensor data across 10 executors. Some operations finish in seconds. Others take 45 minutes. The data size didn't change. The cluster didn't change. So what's different about the slow operations?

The answer, almost every time, is the **shuffle**. Understanding what a shuffle is, why it's expensive, and how to minimize it is the single most practical thing you can learn about Spark performance.

## When operations are fast

Consider this transformation:

```python
df = spark.read.parquet("sensors/")
filtered = df.filter(col("units") == "degrees_c")
selected = filtered.select("sensor_id", "value", "timestamp")
```

This is fast, regardless of data size. Why? Because every executor can do this work independently on its own partitions. Executor 1 filters its partition for `degrees_c` rows and selects three columns. Executor 2 does the same on its partition. No executor needs to talk to any other executor. No data moves between machines.

Spark calls these **narrow transformations** — each output partition depends on only one input partition.

## When operations get expensive

Now add a `groupBy`:

```python
avg_by_sensor = filtered.groupBy("sensor_id").agg(avg("value"))
```

This changes everything. To compute the average for `sensor_0042`, Spark needs ALL rows for that sensor — but those rows are spread across many executors (because the data was partitioned by file, not by sensor ID). Spark must physically move data from every executor to whichever executor is responsible for `sensor_0042`.

Multiply that by thousands of distinct sensor IDs, and you have a massive data transfer.

<div class="definition">
<strong>Shuffle</strong>
The process of redistributing data across executors so that rows with the same key end up on the same machine. Shuffles happen during groupBy, join, distinct, repartition, and any operation that requires data from multiple partitions to be combined. During a shuffle, every executor writes its outgoing data to local disk, then every executor reads incoming data from every other executor over the network.
</div>

## Why shuffles are expensive

A shuffle involves three costs that are each individually significant:

**Disk I/O.** Before transferring data, each executor writes its outgoing shuffle data to local disk. This is called the "shuffle write." On the receiving end, executors read the incoming data from disk again. All of this happens even though the data was already in memory.

**Network transfer.** The shuffle data must travel over the network from every executor to every other executor. If you have 100 executors, the network traffic scales with the square of the executor count. On a large cluster processing terabytes, shuffle transfers can saturate the network.

**Serialization.** Data must be serialized (converted to bytes) for transfer and deserialized on arrival. This costs CPU time.

Here's a rough sense of the speed differences:

| Operation | Typical speed |
|---|---|
| Read from memory | ~10 GB/s |
| Read from local SSD | ~2 GB/s |
| Read over network (within data center) | ~1 GB/s |
| Read over network (cross-zone) | ~0.1-0.5 GB/s |

A shuffle turns an in-memory operation into a disk + network + serialization operation. That's often a 10-100x slowdown.

## Stages: where the boundaries are

Spark uses shuffles to divide your job into **stages**.

<div class="definition">
<strong>Stage</strong>
A group of tasks that can run without a shuffle. When Spark encounters an operation that requires a shuffle (like groupBy or join), it creates a stage boundary. All tasks in the current stage must complete and write their shuffle data before the next stage can begin.
</div>

For our sensor query:

```python
result = (
    spark.read.parquet("sensors/")           # Stage 1: read + filter + select
    .filter(col("units") == "degrees_c")     #   (narrow transformations, no shuffle)
    .select("sensor_id", "value")            #
    .groupBy("sensor_id")                    # -- shuffle boundary --
    .agg(avg("value"))                       # Stage 2: aggregate
    .orderBy("avg_temp", ascending=False)    # -- shuffle boundary --
)                                            # Stage 3: sort
```

This job has 3 stages and 2 shuffles. The stages run sequentially — Stage 2 can't start until Stage 1's shuffle write is complete. This is why shuffles are also bottlenecks in wall-clock time: they create sequential barriers in an otherwise parallel computation.

## The Spark UI: seeing shuffles for yourself

When you run a Spark job on Databricks, the Spark UI shows you exactly what happened:

- **The Jobs tab** shows the overall timeline
- **The Stages tab** shows each stage, how many tasks it had, and how long they took
- **The SQL tab** shows the physical plan with shuffle boundaries marked

The most important numbers in the Spark UI for performance:
- **Shuffle Read / Shuffle Write** — how much data crossed the network
- **Task duration distribution** — are some tasks much slower than others? (this indicates data skew)
- **Spill (Memory) / Spill (Disk)** — did executors run out of memory and spill to disk?

If a job is slow, look at the Spark UI first. The shuffle metrics will almost always point you to the problem.

## Common shuffle triggers and how to think about them

| Operation | Why it shuffles | Can you avoid it? |
|---|---|---|
| `groupBy().agg()` | Rows for same key must be co-located | Not really — but you can reduce data before the group |
| `join()` | Matching rows from two datasets must meet | Use a broadcast join if one side is small (<100MB) |
| `distinct()` | Must compare all rows | Sometimes `dropDuplicates` on a subset of columns is cheaper |
| `orderBy()` | Global sort requires all data to be compared | Do you actually need a global sort, or is `sortWithinPartitions` enough? |
| `repartition()` | Explicitly redistributes data | Only use when you have a good reason |

The instinct to develop: before writing a transformation, ask yourself "does this need data from multiple partitions?" If yes, there's a shuffle, and you should make sure it's worth it.

## What Databricks does about this

Spark shuffles are inherently expensive, but Databricks has invested heavily in making them less painful:

**Photon engine.** Databricks' native vectorized execution engine, written in C++, that replaces parts of the JVM-based Spark engine. Photon is particularly effective at shuffle-heavy operations because it's faster at serialization and more efficient with memory.

**Adaptive Query Execution (AQE).** Spark 3.0+ (enabled by default on Databricks) can dynamically adjust the query plan during execution. If one partition ends up with much more data than others after a shuffle (data skew), AQE can split that partition into smaller pieces. It can also coalesce too-small partitions after a shuffle.

These don't eliminate shuffles, but they reduce the pain. The fundamental rule still applies: the fewer shuffles, the faster your job.

**Key takeaway: A shuffle moves data across the network so that rows with the same key land on the same executor. Shuffles are the primary cause of slow Spark jobs because they replace fast in-memory operations with slow disk + network + serialization operations. Every groupBy, join, and sort triggers a shuffle. Learning to minimize shuffles is the most practical Spark skill you can develop.**
