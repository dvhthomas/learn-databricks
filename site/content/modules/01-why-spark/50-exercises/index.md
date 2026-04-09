---
title: "Exercises: Why Spark Exists"
summary: "Compare DuckDB and Spark hands-on, then model the real costs of a wind utility data platform"
weight: 50
type: exercise
---

## Spark vs. DuckDB on sensor data

Upload `modules/01-why-spark/exercises/01_spark_vs_duckdb.py` to [Databricks Community Edition](https://community.cloud.databricks.com/) as a notebook (File > Import), then work through it:

1. Run the same hourly aggregation in both Spark and DuckDB
2. Find the shuffle stage in the Spark UI after the `groupBy`
3. Identify which operation triggered execution (the action)
4. Explain why DuckDB is faster for this dataset size

The exercise has `# TODO` markers — fill them in before running.

## Wind utility cost model (CalcMark)

The sizing model calculates how much data a 500-turbine wind utility generates, what it costs on Databricks vs. a DIY stack, and whether the platform is justified by the risk it mitigates. It's a live document — change any assumption and rerun to see how the answer changes.

**Requires [CalcMark](https://calcmark.org):** `brew install calcmark/tap/calcmark`

View the model with all computed values:

```sh
cm eval modules/01-why-spark/exercises/wind-utility-sizing.cm -v
```

Export to HTML for a formatted report:

```sh
cm convert modules/01-why-spark/exercises/wind-utility-sizing.cm --to=html -o sizing.html
open sizing.html
```

### Things to try

- Change `turbines = 500` to `turbines = 50` — how does the cost comparison shift?
- Change `sql_dbu_rate = $0.70` to `$0.22` (SQL Classic instead of Serverless) — how much does it save?
- Change `missed_per_year = 2` to `missed_per_year = 0` — does the platform still justify itself on compliance alone?
