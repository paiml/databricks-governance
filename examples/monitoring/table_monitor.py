# =============================================================================
# Lesson 3.1: Lakehouse Monitoring
# Setting Up a Table Monitor and Querying Its Metric Tables
# =============================================================================
# Databricks Lakehouse Monitoring attaches to any Delta table and automatically
# produces a profile metrics table and a drift metrics table stored in a schema
# you specify. No custom monitoring logic required.
#
# Run this file as a Databricks notebook on a cluster with DBR 12.2 LTS or later.
# The databricks-sdk package is included in Databricks Runtime by default.
# =============================================================================

# COMMAND ----------
# Cell 1: Imports

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.catalog import (
    MonitorSnapshot,
    MonitorInferenceLog,
    MonitorInferenceLogProblemType,
)

w = WorkspaceClient()

TABLE_NAME = "GovernanceCatalog.silver.events_clean"
MONITORING_SCHEMA = "GovernanceCatalog.monitoring"

# COMMAND ----------
# Cell 2: Create a snapshot monitor on the silver events table
# A snapshot monitor computes statistics over the full table on each refresh.

monitor = w.quality_monitors.create(
    table_name=TABLE_NAME,
    assets_dir=f"/Shared/monitoring/{TABLE_NAME.replace('.', '_')}",
    output_schema_name=MONITORING_SCHEMA,
    snapshot=MonitorSnapshot(),
)

print(f"Monitor created for: {TABLE_NAME}")
print(f"Profile metrics table:  {monitor.profile_metrics_table_name}")
print(f"Drift metrics table:    {monitor.drift_metrics_table_name}")

# COMMAND ----------
# Cell 3: Trigger an immediate refresh of the monitor

run_info = w.quality_monitors.run_refresh(table_name=TABLE_NAME)
print(f"Refresh run ID: {run_info.refresh_id}")
print(f"State: {run_info.state}")

# COMMAND ----------
# Cell 4: Query the auto-generated profile metrics table
# This table contains per-column statistics: null counts, mean, stddev, percentiles, etc.

profile_table = f"{MONITORING_SCHEMA}.{TABLE_NAME.replace('.', '_')}_profile_metrics"

profile_df = spark.sql(f"""
    SELECT
      column_name,
      count_null,
      count_distinct,
      data_type,
      percent_distinct
    FROM {profile_table}
    ORDER BY column_name
""")

display(profile_df)

# COMMAND ----------
# Cell 5: Query the drift metrics table to detect statistical changes over time

drift_table = f"{MONITORING_SCHEMA}.{TABLE_NAME.replace('.', '_')}_drift_metrics"

drift_df = spark.sql(f"""
    SELECT
      window.start     AS window_start,
      window.end       AS window_end,
      column_name,
      statistic_name,
      drift_type,
      drift_value
    FROM {drift_table}
    WHERE drift_value IS NOT NULL
    ORDER BY window_start DESC, drift_value DESC
    LIMIT 50
""")

display(drift_df)

# COMMAND ----------
# Cell 6: Set up a Databricks SQL alert on the profile metrics table
# Create an alert in the UI based on a SQL query like:
#
#   SELECT column_name, count_null / count_total AS null_rate
#   FROM <profile_table>
#   WHERE null_rate > 0.05
#
# Then configure the alert to notify a Slack webhook or email when rows are returned.
print("Create SQL alerts in the Databricks SQL UI using the profile and drift metric tables above.")
print(f"Profile table: {profile_table}")
print(f"Drift table:   {drift_table}")
