# =============================================================================
# Lesson 1.1: Unity Catalog Overview
# Creating and Inspecting a Catalog
# =============================================================================
# Sidecar for: examples/unity/create_catalog.sql
# Run:  python examples/unity/create_catalog.py
# Prereqs:
#   export DATABRICKS_HOST, DATABRICKS_TOKEN
#   Caller must have metastore admin or CREATE CATALOG privilege
# =============================================================================

from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import ResourceAlreadyExists

w = WorkspaceClient()

# -- Create the catalog ---------------------------------------------------
# Mirrors: CREATE CATALOG IF NOT EXISTS GovernanceCatalog COMMENT '...'
print("Creating GovernanceCatalog...")
try:
    catalog = w.catalogs.create(
        name="GovernanceCatalog",
        comment="Demonstration catalog for the Governance and MLOps course",
    )
    print(f"  Created: {catalog.name}")
except ResourceAlreadyExists:
    catalog = w.catalogs.get(name="GovernanceCatalog")
    print(f"  Already exists: {catalog.name}")

# -- Inspect the catalog --------------------------------------------------
# Mirrors: DESCRIBE CATALOG GovernanceCatalog
print("\nDescribing GovernanceCatalog...")
info = w.catalogs.get(name="GovernanceCatalog")
print(f"  name:       {info.name}")
print(f"  comment:    {info.comment}")
print(f"  owner:      {info.owner}")
print(f"  created_at: {info.created_at}")
print(f"  metastore:  {info.metastore_id}")

# -- List all visible catalogs --------------------------------------------
# Mirrors: SHOW CATALOGS
print("\nVisible catalogs:")
for cat in w.catalogs.list():
    print(f"  {cat.name}")
