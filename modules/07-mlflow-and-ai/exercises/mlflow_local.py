"""
Module 7: MLflow experiment tracking — local version.

Runs entirely locally. No Databricks needed for this exercise.
MLflow stores experiment data in ./mlruns/ by default.

    uv run python modules/07-mlflow-and-ai/exercises/mlflow_local.py

Then view the results:
    uv run mlflow ui
    open http://localhost:5000
"""

import json
from pathlib import Path

import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from rich.console import Console
from rich.panel import Panel
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

console = Console()


def section(title: str) -> None:
    console.print(Panel(f"[bold]{title}[/bold]", expand=False))


def load_gold_data() -> pd.DataFrame:
    """
    Simulate Gold hourly stats from our sample data.
    In production this would be: spark.table("learning.sensors.gold_hourly_stats")
    """
    raw = pd.read_json("data/sample.json")
    raw["timestamp"] = pd.to_datetime(raw["timestamp"], utc=True)
    raw["hour"] = raw["timestamp"].dt.floor("h")

    gold = (
        raw.groupby(["sensor_id", "hour"])
        .agg(
            avg_temp_c=("value", "mean"),
            max_temp_c=("value", "max"),
            min_temp_c=("value", "min"),
            reading_count=("value", "count"),
        )
        .reset_index()
    )

    # Add a synthetic "is_anomaly" label for evaluation
    # In practice you'd have human-labeled anomalies or use a threshold rule
    gold["is_anomaly"] = (gold["max_temp_c"] > 35).astype(int)

    return gold


# ---------------------------------------------------------------------------
# Section 1: Set up the experiment
# ---------------------------------------------------------------------------

section("1. Setting up MLflow experiment")

# MLflow will store runs locally in ./mlruns unless you configure a tracking server
mlflow.set_experiment("sensor-anomaly-detection")

console.print("Experiment: sensor-anomaly-detection")
console.print("Tracking URI: " + mlflow.get_tracking_uri())
console.print("(After this runs, open: uv run mlflow ui)")

gold_df = load_gold_data()
features = ["avg_temp_c", "max_temp_c", "min_temp_c", "reading_count"]
X = gold_df[features]
y = gold_df["is_anomaly"]

console.print(f"\nDataset: {len(gold_df)} hourly sensor records")
console.print(f"Anomaly rate: {y.mean():.1%}")

# ---------------------------------------------------------------------------
# Section 2: Run experiments with different hyperparameters
# ---------------------------------------------------------------------------

section("2. Running experiments — three contamination values")

# IsolationForest's `contamination` parameter = expected fraction of anomalies
# We'll try three values and compare the results in MLflow UI

contamination_values = [0.05, 0.10, 0.20]

for contamination in contamination_values:
    # TODO: Start an MLflow run with a descriptive name
    with mlflow.start_run(run_name=f"isolation_forest_c{int(contamination*100)}"):

        # TODO: Log the hyperparameters
        # mlflow.log_param("contamination", contamination)
        # mlflow.log_param("features", features)
        # mlflow.log_param("n_estimators", 100)

        # Train the model
        model = IsolationForest(
            contamination=contamination,
            n_estimators=100,
            random_state=42,
        )
        model.fit(X)

        # Predict: IsolationForest returns -1 for anomalies, 1 for normal
        raw_predictions = model.predict(X)
        predictions = (raw_predictions == -1).astype(int)  # 1=anomaly, 0=normal

        # TODO: Log metrics
        # Compute precision, recall, and F1 against our labeled anomalies
        # Use sklearn.metrics.classification_report or precision_score / recall_score
        # mlflow.log_metric("precision", ...)
        # mlflow.log_metric("recall", ...)
        # mlflow.log_metric("f1", ...)
        # mlflow.log_metric("predicted_anomaly_rate", predictions.mean())

        anomaly_count = predictions.sum()
        console.print(
            f"contamination={contamination}: "
            f"{anomaly_count} anomalies detected "
            f"({predictions.mean():.1%} of records)"
        )

        # TODO: Log the trained model as an artifact
        # mlflow.sklearn.log_model(model, "isolation-forest")

        # Log a simple text summary as a custom artifact
        summary = {
            "contamination": contamination,
            "anomalies_detected": int(anomaly_count),
            "anomaly_rate": float(predictions.mean()),
        }
        # TODO: log summary as a JSON artifact
        # mlflow.log_dict(summary, "run_summary.json")

# ---------------------------------------------------------------------------
# Section 3: Register the best model
# ---------------------------------------------------------------------------

section("3. Registering the best model")

# In a real workflow, you'd use the MLflow UI to compare runs and pick the best one.
# Here we'll register the model from the run with contamination=0.10 as our "best."

# TODO: Find the run with contamination=0.10 and register its model
# Hint: use mlflow.search_runs() to find the run, then mlflow.register_model()

runs = mlflow.search_runs(
    experiment_names=["sensor-anomaly-detection"],
    filter_string="params.contamination = '0.1'",
)

if not runs.empty:
    best_run_id = runs.iloc[0]["run_id"]
    console.print(f"Best run ID: {best_run_id}")

    # TODO: Register the model from this run
    # model_uri = f"runs:/{best_run_id}/isolation-forest"
    # registered = mlflow.register_model(model_uri, "sensor-anomaly-detector")
    # console.print(f"Registered model version: {registered.version}")
else:
    console.print("[yellow]Run not found — did the logging complete successfully?[/yellow]")

# ---------------------------------------------------------------------------
# Section 4: What to observe in the MLflow UI
# ---------------------------------------------------------------------------

section("4. What to look at in the MLflow UI")

console.print("""
Run: uv run mlflow ui
Open: http://localhost:5000

Things to find:
  1. The experiment "sensor-anomaly-detection" with three runs
  2. Compare the runs — which contamination value had the best F1?
  3. Click into a run — find the logged parameters, metrics, and artifacts
  4. Open the "isolation-forest" artifact — it's a serialized sklearn model
  5. Find the registered model under "Models"

Things to think about:
  - If you ran this script again with different random seeds, would the results change?
    (They wouldn't — why not?)
  - MLflow logged the git commit hash (if you're in a git repo). Why does that matter?
  - The Model Registry has Staging and Production stages. Who should approve a model
    moving to Production, and what should they check?
""")
