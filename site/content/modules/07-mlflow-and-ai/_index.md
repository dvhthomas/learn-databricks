---
title: "Module 7: MLflow and the AI Platform"
summary: "Your vibration model predicted bearing failure in the notebook. In production it missed 3 failures. Nobody can explain what changed."
status: in-progress
weight: 7
tags:
  - mlflow
  - model-registry
  - mosaic-ai
  - feature-store
  - model-serving
  - predictive-maintenance
prerequisites:
  - 1
  - 2
  - 5
last_refreshed: "2026-04-08"
---

Your wind utility's data science team built a vibration model that predicts bearing failure 48 hours in advance. In the notebook, it worked beautifully — 94% recall on the test set. They deployed it to production. In the first quarter, it missed 3 bearing failures that led to $2M in unplanned maintenance. The model also flagged 200 false alarms, each of which sent a technician to a remote turbine site for nothing.

The team can't explain what went wrong because they can't answer basic questions: Which version of the model is running in production? What training data was it built on? Did someone retrain it with different features? Were the input distributions in production different from training?

**MLflow solves the reproducibility crisis for ML.** It tracks experiments, logs parameters and metrics, versions models, and manages the lifecycle from notebook to production. On Databricks, MLflow integrates with Unity Catalog so model governance follows the same rules as data governance — who can deploy a model to production, what data it was trained on, and when it was last validated.

This module doesn't require you to be a data scientist. You need to understand the ML *workflow* well enough to advise on it, spot problems, and connect it to the governance story you already know from Unity Catalog.

Databricks is repositioning from "data platform" to "AI platform" — the thesis is that your AI needs your data, your data is governed in Databricks, therefore Databricks is where your AI should live. Understanding this argument — and its weaknesses — matters for senior technical roles. The Mosaic AI acquisition (2023) and the competitive landscape with Snowflake Cortex are part of that story.

## Prerequisites

Complete [Module 5: Unity Catalog]({{< ref "05-unity-catalog" >}}). Model governance extends data governance — you need to understand the catalog structure first.

## Exercises

Exercises live in [`modules/07-mlflow-and-ai/exercises/`](https://github.com/dvhthomas/learn-databricks/tree/main/modules/07-mlflow-and-ai/exercises). You'll track an experiment, register a model, and explore the model lifecycle from training to production.
