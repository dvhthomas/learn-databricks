---
title: "Module 1: Why Spark Exists"
summary: "You built sensor-analytics on one machine. Now scale it to 500 wind turbines across 3 regions — what infrastructure decisions do you face, and where does Spark fit?"
status: in-progress
weight: 1
tags:
  - spark
  - distributed-compute
  - databricks
  - production-architecture
  - kafka
  - iot
prerequisites: []
last_refreshed: "2026-04-08"
---

You built [sensor-analytics](https://github.com/dvhthomas/sensor-analytics) in a few hours. It has TCP collectors, a Redis queue, a Parquet writer, DuckDB for analysis, and a Flask dashboard. It simulates 50 sensors on one machine. It works.

Now imagine it's real. You're the data platform team for a regional wind utility — 500 turbines across 3 states, each with 50+ SCADA sensors reporting every 10 minutes. That's roughly 3.6 million readings per day of standard telemetry, plus burst vibration data, weather feeds from 12 stations, grid operator signals, and maintenance records from SAP.

**What breaks first?** Not the query engine — the volume is only a few GB/day. What breaks is everything around it: Redis loses data on restart and takes your buffer with it. Local Parquet files can't be shared across teams. Two pipeline runs write to the same directory and corrupt each other. A field engineer deletes last week's readings by accident. NERC auditors ask who has access to grid operations data and you can't answer.

This module maps the full landscape of infrastructure decisions you'd face — ingestion, storage, compute, serving, and governance — and shows where Apache Spark and Databricks fit in that picture. Spark is one piece, not the whole answer. Knowing which piece it is, and when you actually need it, is more valuable than knowing its API.

## Prerequisites

None. This is where you start. Familiarity with [sensor-analytics](https://github.com/dvhthomas/sensor-analytics) helps but isn't required.

## Exercises

Exercises for this module live in [`modules/01-why-spark/exercises/`](https://github.com/dvhthomas/learn-databricks/tree/main/modules/01-why-spark/exercises). You'll run the same sensor data aggregation in DuckDB and PySpark, then examine what Spark actually did under the hood.
