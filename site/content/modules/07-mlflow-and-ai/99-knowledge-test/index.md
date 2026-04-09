---
title: "Knowledge Test: MLflow and the AI Platform"
summary: "Validate your understanding of ML reproducibility, MLflow tracking, the model lifecycle, and the Databricks AI platform"
weight: 99
type: test
tags:
  - mlflow
  - model-registry
  - mosaic-ai
  - feature-store
  - predictive-maintenance
  - platform-comparison
---

## Oral questions

Answer these out loud or in chat. Aim for 2-3 sentences per answer — enough to show you understand, not a lecture.

**Must know cold:**

1. Your wind utility's vibration model had 94% recall in the notebook but missed 3 bearing failures in production. Walk me through the four most likely root causes — and for each one, what specific MLflow feature would have caught it.

2. What are the four things MLflow tracks for every run? Give a concrete example of each one using the vibration model scenario.

3. Explain the model lifecycle stages (None, Staging, Production, Archived). Who in the wind utility should approve each transition, and what should they verify?

4. Your utility's NERC compliance officer asks: "How do we prove which model generated the maintenance dispatch that cost us $200,000?" What is your answer, assuming MLflow and Unity Catalog are in use?

5. A customer says "MLflow is open source and free — why would I pay Databricks for it?" Give an honest answer that acknowledges what standalone MLflow can do while explaining what the managed version adds.

6. Explain the Databricks AI platform thesis in two sentences. Then give one area where the thesis is strong and one where it's a stretch.

**Know the shape:**

7. What is a Feature Store and why does it matter for the vibration model? What specific failure from Lecture 1 does it prevent? (Two sentences is fine.)

8. What is the difference between Snowflake Cortex and Databricks AI? When would you recommend each? (Three sentences maximum.)

9. What is the AI Gateway and why would a NERC-regulated utility care about it? (Two sentences.)

## Code challenge

Complete the `# TODO` sections in `modules/07-mlflow-and-ai/exercises/mlflow_local.py` and run it:

```sh
cd modules/07-mlflow-and-ai/exercises
uv run python mlflow_local.py
uv run mlflow ui
```

You should be able to:

- [ ] Explain what each section of the script does before running it
- [ ] Find the three runs in the MLflow UI and compare their metrics
- [ ] Identify which contamination value produced the best F1 score and explain why
- [ ] Find the registered model in the Models tab
- [ ] Open a model artifact and explain what `MLmodel`, `conda.yaml`, and the pickle file are for
- [ ] Explain why MLflow saves the environment spec alongside the model

## The interview question

Practice this answer until it's fluent (under 90 seconds):

> "Your wind utility's vibration model keeps producing different results in production vs. the notebook. What's the root cause and how does Databricks help?"

A good answer covers: the root cause is the absence of systematic tracking between experimentation and production — different data versions, different feature computation, unknown model versions, and input drift. MLflow solves this by tracking parameters, metrics, artifacts, and code version for every training run. The Model Registry in Unity Catalog manages the lifecycle from experiment to production, with the same governance (access control, lineage, audit trails) that applies to your data. Feature Store eliminates training-serving skew by serving the same computed features to both training and inference. The managed platform means the tracking server, serving infrastructure, and governance integration are handled for you — your team focuses on the model, not the plumbing.

## The whiteboard test

This is the capstone assessment for the entire curriculum. Draw the wind utility's full data platform from memory, covering:

- **Where does data come from?** (SCADA sensors, weather stations, SAP maintenance records)
- **How does it get ingested?** (Kafka/Event Hubs for streaming, Auto Loader for batch)
- **Where does it land?** (Object storage + Delta Lake)
- **How is it structured?** (Medallion: Bronze raw, Silver cleaned, Gold business-ready)
- **How are pipelines managed?** (DLT / Lakeflow Declarative Pipelines)
- **Who governs it?** (Unity Catalog — three-level namespace, CEII access, lineage, audit)
- **Who queries it?** (DBSQL + Photon for analysts, notebooks for engineers)
- **How is ML tracked?** (MLflow experiments, Model Registry in Unity Catalog)
- **How are models served?** (Model Serving endpoints for real-time predictions)
- **How are LLMs governed?** (AI Gateway for rate limiting, audit, guardrails)

If you can draw this in 3 minutes with reasonable accuracy, you've internalized the platform architecture. If you get stuck, review the module that covers the missing component.

## The customer scenario test

Read this scenario cold, then answer without preparation:

> "A solar farm operator has 3 years of inverter telemetry in S3 as CSV files. They have a data engineering team of 3, a data science team of 2, and 12 SQL analysts. They're currently using Redshift for analytics and cron jobs running Python scripts for data prep. They want to 'modernize their data platform.' What do you recommend?"

A strong answer includes:

- Migration approach (don't rip-and-replace — phase it)
- Delta Lake for storage (convert CSVs, get ACID, schema enforcement, time travel)
- Medallion for structure (Bronze raw CSVs, Silver cleaned, Gold analyst-ready)
- Unity Catalog for governance (especially if they have NERC/FERC requirements)
- DBSQL for the 12 analysts (their biggest pain point — consistent, governed queries)
- An honest discussion of scale: with 3 data engineers and 2 data scientists, they may not need the full Databricks platform. DuckDB + dbt for the data engineering, a simpler ML setup for the data science team, and governed SQL access could work at their scale. Over-engineering is a real risk.
- What *not* to do: don't spin up the full Databricks stack for a 3-person team unless the governance requirements demand it

## The "why not Snowflake?" test

> "This customer is also evaluating Snowflake. Make the case for Databricks, then steelman the case for Snowflake."

**For Databricks:** Unified platform — data engineering, ML, and analytics in one place. Open formats (Delta/Parquet) avoid lock-in. Stronger ML story (MLflow, Feature Store, Model Serving) for the data science team. Better streaming support for real-time telemetry.

**For Snowflake:** Simpler for the 12 SQL analysts — Snowflake's SQL experience is more mature. Cortex gives them AI-in-SQL without Python. Easier to administer for a small team. Snowflake's concurrency scaling is more straightforward for BI workloads. If the ML use cases are simple (anomaly detection via Cortex, not custom model training), Snowflake might serve 14 of their 17 people better.

You should be able to make both cases without prompting.
