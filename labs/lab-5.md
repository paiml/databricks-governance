# Lab 5: ML Model CI/CD with MLflow

## Objectives

- Train a model and log it to MLflow with automatic parameter and metric tracking
- Register the trained model in the Unity Catalog-backed MLflow Model Registry
- Run validation checks and promote a passing model to the "champion" (production) alias
- Understand how aliases replace the deprecated stage-based promotion workflow

## Prerequisites

- A Databricks cluster with ML Runtime (DBR ML 14.0 or later recommended)
- GovernanceCatalog with a `ml` schema (created in Lab 1)
- MLflow is pre-installed on all Databricks ML runtime clusters

## Background

The ML lifecycle differs from traditional software deployment in three critical ways:

1. **Experiments are non-deterministic** — you run many training runs and pick the best one
2. **Models are artifacts** — the model binary must be versioned and stored, not just the code
3. **"Deployed" means serving** — you manage both the training code and the resulting model artifact

MLflow provides experiment tracking and the Model Registry. When backed by Unity Catalog, the registry uses a three-level name (`catalog.schema.model_name`) and benefits from Unity Catalog's access controls, lineage, and audit logging.

**Aliases vs. Stages:** The old stage-based workflow (`Staging`, `Production`) is deprecated. The current best practice is to use aliases (`candidate`, `champion`) that point to specific version numbers.

## Exercise 1: Train and Register a Model

Review [`examples/mlops/train_and_register.py`](../examples/mlops/train_and_register.py).

1. Import the file into your Databricks workspace and attach to an ML cluster
2. Run cells 1–3 to train the model and log it to MLflow
3. Navigate to **Experiments** in the sidebar — observe the logged parameters, metrics, and artifacts
4. Run cell 4 to register the model in the Unity Catalog Registry
5. Navigate to **Models** in the sidebar — observe the registered model and version

### Questions

1. What does `mlflow.sklearn.autolog()` log automatically?
2. Why is `mlflow.set_registry_uri("databricks-uc")` required when using Unity Catalog?
3. What happens if you run the training cell twice — does it create a second version?

## Exercise 2: Validate and Promote the Model

Review [`examples/mlops/promote_model.py`](../examples/mlops/promote_model.py).

1. Import the file into your workspace
2. Run cells 1–3: load the candidate model by alias and run validation
3. Observe the accuracy result against the `ACCURACY_THRESHOLD`
4. Run cell 4: if validation passes, the model is promoted to the `champion` alias
5. Verify in the Models UI that the `champion` alias now points to the correct version number

### What to Observe

- The `candidate` alias is set during training; `champion` is only set after validation
- Validation uses a different random seed than training — a fresh split of the data
- If accuracy is below threshold, a `ValueError` is raised and the job run fails — no promotion happens

## Exercise 3: Inspect the Model Registry

1. In the Models UI, click on the registered model `GovernanceCatalog.ml.event_classifier`
2. Observe:
   - Version history
   - Aliases (`candidate`, `champion`)
   - Linked experiment run (click the run ID to see logged metrics)
   - Permissions (who can view, update, manage)

### Questions

1. How would you roll back to a previous champion version if the new one causes errors in production?
2. How would you configure a webhook to notify Slack when a new version is registered?

## Key Takeaways

- `mlflow.sklearn.autolog()` logs parameters, metrics, and the model artifact automatically
- Unity Catalog-backed model registry provides three-level naming, access control, and lineage for models
- Use aliases (`candidate`, `champion`) instead of stages — they can be moved freely across version numbers
- Validation gates before promotion prevent untested models from reaching production
