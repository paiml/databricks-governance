# =============================================================================
# Lesson 2.6: ML Model CI/CD
# Training a Model and Registering It in the MLflow Model Registry
# =============================================================================
# Run this file as a Databricks notebook (cell by cell) or as a Databricks Job.
# The catalog and schema used here are GovernanceCatalog.ml — adjust to match
# your workspace.
# =============================================================================

# COMMAND ----------
# Cell 1: Imports and configuration

import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

# Unity Catalog-backed MLflow registry (three-level name)
CATALOG = "GovernanceCatalog"
SCHEMA = "ml"
MODEL_NAME = f"{CATALOG}.{SCHEMA}.event_classifier"

# Point MLflow at the Unity Catalog registry
mlflow.set_registry_uri("databricks-uc")

# COMMAND ----------
# Cell 2: Load dataset and split

data = load_iris(as_frame=True)
X_train, X_test, y_train, y_test = train_test_split(
    data.data, data.target, test_size=0.2, random_state=42
)

# COMMAND ----------
# Cell 3: Train with MLflow auto-logging

mlflow.sklearn.autolog()

with mlflow.start_run(run_name="event_classifier_v1") as run:
    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    f1 = f1_score(y_test, predictions, average="weighted")

    # Log custom metrics beyond what autolog captures
    mlflow.log_metric("test_accuracy", acc)
    mlflow.log_metric("test_f1_weighted", f1)

    # Log dataset metadata as a tag for lineage
    mlflow.set_tag("training_dataset", "sklearn.iris")
    mlflow.set_tag("catalog", CATALOG)
    mlflow.set_tag("schema", SCHEMA)

    print(f"Run ID: {run.info.run_id}")
    print(f"Accuracy: {acc:.4f}  |  F1: {f1:.4f}")

    RUN_ID = run.info.run_id

# COMMAND ----------
# Cell 4: Register the model in the Unity Catalog Model Registry

client = MlflowClient()

# Register the model — this creates the registered model if it does not exist
model_uri = f"runs:/{RUN_ID}/model"
model_version = mlflow.register_model(model_uri=model_uri, name=MODEL_NAME)

print(f"Registered model: {MODEL_NAME}")
print(f"Version: {model_version.version}")
print(f"Status: {model_version.status}")

# COMMAND ----------
# Cell 5: Add a candidate alias so CI/CD can reference this version by name

client.set_registered_model_alias(
    name=MODEL_NAME,
    alias="candidate",
    version=model_version.version,
)

print(f"Alias 'candidate' → version {model_version.version}")
