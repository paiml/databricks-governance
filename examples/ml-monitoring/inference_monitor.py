# =============================================================================
# Lesson 3.3: ML Model Monitoring
# Creating an Inference Table Monitor for Drift Detection
# =============================================================================
# After deploying a model, you log inputs and predictions to an inference table.
# Databricks Lakehouse Monitoring can attach to that table and compute:
#   - Feature drift (has the input distribution shifted since training?)
#   - Prediction drift (are predictions changing in unusual ways?)
#   - Model performance (when ground truth labels are available)
#
# Run this file as a Databricks notebook on a cluster with DBR 14.0 ML or later.
# =============================================================================

# COMMAND ----------
# Cell 1: Imports and configuration

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.catalog import (
    MonitorInferenceLog,
    MonitorInferenceLogProblemType,
)

w = WorkspaceClient()

# The inference table written by the model serving endpoint or batch job
INFERENCE_TABLE = "GovernanceCatalog.ml.event_classifier_inference"

# The training dataset used as the baseline for drift comparison
BASELINE_TABLE = "GovernanceCatalog.ml.event_classifier_training_baseline"

# Where monitoring output tables should be stored
MONITORING_SCHEMA = "GovernanceCatalog.monitoring"

MODEL_NAME = "GovernanceCatalog.ml.event_classifier"

# COMMAND ----------
# Cell 2: Create the inference table if it does not exist yet
# In production this table is written by the serving endpoint; here we create
# a stub schema so the monitor definition can reference it.

spark.sql(f"""
    CREATE TABLE IF NOT EXISTS {INFERENCE_TABLE} (
      request_id       STRING    NOT NULL  COMMENT 'Unique serving request identifier',
      timestamp        TIMESTAMP NOT NULL  COMMENT 'UTC time the prediction was made',
      sepal_length_cm  DOUBLE              COMMENT 'Input feature',
      sepal_width_cm   DOUBLE              COMMENT 'Input feature',
      petal_length_cm  DOUBLE              COMMENT 'Input feature',
      petal_width_cm   DOUBLE              COMMENT 'Input feature',
      prediction       INT                 COMMENT 'Model output class label (0, 1, or 2)',
      ground_truth     INT                 COMMENT 'Actual label — populated after feedback loop'
    )
    USING DELTA
    TBLPROPERTIES ('delta.enableChangeDataFeed' = 'true')
""")

print(f"Inference table ready: {INFERENCE_TABLE}")

# COMMAND ----------
# Cell 3: Create the monitoring baseline from the training split

spark.sql(f"""
    CREATE TABLE IF NOT EXISTS {BASELINE_TABLE}
    USING DELTA
    AS
    SELECT
      sepal_length_cm,
      sepal_width_cm,
      petal_length_cm,
      petal_width_cm,
      prediction,
      ground_truth
    FROM {INFERENCE_TABLE}
    WHERE timestamp < current_timestamp() - INTERVAL 30 DAYS
    LIMIT 0   -- empty baseline; populate with your actual training data
""")

print(f"Baseline table ready: {BASELINE_TABLE}")

# COMMAND ----------
# Cell 4: Attach an inference log monitor to the inference table

monitor = w.quality_monitors.create(
    table_name=INFERENCE_TABLE,
    assets_dir=f"/Shared/monitoring/ml/{INFERENCE_TABLE.replace('.', '_')}",
    output_schema_name=MONITORING_SCHEMA,
    inference_log=MonitorInferenceLog(
        problem_type=MonitorInferenceLogProblemType.PROBLEM_TYPE_CLASSIFICATION,
        prediction_col="prediction",
        label_col="ground_truth",          # optional — enables accuracy/F1 tracking
        timestamp_col="timestamp",
        model_id_col=None,                 # set if you log multiple model versions
        granularities=["1 day", "1 week"], # time windows for drift computation
    ),
    baseline_table_name=BASELINE_TABLE,
)

print(f"Inference monitor created: {INFERENCE_TABLE}")
print(f"Profile table: {monitor.profile_metrics_table_name}")
print(f"Drift table:   {monitor.drift_metrics_table_name}")

# COMMAND ----------
# Cell 5: Query drift metrics after the first refresh

drift_table = monitor.drift_metrics_table_name

drift_df = spark.sql(f"""
    SELECT
      window.start       AS window_start,
      column_name,
      statistic_name,
      drift_type,
      drift_value,
      threshold_value
    FROM {drift_table}
    WHERE drift_value IS NOT NULL
      AND drift_value > COALESCE(threshold_value, 0.1)
    ORDER BY drift_value DESC
    LIMIT 20
""")

display(drift_df)

# COMMAND ----------
# Cell 6: Trigger retraining when drift exceeds threshold
# Wire this logic into a Databricks Workflow as a conditional task.

HIGH_DRIFT_THRESHOLD = 0.15

drift_rows = drift_df.filter(f"drift_value > {HIGH_DRIFT_THRESHOLD}").count()

if drift_rows > 0:
    print(f"DRIFT DETECTED — {drift_rows} column(s) exceed threshold {HIGH_DRIFT_THRESHOLD}.")
    print("Triggering retraining job via Databricks Jobs API...")
    # In a real workflow, use dbutils.notebook.run() or the Jobs API to kick off
    # the training pipeline defined in examples/mlops/train_and_register.py
    # Example: dbutils.notebook.run("/Shared/mlops/train_and_register", timeout_seconds=3600)
else:
    print("No significant drift detected. Model remains in production.")
