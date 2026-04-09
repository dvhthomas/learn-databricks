---
title: "Module 2: Delta Lake"
summary: "Two teams wrote to the same Parquet directory and corrupted your turbine data. How do you make storage reliable?"
status: in-progress
weight: 2
tags:
  - delta-lake
  - acid
  - transaction-log
  - parquet
  - iceberg
prerequisites:
  - 1
last_refreshed: "2026-04-08"
---

Your sensor-analytics system writes raw Parquet files to disk. That works when one process writes and one person reads. Now imagine the wind utility version: a SCADA ingestion pipeline writes turbine telemetry every 10 minutes. A separate pipeline appends weather data hourly. An ETL job backfills corrected readings from field calibrations. And 15 analysts query the same directory throughout the day.

**What goes wrong?**

A writer crashes halfway through a batch — you get partial files that silently corrupt downstream aggregates. Two pipelines write at the same time — one overwrites the other's files. An analyst queries during a write and gets inconsistent results. A field engineer accidentally deletes last month's vibration data. Nobody notices until the quarterly compliance report doesn't add up.

These aren't edge cases. They're Tuesday.

Delta Lake solves this by putting a **transaction log** on top of Parquet files — turning a pile of files into a proper table with ACID guarantees, schema enforcement, and time travel. This module makes that concrete: you'll read the actual `_delta_log/` JSON files, trigger a schema enforcement error, and travel back in time to recover deleted data.

You'll also understand how Delta compares to Apache Iceberg — particularly relevant since Databricks acquired Tabular (the company behind Iceberg) in 2024 and is working toward format interoperability through Delta Lake UniForm.

## Prerequisites

Complete [Module 1: Why Spark Exists]({{< ref "01-why-spark" >}}).

## Exercises

Exercises live in [`modules/02-delta-lake/exercises/`](https://github.com/dvhthomas/learn-databricks/tree/main/modules/02-delta-lake/exercises). You'll write sensor data to Delta format, inspect the transaction log, and see ACID guarantees in action.
