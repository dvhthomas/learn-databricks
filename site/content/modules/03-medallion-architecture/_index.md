---
title: "Module 3: Medallion Architecture"
summary: "Field engineers want raw readings. Analysts want clean aggregates. Compliance wants an audit trail. How do you serve everyone from one copy of the data?"
status: in-progress
weight: 3
tags:
  - medallion
  - bronze-silver-gold
  - data-architecture
  - dbt
prerequisites:
  - 1
  - 2
last_refreshed: "2026-04-08"
---

Your wind utility now has reliable Delta tables. But the data is a mess — raw SCADA readings, partially cleaned aggregates, and analyst-created CSV extracts all live in the same directory. Field engineers want the raw 10-minute readings so they can see exactly what a turbine reported before a failure. Analysts want hourly averages with outliers removed. The compliance team wants an immutable record of every reading that came in, even the bad ones, because NERC auditors will ask.

Everyone needs different views of the same data. If you give each team their own copy, the copies drift. If you force everyone to use one table, the transformations live in dashboard queries and break constantly.

**The medallion architecture solves this by organizing data into layers: Bronze (raw, immutable, everything), Silver (cleaned, validated, trustworthy), and Gold (aggregated, business-ready, fast).** Every Databricks customer conversation uses this vocabulary. Every data platform job listing assumes you know it.

This module teaches the pattern through the wind utility scenario — and honestly compares it to dbt's staging/intermediate/marts pattern, which solves the same problem in a different way.

## Prerequisites

Complete [Module 2: Delta Lake]({{< ref "02-delta-lake" >}}). You need to understand Delta's ACID guarantees to see why Bronze can safely be append-only.

## Exercises

Exercises live in [`modules/03-medallion-architecture/exercises/`](https://github.com/dvhthomas/learn-databricks/tree/main/modules/03-medallion-architecture/exercises). You'll build a three-layer pipeline from raw SCADA readings to analyst-ready aggregates — and see what happens to bad readings.
