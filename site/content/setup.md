---
title: "Setup Guide"
summary: "Get your machine ready to run exercises"
weight: 1
---

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- Git

That's it.

## Mac

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and sync
git clone https://github.com/dvhthomas/learn-databricks.git
cd learn-databricks
uv sync
```

## Linux

Same as Mac:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone https://github.com/dvhthomas/learn-databricks.git
cd learn-databricks
uv sync
```

## Run an exercise

```bash
uv run python modules/02-delta-lake/exercises/delta_writer.py
```

## Run the tutorial site

```bash
cd site && uv run hugo server --buildDrafts
```

## Databricks modules

Modules 1, 4, 5, and 6 run in Databricks notebooks, not locally. You'll need:

- [Databricks Community Edition](https://community.cloud.databricks.com/) (free) for Module 1
- [Databricks free trial](https://www.databricks.com/try-databricks) (14 days) for Modules 4-7
