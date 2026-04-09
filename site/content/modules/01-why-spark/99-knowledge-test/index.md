---
title: "Knowledge Test: Why Spark Exists"
summary: "Validate your understanding of distributed compute, the Spark execution model, and when to use the Databricks platform"
weight: 99
type: test
tags:
  - spark
  - distributed-compute
  - databricks
  - shuffle
  - production-architecture
---

## Oral questions

Answer these out loud or in chat. Aim for 2–3 sentences per answer — enough to show you understand, not a lecture.

**Must know cold:**

1. Your wind utility has sensor-analytics running on one machine. Walk me through the first 3 things that would break as you scale to 500 turbines — and for each one, what production component replaces the toy version.

2. What is a shuffle in Spark, and why is it expensive? Give a concrete example using the wind utility scenario (e.g., joining SCADA data with weather data).

3. I have 3 years of SCADA data and I want the average gearbox temperature per turbine per month. Walk me through what Spark does when I run `groupBy("turbine_id", "month").agg(avg("value"))`. Where does the shuffle happen?

4. What's the difference between a Spark transformation and an action? Why does this distinction matter when debugging a slow job?

5. Why does Databricks exist? If Apache Spark is open source and free, what are customers paying for?

6. A data scientist says "just use DuckDB." Your wind utility has 15 analysts, NERC compliance requirements, and a predictive maintenance ML model. What do you say?

**Know the shape:**

7. What is Photon and how does it relate to Spark? What's a "vectorized shuffle"? (Two sentences is fine.)

8. What is Spark Connect and why was it introduced in Spark 4.0? (One sentence.)

9. What role does Kafka play in a production IoT data platform? How does it differ from what Redis does in sensor-analytics?

## Code challenge

Run `exercises/01_spark_vs_duckdb.py` in Databricks Community Edition:

```sh
# Upload to Databricks Community Edition as a notebook
# File > Import > select the .py file
```

You should be able to:

- [ ] Explain what each cell is doing before running it
- [ ] Find the shuffle stage in the Spark UI after running the `groupBy`
- [ ] Identify which operation triggered execution (the action)
- [ ] Explain why the DuckDB version is faster for this dataset size

## The interview question

Practice this answer until it's fluent (under 90 seconds):

> "Walk me through what happens when a Spark job runs a groupBy on a 1TB dataset across 10 executors."

A good answer covers: data is partitioned across executors → transformations are lazy (nothing runs until an action) → the `groupBy` triggers a shuffle → each executor writes its outgoing data to disk → data is repartitioned by key across the network → aggregation runs locally on each executor's partition → results are collected by the driver. Mention that AQE can dynamically adjust partition sizes and join strategies during execution.
