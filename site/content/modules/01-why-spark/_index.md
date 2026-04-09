---
title: "Module 1: Why Spark Exists"
summary: "What problem does distributed compute solve, and when do you actually need it?"
status: planned
weight: 1
tags:
  - spark
  - distributed-compute
  - databricks
prerequisites: []
last_refreshed: ""
---

This module answers a deceptively simple question: **why does Apache Spark exist?**

Not "what is Spark" — you can read the docs for that. But why did an entire ecosystem grow up around the idea of splitting computation across dozens or hundreds of machines? What was breaking before Spark, what alternatives exist today, and when is Spark genuinely the right tool versus an expensive distraction?

By the end of this module you should be able to explain — to an engineer, to a VP, to yourself — when distributed compute makes sense, when it doesn't, and what Databricks adds on top of Spark that justifies its existence.

## Prerequisites

None. This is where you start.

## Exercises

Exercises for this module live in [`modules/01-why-spark/exercises/`](https://github.com/dvhthomas/learn-databricks/tree/main/modules/01-why-spark/exercises). You'll run the same sensor data aggregation in DuckDB and PySpark, then examine what Spark actually did under the hood.
