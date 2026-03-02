# =============================================================================
# Lesson 1.4: Access Control — Permission Model for Real-World Teams
# =============================================================================
# Sidecar for: examples/access-control/permission_model.sql
# Column masks and row filters (steps 5-6) have no SDK equivalent;
# those are SQL DDL features only.
# =============================================================================

from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import NotFound
from databricks.sdk.service import catalog

w = WorkspaceClient()
me = w.current_user.me()

# ── Step 1: USE CATALOG ───────────────────────────────────────────────────────

w.grants.update(
    securable_type="catalog",
    full_name="GovernanceCatalog",
    changes=[
        catalog.PermissionsChange(add=[catalog.Privilege.USE_CATALOG], principal=me.user_name),
    ],
)

# ── Step 2: Bronze ────────────────────────────────────────────────────────────

w.grants.update(
    securable_type="schema",
    full_name="GovernanceCatalog.bronze",
    changes=[
        catalog.PermissionsChange(
            add=[catalog.Privilege.USE_SCHEMA, catalog.Privilege.SELECT, catalog.Privilege.MODIFY],
            principal=me.user_name,
        ),
    ],
)

# ── Step 3: Silver ────────────────────────────────────────────────────────────

w.grants.update(
    securable_type="schema",
    full_name="GovernanceCatalog.silver",
    changes=[
        catalog.PermissionsChange(
            add=[catalog.Privilege.USE_SCHEMA, catalog.Privilege.SELECT, catalog.Privilege.MODIFY],
            principal=me.user_name,
        ),
    ],
)

# ── Step 4: Gold ──────────────────────────────────────────────────────────────

w.grants.update(
    securable_type="schema",
    full_name="GovernanceCatalog.gold",
    changes=[
        catalog.PermissionsChange(
            add=[catalog.Privilege.USE_SCHEMA, catalog.Privilege.SELECT],
            principal=me.user_name,
        ),
    ],
)

# ── Audit ─────────────────────────────────────────────────────────────────────
# Table-level audit requires the table to exist — run create_tables.py first.

for securable_type, full_name in [
    ("catalog", "GovernanceCatalog"),
    ("schema",  "GovernanceCatalog.silver"),
    ("table",   "GovernanceCatalog.silver.events_clean"),
]:
    try:
        result = w.grants.get_effective(securable_type=securable_type, full_name=full_name)
        print(f"\n{full_name}:")
        for a in (result.privilege_assignments or []):
            privs = [p.privilege.value for p in (a.privileges or [])]
            print(f"  {a.principal}: {privs}")
    except NotFound:
        print(f"\n{full_name}: [not found — run create_tables.py first]")
