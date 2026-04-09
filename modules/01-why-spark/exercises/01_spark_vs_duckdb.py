# Databricks notebook source
# Upload this file to Databricks Community Edition as a notebook.
# File > Import > select this file.

# COMMAND ----------
# MAGIC %md
# MAGIC # Module 1: Spark vs. DuckDB on Sensor Data
# MAGIC
# MAGIC The same aggregation, two tools. The goal isn't to pick a winner —
# MAGIC it's to understand *why* the results differ and what that means in practice.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Setup: load sample data into a Delta table
# MAGIC
# MAGIC We'll generate synthetic sensor data directly so this notebook
# MAGIC is self-contained — no file uploads needed.

# COMMAND ----------

import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone

# Generate 10,000 readings across 50 sensors over 24 hours
# This is small enough to run in Community Edition
rng = np.random.default_rng(seed=42)
n = 10_000
sensors = [f"sensor_{i:04d}" for i in range(50)]

base_time = datetime(2024, 11, 18, 0, 0, 0, tzinfo=timezone.utc)
readings = pd.DataFrame({
    "sensor_id": rng.choice(sensors, size=n),
    "value": rng.normal(loc=25.0, scale=8.0, size=n).round(2),
    "units": "degrees_c",
    "timestamp": [
        base_time + timedelta(seconds=int(s))
        for s in rng.uniform(0, 86400, size=n)
    ],
})

print(f"Generated {len(readings):,} readings")
print(readings.head())

# COMMAND ----------
# MAGIC %md
# MAGIC ## Part 1: The Spark way

# COMMAND ----------

# Convert pandas DataFrame to Spark DataFrame
from pyspark.sql import functions as F

spark_df = spark.createDataFrame(readings)
spark_df.printSchema()

# COMMAND ----------

# TODO: Run the hourly aggregation using Spark
# Group by sensor_id and hour, compute avg and max temperature
# Hint: use F.date_trunc("hour", "timestamp") to extract the hour

hourly_stats = (
    spark_df
    # TODO: groupBy sensor_id and hour
    # TODO: agg avg("value") as avg_temp, max("value") as max_temp, count as readings
    # TODO: orderBy sensor_id, hour
)

# This line triggers execution — before this, nothing has run
hourly_stats.show(10)

# COMMAND ----------
# MAGIC %md
# MAGIC ## Examine the Spark UI
# MAGIC
# MAGIC After the cell above runs:
# MAGIC 1. Click **View** > **Spark UI** in the Databricks toolbar
# MAGIC 2. Click on the most recent job
# MAGIC 3. Find the stage that has a shuffle (look for "Exchange" in the DAG)
# MAGIC 4. Note the shuffle read/write size
# MAGIC
# MAGIC **Question:** Which operation caused the shuffle? Why?

# COMMAND ----------
# MAGIC %md
# MAGIC ## Part 2: The DuckDB way

# COMMAND ----------

# DuckDB is available in Databricks notebooks
import duckdb

# DuckDB can query a pandas DataFrame directly — no conversion needed
con = duckdb.connect()

# TODO: Write the same aggregation in SQL using DuckDB
# Query the `readings` pandas DataFrame directly (DuckDB can see it in scope)

result = con.execute("""
    SELECT
        sensor_id,
        -- TODO: truncate timestamp to hour
        -- TODO: avg(value) as avg_temp
        -- TODO: max(value) as max_temp
        -- TODO: count(*) as readings
    FROM readings
    -- TODO: GROUP BY sensor_id, hour
    -- TODO: ORDER BY sensor_id, hour
""").df()

print(result.head(10))

# COMMAND ----------
# MAGIC %md
# MAGIC ## Part 3: Compare the results
# MAGIC
# MAGIC Both queries should produce identical output.

# COMMAND ----------

# TODO: Verify the two results match
# Convert hourly_stats (Spark) to pandas and compare with result (DuckDB)
# Are the row counts the same? Are the values the same (within floating point)?

spark_result = hourly_stats.toPandas()

print(f"Spark rows: {len(spark_result)}")
print(f"DuckDB rows: {len(result)}")

# TODO: assert the counts match

# COMMAND ----------
# MAGIC %md
# MAGIC ## Reflection
# MAGIC
# MAGIC Answer these in a comment below before moving on:
# MAGIC
# MAGIC 1. Which was faster? Why?
# MAGIC 2. At what data size would Spark start to win?
# MAGIC 3. What operation caused the Spark shuffle, and why was a shuffle necessary?
# MAGIC 4. If you were advising a company with 500GB of sensor data, which tool
# MAGIC    would you recommend and why?

# COMMAND ----------

# Your answers here:
# 1.
# 2.
# 3.
# 4.
