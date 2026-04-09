---
title: "Module 4: Delta Live Tables"
summary: "Your medallion pipeline breaks at 3am and nobody knows which step failed or what data was affected. What if you declared the outcome instead of coding every step?"
status: planned
weight: 4
tags:
  - delta-live-tables
  - declarative-pipelines
  - lakeflow
  - data-quality
  - dlt
prerequisites:
  - 1
  - 2
  - 3
last_refreshed: "2026-04-08"
---

In Module 3, you built a medallion pipeline by hand — Python scripts that read Bronze, clean to Silver, and aggregate to Gold. It works. But in production at the wind utility, that pipeline runs every 10 minutes, 24/7. When it fails at 3am because a weather station sent malformed JSON, nobody knows which step failed, what data was affected, or whether the Silver table is now inconsistent.

You also can't answer a simple question: "What percentage of our SCADA readings passed quality checks this month?" The compliance team needs that number. Your hand-coded pipeline doesn't track it.

**Delta Live Tables (DLT) — now called Lakeflow Spark Declarative Pipelines — shifts from imperative to declarative.** Instead of writing the orchestration (read this, transform that, write here, handle errors), you describe the datasets you want and the quality rules they must satisfy. The engine figures out execution order, handles retries, and tracks data quality metrics automatically.

The name change is recent (2025), and the DLT → Lakeflow Declarative Pipelines transition is still in progress. The underlying concepts are the same, but the API surface is evolving — `import dlt` is becoming `from pyspark import pipelines`. This module teaches the concepts that are stable and flags what's in transition.

For enterprise buyers, the data quality tracking (`@dlt.expect`) is often more valuable than the pipeline automation itself. Being able to tell a NERC auditor "our Silver turbine data has a 99.7% validity rate this month, and here's the trend" is what compliance teams actually want.

## Prerequisites

Complete [Module 3: Medallion Architecture]({{< ref "03-medallion-architecture" >}}). You need to have built the medallion pipeline manually to appreciate what DLT automates.

## Exercises

Exercises live in [`modules/04-delta-live-tables/exercises/`](https://github.com/dvhthomas/learn-databricks/tree/main/modules/04-delta-live-tables/exercises). You'll convert the hand-coded medallion pipeline into a declarative DLT pipeline with quality expectations.
