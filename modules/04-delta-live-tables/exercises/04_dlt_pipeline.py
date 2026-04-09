# Databricks notebook source
# Upload to Databricks and attach to a DLT pipeline (not a regular cluster).
# Delta Live Tables > Create Pipeline > select this notebook.

# COMMAND ----------
# MAGIC %md
# MAGIC # Module 4: Delta Live Tables Pipeline
# MAGIC
# MAGIC This notebook is the DLT version of the Module 3 medallion.py script.
# MAGIC Compare them side by side when you're done.
# MAGIC
# MAGIC **Before running:** generate some test data by running the cell below once
# MAGIC *outside* the pipeline (on a regular cluster), then switch to the DLT pipeline.

# COMMAND ----------

# Run this cell ONCE on a regular cluster to create test data in DBFS.
# Do NOT include this in the DLT pipeline — it's just setup.

import json
import random
from datetime import UTC, datetime, timedelta

readings = []
base = datetime(2024, 11, 18, 10, 0, 0, tzinfo=UTC)
for i in range(200):
    readings.append({
        "sensor_id": f"sensor_{random.randint(1, 5):04d}",
        "value": round(random.gauss(25.0, 8.0), 2),
        "units": "degrees_c",
        "timestamp": (base + timedelta(seconds=i * 30)).isoformat(),
    })

# Add one obviously bad reading
readings.append({
    "sensor_id": "sensor_0001",
    "value": 999.9,
    "units": "degrees_c",
    "timestamp": base.isoformat(),
})

dbutils.fs.put("/tmp/sensor-raw/batch_001.json",
               "\n".join(json.dumps(r) for r in readings),
               overwrite=True)
print(f"Wrote {len(readings)} readings to /tmp/sensor-raw/batch_001.json")

# COMMAND ----------
# MAGIC %md
# MAGIC ## The DLT Pipeline
# MAGIC
# MAGIC The cells below define the pipeline. Run them via the DLT pipeline UI,
# MAGIC not directly on a cluster.

# COMMAND ----------

import dlt
from pyspark.sql import functions as F
from pyspark.sql.types import (
    DoubleType,
    StringType,
    StructField,
    StructType,
)

RAW_PATH = "/tmp/sensor-raw/"

# COMMAND ----------
# MAGIC %md
# MAGIC ### Bronze: raw ingestion

# COMMAND ----------

@dlt.table(
    comment="Raw sensor readings as JSON, exactly as received. Append-only.",
    table_properties={"quality": "bronze"},
)
def bronze_sensor_readings():
    # TODO: Read from RAW_PATH using Auto Loader (cloudFiles format)
    # Schema: sensor_id (string), value (double), units (string), timestamp (string)
    # Use spark.readStream with format("cloudFiles")
    schema = StructType([
        StructField("sensor_id", StringType()),
        StructField("value", DoubleType()),
        StructField("units", StringType()),
        StructField("timestamp", StringType()),
    ])
    return (
        spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "json")
        # TODO: add schema hint
        .load(RAW_PATH)
    )

# COMMAND ----------
# MAGIC %md
# MAGIC ### Silver: validation and typing

# COMMAND ----------

@dlt.table(
    comment="Validated readings. Bad rows tracked in quality metrics, not silently dropped.",
    table_properties={"quality": "silver"},
)
# TODO: Add two @dlt.expect_or_drop decorators:
#   1. "valid_temperature" — value must be between -50 and 100
#   2. "sensor_id_present" — sensor_id must not be null
def silver_sensor_readings():
    return (
        dlt.read_stream("bronze_sensor_readings")
        # TODO: Cast timestamp string to proper timestamp type
        # TODO: Add processed_at column with current_timestamp()
        .withColumn("processed_at", F.current_timestamp())
    )

# COMMAND ----------
# MAGIC %md
# MAGIC ### Gold: hourly aggregates

# COMMAND ----------

@dlt.table(
    comment="Hourly temperature statistics per sensor. Business-ready.",
    table_properties={"quality": "gold"},
)
def gold_sensor_hourly_stats():
    # TODO: Read from silver (batch, not stream — Gold is recomputed)
    # Group by sensor_id and hour (date_trunc "hour" on timestamp)
    # Aggregate: avg_temp_c, max_temp_c, reading_count, warning_count (>35), critical_count (>40)
    return (
        dlt.read("silver_sensor_readings")
        # TODO: groupBy and agg
    )

# COMMAND ----------
# MAGIC %md
# MAGIC ## After the pipeline runs
# MAGIC
# MAGIC 1. Click the pipeline graph — find the quality metrics for silver_sensor_readings.
# MAGIC    How many rows were dropped? Why?
# MAGIC
# MAGIC 2. Click on a table node — find the lineage showing Bronze → Silver → Gold.
# MAGIC
# MAGIC 3. Compare this notebook to modules/03-medallion-architecture/exercises/medallion.py.
# MAGIC    What did you delete? What does DLT now own?
# MAGIC
# MAGIC 4. Add a second batch of data (run the setup cell again with batch_002.json)
# MAGIC    and re-run the pipeline. Notice that only new data is processed — DLT
# MAGIC    handles incremental processing automatically.
