# learn-databricks

Hands-on learning curriculum for Databricks and the modern data lakehouse ecosystem.
Goal: practical, industry-ready knowledge of data platforms — credible enough to
hold your own in technical conversations with engineers and architects.

**Not theoretical.** Every module produces working code and tested understanding.

## Prerequisites

- [sensor-analytics](https://github.com/dvhthomas/sensor-analytics) — the project
  that evolves across modules. Clone it alongside this repo.
- [Databricks Community Edition](https://community.cloud.databricks.com/) — free,
  no credit card. Needed from Module 1.
- [Databricks free trial](https://www.databricks.com/try-databricks) — 14 days,
  needed for Modules 5–7 (Unity Catalog requires a full workspace).
- [uv](https://docs.astral.sh/uv/) for Python dependency management.

## Modules

| # | Module | Status | Blog post |
|---|--------|--------|-----------|
| 1 | [Why Spark Exists](modules/01-why-spark/) | planned | |
| 2 | [Delta Lake: ACID on Files](modules/02-delta-lake/) | planned | |
| 3 | [Medallion Architecture](modules/03-medallion-architecture/) | planned | |
| 4 | [Delta Live Tables](modules/04-delta-live-tables/) | planned | |
| 5 | [Unity Catalog](modules/05-unity-catalog/) | planned | |
| 6 | [Databricks SQL](modules/06-databricks-sql/) | planned | |
| 7 | [MLflow and the AI Platform](modules/07-mlflow-and-ai/) | planned | |

Update status (`planned` → `in-progress` → `done`) and add blog post links as you go.

## Running exercises locally

```sh
uv sync
uv run python modules/02-delta-lake/exercises/delta_writer.py
```

Modules 1, 4, 5, and 6 require Databricks — exercises for those modules include
notebooks to upload rather than scripts to run locally.

## Working with an AI agent

This repo includes `AGENTS.md` — instructions for Claude (or any AI agent) on how
to help you work through each module, populate exercises, and run validation.

When starting a module: "Let's work on module 2."
When finishing a module: "Validate module 2 with me."

## Data

Sample sensor data lives in `data/`. See `data/README.md` for instructions on
generating more using the sensor-analytics project.
