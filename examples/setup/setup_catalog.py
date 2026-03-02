# =============================================================================
# Course Setup: Create GovernanceCatalog and All Schemas
# =============================================================================
# Run this before any other example scripts.
# Requires CREATE CATALOG privilege on the metastore.
# =============================================================================

from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import ResourceAlreadyExists
from databricks.sdk.errors.platform import NotFound

w = WorkspaceClient()

CATALOG_NAME = "GovernanceCatalog"
SCHEMAS = ["bronze", "silver", "gold", "ml", "monitoring"]

# ── Catalog ───────────────────────────────────────────────────────────────────

try:
    cat = w.catalogs.get(name=CATALOG_NAME)
except (ResourceAlreadyExists, NotFound):
    cat = w.catalogs.create(
        name=CATALOG_NAME,
        comment="Demonstration catalog for the Governance and MLOps course",
    )
    print(f"  [created] catalog: {cat.name}")

# ── Schemas ───────────────────────────────────────────────────────────────────

for schema_name in SCHEMAS:
    full_name = f"{CATALOG_NAME}.{schema_name}"
    try:
        schema = w.schemas.create(name=schema_name, catalog_name=CATALOG_NAME)
        print(f"  [created] schema:  {full_name}")
    except ResourceAlreadyExists:
        print(f"  [exists]  schema:  {full_name}")
