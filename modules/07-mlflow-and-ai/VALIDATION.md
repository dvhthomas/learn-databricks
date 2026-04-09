# Module 7 Validation: MLflow and the AI Platform

---

## Oral questions

**Must know cold:**

1. What does MLflow track in an experiment run? List four things that are
   recorded, and explain why each matters for reproducibility.

2. What is the Model Registry and what problem does it solve? Walk me through
   the lifecycle of a model from experiment to production.

3. A customer's data science team says their models keep producing different
   results and they don't know why. What's the root cause, and how does
   MLflow help?

4. The Databricks pitch is "your AI should be where your data is." Explain
   that argument in two sentences, then tell me its biggest weakness.

5. When would you recommend a customer use Databricks' AI platform vs. a
   dedicated ML platform like SageMaker or Vertex AI?

**Know the shape:**

6. What is Vector Search in Databricks, and what type of application needs it?
   (RAG is the answer — explain what RAG means without jargon.)

7. What is AI Gateway and why does a large enterprise care about it?

8. A SQL analyst asks if they can call an LLM from a SQL query in Databricks.
   What's the answer, and what's the function they'd use?

---

## Code challenge

Run the local MLflow exercise:

```sh
uv run python modules/07-mlflow-and-ai/exercises/mlflow_local.py
```

Then open the MLflow UI:

```sh
uv run mlflow ui
# open http://localhost:5000
```

You should be able to:

- [ ] Find the experiment in the MLflow UI and compare the three runs
- [ ] Explain what each logged parameter and metric represents
- [ ] Identify which run had the best precision/recall balance and explain why
- [ ] Find the registered model in the Model Registry (local)
- [ ] Explain what "promoting to Production" means and why it requires a human decision

Bonus: upload `exercises/07_mlflow_databricks.py` to Databricks and run it against
your Gold table from Unity Catalog. Verify the run appears in the managed MLflow UI.

---

## The final interview question: The Whiteboard Test

This is the job-readiness test. Draw the Databricks architecture from memory:

```
[ object storage (S3/ADLS/GCS) ]
          ↓
    [ Delta Lake ]  ← transaction log, ACID, time travel
          ↓
  Bronze → Silver → Gold  ← medallion architecture
   (DLT pipeline, @dlt.expect quality tracking)
          ↓
  [ Unity Catalog ]  ← governance, lineage, audit
          ↙           ↘
[ DBSQL + BI tools ]  [ ML notebooks + MLflow ]
                              ↓
                      [ Model Registry ]
                              ↓
                      [ Model Serving ]
```

You should be able to label every box, explain what problem it solves, and name
one specific competing approach for each layer (Iceberg, dbt, Snowflake, Airflow,
SageMaker).

---

## Done when

- [ ] All oral questions answered without significant prompting
- [ ] MLflow local exercise complete and UI explored
- [ ] Architecture diagram drawn from memory with all layers labeled
- [ ] Module status updated to `done` in repo README
- [ ] Ready for the job-readiness assessment in AGENTS.md
