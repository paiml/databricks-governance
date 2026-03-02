# Lab 6: Monitoring and Secrets Management

## Objectives

- Attach a Lakehouse Monitor to a Delta table and query the generated metric tables
- Attach an inference log monitor to an ML serving inference table
- Detect feature and prediction drift and wire up a retraining trigger
- Create a Databricks-backed secret scope and retrieve credentials safely in a notebook
- Understand the difference between Databricks-backed, Azure Key Vault-backed, and AWS Secrets Manager-backed scopes

## Prerequisites

- Completed Lab 1 (GovernanceCatalog with schemas and tables)
- Completed Lab 5 (event_classifier model trained and registered)
- A Databricks cluster with DBR 12.2 LTS or later (for Lakehouse Monitoring SDK)
- Databricks CLI installed locally for secret scope creation

## Background — Lakehouse Monitoring

Production data pipelines fail silently far more often than they fail loudly. A schema drift, a late-arriving partition, or a change in upstream data can corrupt your tables for days before anyone notices. Databricks Lakehouse Monitoring attaches to any Delta table and automatically generates:

- **Profile metrics table** — per-column statistics (null rates, cardinality, percentiles) over time
- **Drift metrics table** — statistical comparison between time windows (Jensen-Shannon divergence, Wasserstein distance)
- **Auto-generated dashboard** — pre-built DBSQL dashboard linked to both metric tables

## Background — Secrets Management

A hardcoded password in a notebook is one of the most common and costliest security mistakes in data engineering. It shows up in version history, gets shared in screenshots, and can expose production databases to anyone with read access to the workspace. Databricks secret scopes solve this by providing an API to store and retrieve credentials without ever exposing the value in output.

## Exercise 1: Set Up a Table Monitor

Review [`examples/monitoring/table_monitor.py`](../examples/monitoring/table_monitor.py).

1. Import the file into your workspace and attach to a cluster
2. Run cell 2 to create the snapshot monitor on `GovernanceCatalog.silver.events_clean`
3. Run cell 3 to trigger the first refresh
4. After the refresh completes (~2 minutes), run cells 4–5 to query the profile and drift tables

### What to Observe

- The profile table contains a row per column per refresh window
- The drift table is empty until there is at least one subsequent refresh to compare against
- Databricks automatically creates a DBSQL dashboard — find it under **Dashboards** in the sidebar

## Exercise 2: Set Up an Inference Table Monitor

Review [`examples/ml-monitoring/inference_monitor.py`](../examples/ml-monitoring/inference_monitor.py).

1. Import and run the file
2. Observe how `MonitorInferenceLog` differs from `MonitorSnapshot` — it takes prediction and label column names
3. After a refresh, query the drift metrics table for features with high drift values

### Questions

1. What does it mean when `prediction` drift is high but feature drift is low?
2. When would you set `label_col` to `None`?
3. Why is the baseline table important for drift detection?

## Exercise 3: Create a Secret Scope and Retrieve Credentials

Review [`examples/secrets/secret_scope.py`](../examples/secrets/secret_scope.py).

1. Open a terminal and run the Databricks CLI commands from Cell 1's comments to create a scope named `governance-course`
2. Add a test secret: `databricks secrets put --scope governance-course --key jdbc-password`
3. In the notebook, run Cell 2 to retrieve the secret — observe that Databricks redacts the output
4. Run Cell 3 to list all scopes and keys visible to your user

### What to Observe

- `dbutils.secrets.get()` returns a Python string — but Databricks replaces its value with `[REDACTED]` in any output cell
- The key metadata is visible (key name, byte length), but the value never is

### Questions

1. What is the difference between a Databricks-backed scope and an Azure Key Vault-backed scope from a developer's perspective? From a security team's perspective?
2. How would you restrict the `governance-course` scope so only the `etl-service-principal` can read from it?

## Key Takeaways

- Lakehouse Monitoring requires zero custom monitoring code — attach the monitor to any Delta table and it generates metrics automatically
- Profile metrics tables enable data quality dashboards; drift metrics tables enable anomaly alerting
- Never print secret values in notebook output — Databricks redacts them, but don't rely on this as a security control
- Cloud-native vault backends (Key Vault, Secrets Manager) are preferred for enterprise deployments — secrets never enter Databricks storage
