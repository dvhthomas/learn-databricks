---
title: "Exercises: MLflow and the AI Platform"
summary: "Track experiments, register models, and explore the model lifecycle — first locally, then on Databricks"
weight: 50
type: exercise
---

## Exercise 1: MLflow locally (no Databricks needed)

This exercise runs entirely on your machine. You'll train an anomaly detection model on sensor data, track the experiment in MLflow, and register the best model.

**Setup:**

```sh
cd modules/07-mlflow-and-ai/exercises
uv run python mlflow_local.py
```

Then open the MLflow UI:

```sh
uv run mlflow ui
open http://localhost:5000
```

### What to do

The exercise file has `# TODO` markers. Work through them in order:

1. **Log parameters** — uncomment and complete the `mlflow.log_param()` calls for each hyperparameter
2. **Log metrics** — compute precision, recall, and F1 using sklearn's metrics, then log them with `mlflow.log_metric()`
3. **Log the model artifact** — uncomment `mlflow.sklearn.log_model()` to save the trained model
4. **Log a summary** — uncomment `mlflow.log_dict()` to save a JSON summary as an artifact
5. **Register the best model** — uncomment the `mlflow.register_model()` call to register the contamination=0.10 model

### What to observe in the MLflow UI

After running the script, open `http://localhost:5000` and find:

- [ ] The "sensor-anomaly-detection" experiment with three runs
- [ ] Compare the runs side by side — which contamination value had the best F1 score?
- [ ] Click into a run and find: logged parameters, metrics, and the model artifact
- [ ] Open the "isolation-forest" artifact — it's a serialized sklearn model with a `conda.yaml` and `MLmodel` file
- [ ] Find the registered model under the "Models" tab

### Things to think about

- The model artifact includes `conda.yaml` and `requirements.txt`. Why does MLflow save the environment alongside the model?
- If you ran this script again with `random_state=None` instead of `42`, the results would change. How does this affect reproducibility?
- MLflow automatically logged the git commit hash (check the run's "Tags" section). Why does this matter when debugging a production model?
- The Model Registry has lifecycle stages (None, Staging, Production, Archived). Who in the wind utility should approve the transition from Staging to Production? What should they check?

## Exercise 2: MLflow on Databricks (requires workspace)

Upload `modules/07-mlflow-and-ai/exercises/07_mlflow_databricks.py` to a Databricks workspace as a notebook (File > Import).

This exercise does the same anomaly detection experiment but uses:

- The managed MLflow tracking server (no local `mlruns/` directory)
- Unity Catalog for model registration (if available)
- Databricks-native experiment UI

### What to do

1. Run the notebook cells in order
2. Complete the `# TODO` sections:
   - Log the model with `mlflow.sklearn.log_model()` and include an `input_example`
   - Register the best model using `mlflow.register_model()`
3. If you have a Gold table from earlier modules, replace the synthetic data with `spark.table("learning.sensors.gold_hourly_stats")`

### What to observe

- [ ] Left sidebar > Experiments — find your experiment
- [ ] Compare the three runs in the Databricks experiment UI
- [ ] Left sidebar > Models — find the registered model (if you completed the registration)
- [ ] Notice that the experiment shows which notebook created which run (lineage)
- [ ] Notice that `mlflow.get_tracking_uri()` returns `"databricks"` — the tracking server is managed for you

### The key difference from local

On your laptop, MLflow stored everything in a `./mlruns/` directory. On Databricks, everything is stored in a managed service with enterprise governance. The code is nearly identical — the experience is very different. This is the managed platform value proposition in action.

## Exercise 3: ML platform cost model (CalcMark)

The vibration model works. Now the question every stakeholder asks: **what does it cost to run in production?**

This exercise is a CalcMark cost model that compares three paths for deploying the bearing failure prediction model: Databricks AI, AWS SageMaker, and DIY (MLflow OSS on cloud VMs).

**Run it:**

```sh
cd modules/07-mlflow-and-ai/exercises
cm eval ml-platform-costs.cm -v
```

### What the model covers

- **Weekly retraining** on a GPU node (6 hours/week on 50 GB of features)
- **Real-time serving** at 500 predictions/hour (one per turbine per hour, 24/7)
- **Experiment tracking**, feature stores, and model monitoring on each platform
- **The hidden cost of DIY** — 5 services to maintain, 10 hours/month of ops work
- **Time to first production model** — Databricks (1-2 weeks) vs. SageMaker (3-4 weeks) vs. DIY (4-8 weeks)

### What to think about

- Databricks bundles MLflow tracking and Lakehouse Monitoring at no extra charge. How does that change the comparison if you are already on the platform vs. starting fresh?
- The DIY path has the lowest infrastructure bill but the highest labor cost. At what team size does that trade-off flip?
- Change `training_hours_per_run = 12` and rerun. What happens if you move from a simple Isolation Forest to a hyperparameter-tuned ensemble?
- SageMaker's serving endpoint (ml.t2.medium) costs less than Databricks Model Serving. But what does it cost to move the feature data from Delta to S3 every time you retrain?

### The interview angle

> "Your wind utility's CFO asks why the ML platform costs $1,500/month when the data scientist could just run the model on their laptop. What do you say?"

The cost model gives you the numbers. The answer is about risk: every week without automated bearing failure alerts is a week of undetected $500K failures. The platform cost is a rounding error next to the risk it mitigates.
