# Module 7: MLflow and the AI Platform

**Status:** planned  
**Databricks environment:** Free trial workspace  
**Local code:** yes — `uv run python exercises/mlflow_local.py` (MLflow runs locally too)

## The question this module answers

Your data pipeline is solid. Now the data science team wants to train anomaly
detection models on the Gold table, track which model is in production, and
explain to the compliance team why the model made a given decision. How does
Databricks serve them — and how does this connect to everything you've built?

## Core concepts

### MLflow: the ML lifecycle standard

MLflow is an open-source ML lifecycle platform that Databricks created in 2018.
It's become a de facto standard even outside Databricks. Four components:

**Tracking** — log parameters, metrics, and artifacts for every training run:
```python
with mlflow.start_run():
    mlflow.log_param("threshold", 35.0)
    mlflow.log_metric("precision", 0.94)
    mlflow.sklearn.log_model(model, "anomaly-detector")
```

**Model Registry** — versioned, governed model store with lifecycle stages:
`None → Staging → Production → Archived`

**Projects** — reproducible ML code packaging (less commonly used in practice)

**Models** — standardized model format for deployment across frameworks

### Why MLflow matters for governance (not just ML)

The governance story for ML mirrors Unity Catalog's story for data:

- **Reproducibility:** every run has a recorded git commit, parameters, and environment
- **Auditability:** who trained this model, with what data, approved by whom?
- **Rollback:** promote model v3 back to production when v4 underperforms
- **Lineage:** which training dataset produced which model version?

A compliance team asking "how did this model make this decision?" needs MLflow's
tracking, not just the model file.

### The Databricks AI platform pivot

Databricks acquired Mosaic ML in 2023. The combined platform now offers:

- **Mosaic AI Model Training** — fine-tune open LLMs (Llama, Mistral) on your data
- **Vector Search** — similarity search on embeddings, for RAG applications  
- **AI Playground** — test and compare LLMs interactively
- **AI Gateway** — governed, rate-limited access to external LLMs (OpenAI, Anthropic)
- **AI Functions** — call LLMs directly from SQL: `SELECT ai_classify(value, ...)`

The thesis: your AI should be where your data is, governed by the same policies,
with the same lineage tracking. Running AI on a separate platform means copying
data or losing governance.

### Mosaic AI vs. Snowflake Cortex

| | Databricks Mosaic AI | Snowflake Cortex |
|---|---|---|
| Approach | Full ML lifecycle (train, track, serve) | LLM functions in SQL |
| Fine-tuning | Yes, first-class | Limited |
| Target user | ML engineers + data engineers | SQL analysts |
| Maturity | More mature (MLflow established) | Newer, evolving fast |
| Vector search | Yes | Yes (Cortex Search) |

Snowflake Cortex is more accessible to SQL-first teams. Databricks Mosaic AI is
more powerful for teams with ML engineering capability.

### What you actually need to know for the role

You're not being hired as a data scientist. But you need to:

1. Explain the ML workflow at a conceptual level: data prep → feature engineering
   → training → evaluation → deployment → monitoring
2. Recognize when a customer's ML problem is actually a data problem (most ML
   failures are data quality failures, not algorithm failures)
3. Understand MLflow's governance value for enterprise buyers
4. Have a view on when Databricks' AI platform is the right choice vs. dedicated
   ML platforms (SageMaker, Vertex AI)

## Reading

- [MLflow documentation](https://mlflow.org/docs/latest/index.html) — Tracking and Model Registry sections
- [Mosaic AI documentation](https://docs.databricks.com/en/machine-learning/index.html) — overview page
- [MLflow original announcement](https://www.databricks.com/blog/2018/06/05/introducing-mlflow-an-open-source-machine-learning-platform.html) — historical context, 5 min
- [Databricks AI Functions](https://docs.databricks.com/en/large-language-models/ai-functions.html)
- [Snowflake Cortex overview](https://docs.snowflake.com/en/user-guide/snowflake-cortex/overview) — for contrast

## Hands-on exercise

See [`exercises/`](exercises/) for two parts:

1. **`mlflow_local.py`** — run MLflow locally (no Databricks needed) to track
   anomaly detection experiments on the Gold sensor data. Demonstrates the core
   tracking workflow before you move it to Databricks.

2. **`07_mlflow_databricks.py`** — Databricks notebook version that uses the
   managed MLflow tracking server and Model Registry.

## What to write on your blog

The governance angle, not the ML tutorial. MLflow for ML is what Unity Catalog
is for data: explicit versioning, auditable lineage, reproducible outputs. That
framing resonates with non-ML leaders evaluating the platform — and it connects
everything from Module 5 onward into a coherent story.
