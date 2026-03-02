# =============================================================================
# Lesson 2.6: ML Model CI/CD
# Validating and Promoting a Model Through the MLflow Model Registry
# =============================================================================
# This script runs validation checks against the candidate model version and,
# if all checks pass, promotes it to the "champion" (production) alias.
# Run this as a Databricks Job step that follows train_and_register.py.
# =============================================================================

# COMMAND ----------
# Cell 1: Imports and configuration

import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

CATALOG = "GovernanceCatalog"
SCHEMA = "ml"
MODEL_NAME = f"{CATALOG}.{SCHEMA}.event_classifier"

ACCURACY_THRESHOLD = 0.90  # Minimum accuracy required to promote to champion

mlflow.set_registry_uri("databricks-uc")
client = MlflowClient()

# COMMAND ----------
# Cell 2: Load the candidate model by alias

candidate_model = mlflow.sklearn.load_model(f"models:/{MODEL_NAME}@candidate")
print(f"Loaded candidate model: {MODEL_NAME}@candidate")

# Retrieve the version number for this alias
candidate_version_info = client.get_model_version_by_alias(MODEL_NAME, "candidate")
candidate_version = candidate_version_info.version
print(f"Candidate version: {candidate_version}")

# COMMAND ----------
# Cell 3: Run validation on a held-out evaluation dataset

data = load_iris(as_frame=True)
_, X_eval, _, y_eval = train_test_split(
    data.data, data.target, test_size=0.2, random_state=99  # different seed = different split
)

predictions = candidate_model.predict(X_eval)
eval_accuracy = accuracy_score(y_eval, predictions)

print(f"Evaluation accuracy: {eval_accuracy:.4f}  (threshold: {ACCURACY_THRESHOLD})")

# COMMAND ----------
# Cell 4: Promote or reject based on validation result

if eval_accuracy >= ACCURACY_THRESHOLD:
    # Promote to champion alias — this is the model that serving endpoints will load
    client.set_registered_model_alias(
        name=MODEL_NAME,
        alias="champion",
        version=candidate_version,
    )
    print(f"PASSED — version {candidate_version} promoted to 'champion'")
else:
    # Do not promote; fail the job so CI/CD marks this pipeline run as failed
    raise ValueError(
        f"FAILED — accuracy {eval_accuracy:.4f} is below threshold {ACCURACY_THRESHOLD}. "
        f"Version {candidate_version} NOT promoted."
    )

# COMMAND ----------
# Cell 5: Verify the champion alias is now pointing to the new version

champion_info = client.get_model_version_by_alias(MODEL_NAME, "champion")
print(f"Champion alias → version {champion_info.version}")
print(f"Run ID: {champion_info.run_id}")
