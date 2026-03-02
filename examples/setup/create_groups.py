# =============================================================================
# Course Setup: Create Demo Groups
# =============================================================================
# Creates workspace-local groups used in the access-control examples.
# Note: Unity Catalog GRANT statements require account-level groups managed
# in the Account Console. These workspace groups demonstrate the SDK API but
# for UC grants the examples use current_user() instead.
# =============================================================================

from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

DEMO_GROUPS = [
    "analysts",
    "data-admins",
    "data-consumers",
    "data-engineers",
    "etl-service-principal",
    "ml-engineers",
    "contractors",
]

existing = {g.display_name for g in w.groups.list()}

for name in DEMO_GROUPS:
    if name in existing:
        print(f"  [skip]    {name}")
        continue
    group = w.groups.create(display_name=name)
    print(f"  [created] {group.display_name}  id={group.id}")
