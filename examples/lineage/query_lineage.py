# =============================================================================
# Lesson 1.6: Data Lineage
# =============================================================================
# Sidecar for: examples/lineage/query_lineage.sql
# Grants use w.grants.update() (SDK).
# Lineage and audit data live in Unity Catalog system tables; there is no
# higher-level SDK client for them, so w.statement_execution.execute() is
# used — this is the SDK method the official examples use for SQL queries
# (see tmp/databricks-sdk-py/examples/workspace/statement_execution/).
# Requires DATABRICKS_WAREHOUSE_ID env var for statement_execution.
# =============================================================================

import os

from databricks.sdk import WorkspaceClient
from databricks.sdk.service import catalog

w = WorkspaceClient()
me = w.current_user.me()

WAREHOUSE_ID = os.environ["DATABRICKS_WAREHOUSE_ID"]

# ── Grant system table access ─────────────────────────────────────────────────

for schema_name in ("system.access", "system.lineage"):
    w.grants.update(
        securable_type="schema",
        full_name=schema_name,
        changes=[catalog.PermissionsChange(add=[catalog.Privilege.USE_SCHEMA], principal=me.user_name)],
    )

for table_name in (
    "system.access.audit",
    "system.lineage.table_lineage",
    "system.lineage.column_lineage",
):
    w.grants.update(
        securable_type="table",
        full_name=table_name,
        changes=[catalog.PermissionsChange(add=[catalog.Privilege.SELECT], principal=me.user_name)],
    )

# ── Lineage and audit queries ─────────────────────────────────────────────────
# Unity Catalog captures lineage in system.lineage.* and audit logs in
# system.access.audit. No dedicated SDK client exists for these tables;
# w.statement_execution.execute() is the SDK-provided interface for running
# SQL against a warehouse — the same pattern used in the official SDK examples.

upstream = w.statement_execution.execute(
    warehouse_id=WAREHOUSE_ID,
    statement="""
        SELECT source_table_full_name, target_table_full_name, created_by, event_time
        FROM system.lineage.table_lineage
        WHERE target_table_full_name = 'GovernanceCatalog.silver.events_clean'
        ORDER BY event_time DESC
        LIMIT 50
    """,
).result()

downstream = w.statement_execution.execute(
    warehouse_id=WAREHOUSE_ID,
    statement="""
        SELECT source_table_full_name, target_table_full_name, created_by, event_time
        FROM system.lineage.table_lineage
        WHERE source_table_full_name = 'GovernanceCatalog.gold.daily_event_counts'
        ORDER BY event_time DESC
        LIMIT 50
    """,
).result()

col_lineage = w.statement_execution.execute(
    warehouse_id=WAREHOUSE_ID,
    statement="""
        SELECT source_table_full_name, source_column_name,
               target_table_full_name, target_column_name, event_time
        FROM system.lineage.column_lineage
        WHERE target_table_full_name = 'GovernanceCatalog.silver.events_clean'
          AND target_column_name = 'user_id'
        ORDER BY event_time DESC
    """,
).result()

recent_access = w.statement_execution.execute(
    warehouse_id=WAREHOUSE_ID,
    statement="""
        SELECT user_identity.email AS user_email, action_name,
               request_params.table AS table_name, event_time
        FROM system.access.audit
        WHERE action_name IN ('selectTable', 'describeTable')
          AND request_params.table LIKE '%events_clean%'
          AND event_time >= current_timestamp() - INTERVAL 7 DAYS
        ORDER BY event_time DESC
    """,
).result()

drop_events = w.statement_execution.execute(
    warehouse_id=WAREHOUSE_ID,
    statement="""
        SELECT user_identity.email AS user_email, action_name, request_params, event_time
        FROM system.access.audit
        WHERE action_name IN ('deleteTable', 'deleteSchema', 'deleteCatalog')
          AND event_time >= current_timestamp() - INTERVAL 30 DAYS
        ORDER BY event_time DESC
    """,
).result()

pii_downstream = w.statement_execution.execute(
    warehouse_id=WAREHOUSE_ID,
    statement="""
        SELECT DISTINCT target_table_full_name, target_column_name
        FROM system.lineage.column_lineage
        WHERE source_table_full_name = 'GovernanceCatalog.bronze.raw_events'
          AND source_column_name = 'payload'
        ORDER BY target_table_full_name
    """,
).result()
