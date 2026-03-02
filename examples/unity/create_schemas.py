# =============================================================================
# Lesson 1.1: Unity Catalog Overview
# Creating Schemas (Databases) That Mirror Data Layers
# =============================================================================
# Sidecar for: examples/unity/create_schemas.sql
# Run:  python examples/unity/create_schemas.py
# Prereqs:
#   export DATABRICKS_HOST, DATABRICKS_TOKEN
#   create_catalog.py must have been run first
# =============================================================================

from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import ResourceAlreadyExists

w = WorkspaceClient()

CATALOG = "GovernanceCatalog"

SCHEMAS = [
    ("bronze", "Raw ingested data — untransformed, append-only"),
    ("silver", "Cleaned and validated data — conformed types and deduplication applied"),
    ("gold",   "Business-ready aggregations and feature tables"),
    ("ml",     "MLflow models, feature tables, and evaluation results"),
]

# -- Create schemas -------------------------------------------------------
# Mirrors: CREATE SCHEMA IF NOT EXISTS GovernanceCatalog.<name> COMMENT '...'
print(f"Creating schemas in {CATALOG}...")
for name, comment in SCHEMAS:
    try:
        schema = w.schemas.create(
            name=name,
            catalog_name=CATALOG,
            comment=comment,
        )
        print(f"  Created: {schema.full_name}")
    except ResourceAlreadyExists:
        print(f"  Already exists: {CATALOG}.{name}")

# -- List all schemas in the catalog --------------------------------------
# Mirrors: SHOW SCHEMAS IN GovernanceCatalog
print(f"\nSchemas in {CATALOG}:")
for schema in w.schemas.list(catalog_name=CATALOG):
    print(f"  {schema.name}")

# -- Inspect one schema's metadata ----------------------------------------
# Mirrors: DESCRIBE SCHEMA GovernanceCatalog.silver
print(f"\nDescribing {CATALOG}.silver...")
silver = w.schemas.get(full_name=f"{CATALOG}.silver")
print(f"  full_name:  {silver.full_name}")
print(f"  comment:    {silver.comment}")
print(f"  owner:      {silver.owner}")
print(f"  created_at: {silver.created_at}")
