---
title: "Exercises: Delta Live Tables"
summary: "Convert your Module 3 medallion pipeline into a declarative DLT pipeline with quality expectations, then watch the quality dashboard track a deliberately bad reading"
weight: 50
type: exercise
tags:
  - dlt
  - exercises
  - databricks
  - quality-expectations
---

## DLT pipeline notebook (Databricks)

This exercise runs on Databricks -- DLT pipelines cannot execute locally. You will upload a notebook, attach it to a DLT pipeline, and see the declarative model in action.

The exercise file is at [`modules/04-delta-live-tables/exercises/04_dlt_pipeline.py`](https://github.com/dvhthomas/learn-databricks/tree/main/modules/04-delta-live-tables/exercises/04_dlt_pipeline.py).

### Setup

1. Open your Databricks workspace (Community Edition works for this exercise)
2. Upload `04_dlt_pipeline.py` as a notebook
3. Run the **setup cell** (the first code cell) on a regular cluster to generate test data in DBFS at `/tmp/sensor-raw/`
4. Create a DLT pipeline: **Workflows > Delta Live Tables > Create Pipeline**
5. Attach the notebook and configure the pipeline to use Unity Catalog (if available) or the legacy Hive Metastore

### What you'll do

The notebook has `# TODO` markers. Fill them in to complete the pipeline:

1. **Bronze table:** Configure Auto Loader (`cloudFiles`) to read JSON from `/tmp/sensor-raw/` with the provided schema hint. This is the streaming ingestion step.

2. **Silver table:** Add two `@dlt.expect_or_drop` decorators:
   - `"valid_temperature"` -- value must be between -50 and 100
   - `"sensor_id_present"` -- sensor_id must not be null
   
   Also cast the timestamp string to a proper timestamp type.

3. **Gold table:** Read from Silver using `dlt.read()` (batch, not stream). Group by sensor_id and hour, then aggregate: `avg_temp_c`, `max_temp_c`, `reading_count`.

### After the pipeline runs

1. **Check the quality dashboard.** Click the Silver table node in the pipeline graph. How many rows were dropped? The test data includes one reading with `value=999.9` -- it should be caught by `valid_temperature`.

2. **Explore the lineage graph.** The pipeline UI shows Bronze flowing to Silver flowing to Gold. This dependency was inferred from your `dlt.read()` and `dlt.read_stream()` calls -- you did not specify it.

3. **Compare with Module 3.** Open `modules/03-medallion-architecture/exercises/medallion.py` side by side. Count what you deleted: checkpoint management, explicit write operations, scheduling logic, error handling. Count what you gained: quality expectations, automatic dependency resolution, incremental processing.

4. **Test incremental processing.** Run the setup cell again to generate `batch_002.json`, then re-run the pipeline. Notice that only the new data is processed through Bronze and Silver. DLT tracked the checkpoint automatically.

5. **Introduce a systemic failure.** Add a reading with a timestamp in the year 2030. Add an `@dlt.expect_or_fail("no_future_timestamps", "ts <= current_timestamp()")` expectation to Silver. Re-run and watch the pipeline halt. Read the error message -- it tells you exactly which expectation failed and on which row.
