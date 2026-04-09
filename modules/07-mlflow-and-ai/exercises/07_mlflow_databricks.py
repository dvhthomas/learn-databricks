# Databricks notebook source
# Upload to Databricks (requires Unity Catalog workspace with your Gold table).
# Uses the managed MLflow tracking server — no local mlruns/ directory.

# COMMAND ----------
# MAGIC %md
# MAGIC # Module 7: MLflow on Databricks
# MAGIC
# MAGIC Same experiment as mlflow_local.py, but now using:
# MAGIC - Your actual Gold table from Unity Catalog
# MAGIC - The managed MLflow tracking server (no local setup)
# MAGIC - The Databricks Model Registry
# MAGIC
# MAGIC After running, find your experiment under Experiments in the left sidebar.

# COMMAND ----------

import mlflow
import mlflow.sklearn
from sklearn.ensemble import IsolationForest

# Databricks manages the MLflow tracking server automatically
# mlflow.get_tracking_uri() will show "databricks"
print("MLflow tracking URI:", mlflow.get_tracking_uri())

# COMMAND ----------
# MAGIC %md
# MAGIC ## Load Gold data from Unity Catalog

# COMMAND ----------

# TODO: Read your Gold table from Unity Catalog
# gold_df = spark.table("learning.sensors.gold_hourly_stats").toPandas()

# For now, generate synthetic data if the table doesn't exist yet
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 500
gold_df = pd.DataFrame({
    "sensor_id": rng.choice([f"sensor_{i:04d}" for i in range(5)], n),
    "avg_temp_c": rng.normal(25.0, 6.0, n),
    "max_temp_c": rng.normal(28.0, 7.0, n),
    "min_temp_c": rng.normal(22.0, 5.0, n),
    "reading_count": rng.integers(8, 30, n),
})

print(f"Gold data shape: {gold_df.shape}")
display(gold_df.head())

# COMMAND ----------
# MAGIC %md
# MAGIC ## Run experiments

# COMMAND ----------

mlflow.set_experiment("/Users/" + spark.sql("SELECT current_user()").collect()[0][0] + "/sensor-anomaly-detection")

features = ["avg_temp_c", "max_temp_c", "min_temp_c", "reading_count"]
X = gold_df[features]

for contamination in [0.05, 0.10, 0.20]:
    with mlflow.start_run(run_name=f"isolation_forest_c{int(contamination*100)}"):
        mlflow.log_param("contamination", contamination)
        mlflow.log_param("features", features)
        mlflow.log_param("training_rows", len(X))

        model = IsolationForest(contamination=contamination, random_state=42)
        model.fit(X)

        predictions = (model.predict(X) == -1).astype(int)
        mlflow.log_metric("predicted_anomaly_rate", float(predictions.mean()))
        mlflow.log_metric("anomaly_count", int(predictions.sum()))

        # TODO: log the model
        # mlflow.sklearn.log_model(model, "isolation-forest",
        #     input_example=X.head(3))

        print(f"contamination={contamination}: {predictions.sum()} anomalies ({predictions.mean():.1%})")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Register the best model

# COMMAND ----------

# TODO: Register the run with contamination=0.10
# runs = mlflow.search_runs(filter_string="params.contamination = '0.1'")
# best_run_id = runs.iloc[0]["run_id"]
# model_uri = f"runs:/{best_run_id}/isolation-forest"
# registered = mlflow.register_model(model_uri, "sensor-anomaly-detector")

# COMMAND ----------
# MAGIC %md
# MAGIC ## What to observe
# MAGIC
# MAGIC 1. Left sidebar > Experiments — find "sensor-anomaly-detection"
# MAGIC 2. Compare the three runs. Which has the best anomaly rate for your data?
# MAGIC 3. Left sidebar > Models — find "sensor-anomaly-detector" (if you registered it)
# MAGIC 4. Notice that lineage shows which notebook created which model
# MAGIC 5. Notice that Unity Catalog governs who can access the registered model
# MAGIC
# MAGIC The key insight: this is the same governance story as your data pipeline.
# MAGIC Models are versioned artifacts with lineage, access control, and audit trails —
# MAGIC just like Delta tables in Unity Catalog.
