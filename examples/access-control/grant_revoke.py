# =============================================================================
# Lesson 1.4: Access Control — GRANT and REVOKE
# =============================================================================
# Sidecar for: examples/access-control/grant_revoke.sql
# =============================================================================

from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import NotFound
from databricks.sdk.service import catalog

w = WorkspaceClient()

# Resolve the current user — the only principal guaranteed to exist in the
# current workspace. In production, replace with group names like `analysts`.
me = w.current_user.me()

# ── Catalog-level ─────────────────────────────────────────────────────────────

w.grants.update(
    securable_type="catalog",
    full_name="GovernanceCatalog",
    changes=[
        catalog.PermissionsChange(add=[catalog.Privilege.USE_CATALOG], principal=me.user_name),
    ],
)

w.grants.update(
    securable_type="catalog",
    full_name="GovernanceCatalog",
    changes=[
        catalog.PermissionsChange(add=[catalog.Privilege.CREATE_SCHEMA], principal=me.user_name),
    ],
)

# ── Schema-level ──────────────────────────────────────────────────────────────

w.grants.update(
    securable_type="schema",
    full_name="GovernanceCatalog.silver",
    changes=[
        catalog.PermissionsChange(
            add=[catalog.Privilege.USE_SCHEMA, catalog.Privilege.SELECT],
            principal=me.user_name,
        ),
    ],
)

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

w.grants.update(
    securable_type="schema",
    full_name="GovernanceCatalog.ml",
    changes=[
        catalog.PermissionsChange(
            add=[
                catalog.Privilege.USE_SCHEMA,
                catalog.Privilege.SELECT,
                catalog.Privilege.MODIFY,
                catalog.Privilege.CREATE_TABLE,
            ],
            principal=me.user_name,
        ),
    ],
)

# ── Table-level ───────────────────────────────────────────────────────────────
# Requires tables to exist first — run examples/unity/create_tables.py beforehand.

try:
    w.grants.update(
        securable_type="table",
        full_name="GovernanceCatalog.gold.daily_event_counts",
        changes=[
            catalog.PermissionsChange(add=[catalog.Privilege.SELECT], principal=me.user_name),
        ],
    )

    # ── Revoke ────────────────────────────────────────────────────────────────

    w.grants.update(
        securable_type="table",
        full_name="GovernanceCatalog.gold.daily_event_counts",
        changes=[
            catalog.PermissionsChange(remove=[catalog.Privilege.SELECT], principal=me.user_name),
        ],
    )
except NotFound as e:
    print(f"  [skip] table-level grant/revoke: {e}")
    print("         Run examples/unity/create_tables.py first to create the tables.")

# ── Inspect effective permissions ─────────────────────────────────────────────

table_grants = w.grants.get_effective(
    securable_type="table",
    full_name="GovernanceCatalog.silver.events_clean",
)
for assignment in (table_grants.privilege_assignments or []):
    privs = [p.privilege.value for p in (assignment.privileges or [])]
    print(f"{assignment.principal}: {privs}")

schema_grants = w.grants.get_effective(
    securable_type="schema",
    full_name="GovernanceCatalog.silver",
    principal=me.user_name,
)
for assignment in (schema_grants.privilege_assignments or []):
    privs = [p.privilege.value for p in (assignment.privileges or [])]
    print(f"{assignment.principal}: {privs}")
