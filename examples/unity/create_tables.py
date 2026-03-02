# =============================================================================
# Lesson 1.1: Unity Catalog Overview
# Creating Tables, Volumes, and Inspecting Objects
# =============================================================================
# Sidecar for: examples/unity/create_tables.sql
# Run:  python examples/unity/create_tables.py
# Prereqs:
#   export DATABRICKS_HOST, DATABRICKS_TOKEN
#   create_catalog.py and create_schemas.py must have been run first
#
# Note on Spark session:
#   The DeltaTable builder requires a live Spark session. Use one of:
#     a) VS Code Databricks extension connected to a cluster
#     b) databricks-connect installed locally:  pip install databricks-connect
#   Volumes and table inspection (list/get) use the REST API and need no Spark.
# =============================================================================

from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import ResourceAlreadyExists
from databricks.sdk.service.catalog import VolumeType

# Delta table creation requires PySpark. Use databricks-connect for local runs.
try:
    from databricks.connect import DatabricksSession
    spark = DatabricksSession.builder.getOrCreate()
except ImportError:
    from pyspark.sql import SparkSession
    spark = SparkSession.getActiveSession()
    if spark is None:
        raise RuntimeError(
            "No active Spark session found.\n"
            "Install databricks-connect for local runs:  pip install databricks-connect\n"
            "Or run this file via the VS Code Databricks extension on a connected cluster."
        )

from delta.tables import DeltaTable  # noqa: E402 (import after spark is ready)

w = WorkspaceClient()
CATALOG = "GovernanceCatalog"

# ── Bronze: raw event ingest ──────────────────────────────────────────────────
# Mirrors: CREATE TABLE IF NOT EXISTS GovernanceCatalog.bronze.raw_events (...)
print("Creating bronze.raw_events...")
DeltaTable.createIfNotExists(spark) \
    .tableName(f"{CATALOG}.bronze.raw_events") \
    .comment("Bronze-layer raw events — full fidelity, no transformations applied") \
    .addColumn("event_id",   "STRING",    nullable=False, comment="Unique identifier for the event") \
    .addColumn("event_time", "TIMESTAMP",                 comment="UTC timestamp when the event occurred") \
    .addColumn("source",     "STRING",                    comment="System or service that produced the event") \
    .addColumn("payload",    "STRING",                    comment="Raw JSON payload from the source system") \
    .property("delta.enableChangeDataFeed", "true") \
    .execute()
print("  Done.")

# ── Silver: validated and typed ───────────────────────────────────────────────
print("Creating silver.events_clean...")
DeltaTable.createIfNotExists(spark) \
    .tableName(f"{CATALOG}.silver.events_clean") \
    .comment("Silver-layer events — deduplicated, typed, and null-checked") \
    .addColumn("event_id",   "STRING",    nullable=False, comment="Unique identifier for the event") \
    .addColumn("event_time", "TIMESTAMP", nullable=False, comment="UTC timestamp when the event occurred") \
    .addColumn("source",     "STRING",    nullable=False, comment="System or service that produced the event") \
    .addColumn("event_type", "STRING",                    comment="Parsed event type from the payload") \
    .addColumn("user_id",    "STRING",                    comment="User associated with the event, if present") \
    .execute()
print("  Done.")

# ── Gold: pre-aggregated business metrics ─────────────────────────────────────
print("Creating gold.daily_event_counts...")
DeltaTable.createIfNotExists(spark) \
    .tableName(f"{CATALOG}.gold.daily_event_counts") \
    .comment("Gold-layer daily event counts — pre-aggregated for dashboard queries") \
    .addColumn("event_date",  "DATE",   nullable=False, comment="Calendar date of the events") \
    .addColumn("source",      "STRING", nullable=False, comment="System or service that produced the events") \
    .addColumn("event_type",  "STRING", nullable=False, comment="Parsed event type") \
    .addColumn("event_count", "BIGINT",                 comment="Number of events for this date/source/type") \
    .execute()
print("  Done.")

# ── Volume: unstructured file storage under Unity Catalog governance ──────────
# Mirrors: CREATE VOLUME IF NOT EXISTS GovernanceCatalog.bronze.raw_files
print("Creating bronze.raw_files volume...")
try:
    vol = w.volumes.create(
        catalog_name=CATALOG,
        schema_name="bronze",
        name="raw_files",
        volume_type=VolumeType.MANAGED,
        comment="Landing zone for raw CSV and JSON files before pipeline ingestion",
    )
    print(f"  Created volume: {vol.full_name}")
except ResourceAlreadyExists:
    print(f"  Already exists: {CATALOG}.bronze.raw_files")

# ── Inspection: list tables and volumes ───────────────────────────────────────
# Mirrors: SHOW TABLES IN GovernanceCatalog.<schema>
for schema_name in ("bronze", "silver", "gold"):
    tables = list(w.tables.list(catalog_name=CATALOG, schema_name=schema_name))
    print(f"\nTables in {CATALOG}.{schema_name}: ({len(tables)} found)")
    for t in tables:
        print(f"  {t.name}  [{t.table_type.value if t.table_type else '?'}]")

# Mirrors: SHOW VOLUMES IN GovernanceCatalog.bronze
print(f"\nVolumes in {CATALOG}.bronze:")
for v in w.volumes.list(catalog_name=CATALOG, schema_name="bronze"):
    print(f"  {v.name}  [{v.volume_type.value if v.volume_type else '?'}]")

# ── Describe a table — mirrors DESCRIBE TABLE EXTENDED ───────────────────────
print(f"\nTable info for {CATALOG}.silver.events_clean:")
info = w.tables.get(full_name=f"{CATALOG}.silver.events_clean")
print(f"  full_name:    {info.full_name}")
print(f"  table_type:   {info.table_type.value if info.table_type else '?'}")
print(f"  data_source:  {info.data_source_format.value if info.data_source_format else '?'}")
print(f"  owner:        {info.owner}")
print(f"  comment:      {info.comment}")
if info.columns:
    print("  columns:")
    for col in info.columns:
        nullable = "" if col.nullable else " NOT NULL"
        print(f"    {col.name:15s}  {str(col.type_name.value if col.type_name else '?'):12s}{nullable}")
