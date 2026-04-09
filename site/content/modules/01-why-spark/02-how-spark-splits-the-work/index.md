---
title: "How does Spark actually split up the work?"
summary: "The driver/executor model, partitions, the DAG, and why Spark waits until the last possible moment to do anything"
weight: 2
type: lecture
tags:
  - driver-executor
  - partitions
  - dag
  - lazy-evaluation
sources:
  - https://spark.apache.org/docs/latest/cluster-overview.html
  - https://www.databricks.com/spark/about
last_refreshed: ""
---

## The question

You write `df.filter(...).groupBy(...).count()` in PySpark and hit run. What actually happens? Where does this code execute? How does Spark decide which machines do what work, and how much data each one gets?

Understanding this machinery is the difference between someone who *uses* Spark and someone who can *reason about* Spark — debug slow jobs, explain performance decisions, or advise a team on cluster sizing.

## A single machine, for comparison

On a single machine with pandas or DuckDB, the mental model is simple: your code runs top-to-bottom, one operation at a time, on the data sitting on your local disk. When you call `df.groupby("sensor_id").mean()`, the CPU reads the data, groups it, computes the means, and returns the result. Everything happens in one process, in one place.

This simplicity is a genuine advantage. When it works, nothing beats it for speed of development and ease of debugging.

## Two roles: driver and executors

When you submit code to Spark, it doesn't run on one machine. It runs on a cluster — a collection of machines coordinated to act as one system.

<div class="definition">
<strong>Driver</strong>
The single process that runs your main program. It accepts your code, plans the execution, and coordinates the work. The driver does NOT process your data — it manages the processes that do. Think of it as the conductor of an orchestra: it doesn't play any instruments, but without it, the musicians can't coordinate.
</div>

<div class="definition">
<strong>Executor</strong>
A worker process that runs on a machine in the cluster. Each executor receives tasks from the driver, processes a portion of the data, and reports results back. A cluster typically has many executors — anywhere from 2 to hundreds, depending on the workload.
</div>

When you write `spark.read.parquet("sensors/")`, the driver doesn't read the data. It tells the executors where the data is and what to do with it. Each executor reads a portion of the files and processes its share.

## Partitions: how data gets divided

Spark doesn't send random chunks of data to each executor. It divides the data into logical slices called partitions.

<div class="definition">
<strong>Partition</strong>
A chunk of your dataset that one executor task processes independently. If your data has 200 partitions and you have 10 executors, each executor processes roughly 20 partitions (one at a time or a few in parallel, depending on cores). Partitions are the fundamental unit of parallelism in Spark.
</div>

How does Spark decide on partitions?

- **Reading files:** Each file (or file block) typically becomes one partition. If you have 200 Parquet files, you get roughly 200 partitions.
- **After a shuffle** (more on this in the next lecture): Spark repartitions the data based on a configuration parameter (`spark.sql.shuffle.partitions`, default 200).
- **You can control it:** `df.repartition(100)` explicitly sets the partition count.

Partition count matters more than most people think. Too few partitions means some executors sit idle while others are overloaded. Too many means the overhead of managing tiny tasks dominates actual processing. A reasonable starting point: 2-4 partitions per CPU core in your cluster.

## The DAG: Spark's execution plan

When you write a chain of transformations like:

```python
result = (
    df
    .filter(col("units") == "degrees_c")
    .groupBy("sensor_id")
    .agg(avg("value").alias("avg_temp"))
    .orderBy("avg_temp", ascending=False)
)
```

Spark doesn't execute each line as you write it. It records what you *want* to do and builds a plan.

<div class="definition">
<strong>DAG (Directed Acyclic Graph)</strong>
Spark's internal representation of your computation as a graph of steps. Each node is an operation (filter, group, sort); edges show data flow. "Directed" means data flows one way. "Acyclic" means no loops — the plan always moves forward. Spark uses this graph to optimize the entire computation before running anything.
</div>

Why build a plan instead of executing immediately? Because the plan lets Spark optimize. It can:

- **Reorder operations.** Push a filter before a join so less data gets shuffled.
- **Combine steps.** Merge adjacent operations that can run together without moving data.
- **Skip unnecessary work.** If you only select 3 columns from a 50-column Parquet file, Spark reads only those 3 columns from disk (this is called "column pruning").

You can see the plan by calling `.explain()`:

```python
result.explain(True)
```

This prints the physical and logical plans — extremely useful for debugging slow queries. If you're ever wondering "why is this slow?", the plan is where you look first.

## Lazy evaluation: nothing runs until you ask for results

This is the concept that surprises people coming from pandas or SQL:

<div class="definition">
<strong>Lazy evaluation</strong>
Spark records transformations (filter, groupBy, join, select) but does NOT execute them. Execution only happens when you call an <em>action</em> — an operation that needs to return a result to the driver or write data to storage.
</div>

**Transformations** (lazy — build the plan):
`filter()`, `select()`, `groupBy()`, `join()`, `withColumn()`, `orderBy()`

**Actions** (trigger execution):
`show()`, `count()`, `collect()`, `write.parquet()`, `take(10)`

This means you can build an arbitrarily complex chain of transformations and Spark won't touch any data. Only when you call `.show()` or `.write()` does the engine execute the entire plan.

Practical consequences:

- **Debugging is different.** An error in your transformation logic might not appear until you call an action — possibly many lines later in your code. This trips up everyone at first.
- **Chaining is free.** Adding another `.filter()` or `.select()` to a chain costs nothing at build time. Spark optimizes the whole thing together.
- **Plans can be inspected.** Since nothing has executed, you can call `.explain()` to see what Spark *would* do, without doing it.

## Putting it together: what happens when you hit "run"

Here's the full picture for our sensor query:

1. **You write transformations.** `df.filter(...).groupBy(...).agg(...)` — Spark records each step in the DAG. Nothing executes.
2. **You call an action.** `.show()` — NOW Spark looks at the full DAG.
3. **The optimizer kicks in.** Spark's Catalyst optimizer rewrites the plan: pushes the filter down (less data to read), prunes unnecessary columns, determines the join strategy.
4. **The driver divides work into stages and tasks.** A stage is a group of operations that can run without moving data between executors. A task is one stage applied to one partition.
5. **Executors process their partitions.** Each executor reads its portion of the Parquet files, applies the filter, and computes partial aggregations.
6. **Results come back.** The driver collects the final results and returns them to your notebook.

The next lecture covers the one thing that makes this machinery expensive: what happens when Spark DOES need to move data between executors.

**Key takeaway: Spark separates planning from execution. The driver builds a DAG of your transformations, optimizes the whole plan, then distributes the work across executors that each process a partition of the data. Nothing runs until you call an action.**
