# Module 4: Delta Live Tables

**Status:** planned  
**Databricks environment:** Community Edition  
**Local code:** none — DLT only runs in Databricks

## The question this module answers

In Module 3, you wrote three scripts: Bronze, Silver, Gold. They worked, but you
were responsible for running them in order, retrying failures, tracking quality
metrics, and ensuring idempotency. What if the platform did all of that?

## Core concepts

### Declarative vs. imperative pipelines

Module 3 was imperative: you wrote *how* to move data. DLT is declarative: you
describe *what* each table should look like, and Databricks figures out how.

```python
import dlt
from pyspark.sql import functions as F

@dlt.table(comment="Raw sensor readings, append-only")
def bronze_sensor_readings():
    return spark.readStream.format("cloudFiles") \
        .option("cloudFiles.format", "json") \
        .load("/mnt/raw/sensors/")

@dlt.table
@dlt.expect_or_drop("valid_range", "value BETWEEN -50 AND 100")
@dlt.expect_or_drop("sensor_not_null", "sensor_id IS NOT NULL")
def silver_sensor_readings():
    return dlt.read_stream("bronze_sensor_readings") \
        .withColumn("processed_at", F.current_timestamp())

@dlt.table
def gold_hourly_stats():
    return (
        dlt.read("silver_sensor_readings")
        .groupBy("sensor_id", F.date_trunc("hour", "timestamp").alias("hour"))
        .agg(F.avg("value").alias("avg_temp_c"), F.count("*").alias("readings"))
    )
```

DLT infers the dependency graph from `dlt.read()` calls. Silver won't run until
Bronze has new data. Gold won't run until Silver is updated.

### Data quality as first-class

| Decorator | What it does |
|---|---|
| `@dlt.expect("name", "condition")` | Warn on violation, keep the row |
| `@dlt.expect_or_drop("name", "condition")` | Drop violating rows, track count |
| `@dlt.expect_or_fail("name", "condition")` | Fail the pipeline on any violation |

Failed rows are tracked in a quality metrics table automatically — not just right
now, but historically. You can trend quality over time without writing any logging code.

This is what compliance teams actually want: not "we validate data" but "our Silver
table had a 99.3% validity rate last month, here's the trend."

### `read()` vs. `read_stream()`

- `dlt.read_stream()` — streaming: process new data as it arrives (Bronze → Silver)
- `dlt.read()` — batch: recompute the whole table (Silver → Gold)

You can mix both in one pipeline. Near-real-time ingestion feeding periodic aggregates
is the standard pattern.

### DLT vs. Airflow

DLT is for data transformation within Databricks. Airflow/Workflows orchestrate
broader workflows (triggering ingestion from external systems, coordinating across
platforms). Most enterprises use both: Airflow to schedule and trigger, DLT for the
actual transformation logic. Knowing when to use each is a real consulting question.

## Reading

- [DLT Documentation](https://docs.databricks.com/en/delta-live-tables/index.html) — start with Quickstart
- [DLT Expectations](https://docs.databricks.com/en/delta-live-tables/expectations.html)
- [Databricks Workflows vs. DLT](https://docs.databricks.com/en/jobs/index.html)
- [DLT vs. Spark Structured Streaming](https://www.databricks.com/blog/2022/04/25/simplifying-streaming-data-ingestion-with-delta-live-tables.html)

## Hands-on exercise

See [`exercises/`](exercises/) — a DLT pipeline notebook to upload to Databricks.

Rebuild your Module 3 Bronze → Silver → Gold as a single DLT pipeline. Compare
the code size. Then introduce a bad reading and watch the quality dashboard track it.

## What to write on your blog

Count the lines of code you deleted when moving from Module 3's manual scripts to
DLT. What did you give up (portability, control)? What did you gain (quality tracking,
retries, ordering)? That trade-off is the real story.
