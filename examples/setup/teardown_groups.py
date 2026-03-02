# =============================================================================
# Course Teardown: Remove Demo Account-Level Groups
# Run this AFTER finishing the access-control examples.
# =============================================================================
# Removes the account-level groups created by create_groups.py.
# Groups NOT in DEMO_GROUPS are left untouched.
#
# Environment variables (same as create_groups.py):
#   DATABRICKS_ACCOUNT_HOST   — e.g. https://accounts.cloud.databricks.com
#   DATABRICKS_ACCOUNT_ID     — your account UUID
#   DATABRICKS_TOKEN          — a PAT with account admin rights
#
# Usage:
#   python examples/setup/teardown_groups.py
# =============================================================================

import os
import sys

from databricks.sdk import AccountClient

DATABRICKS_ACCOUNT_HOST = os.environ.get("DATABRICKS_ACCOUNT_HOST", "")
DATABRICKS_ACCOUNT_ID   = os.environ.get("DATABRICKS_ACCOUNT_ID", "")

if not DATABRICKS_ACCOUNT_HOST or not DATABRICKS_ACCOUNT_ID:
    print(
        "\nERROR: Set DATABRICKS_ACCOUNT_HOST and DATABRICKS_ACCOUNT_ID before running.\n"
        "See create_groups.py for details.\n"
    )
    sys.exit(1)

DEMO_GROUPS = [
    "analysts",
    "data-admins",
    "data-consumers",
    "data-engineers",
    "etl-service-principal",
    "ml-engineers",
    "contractors",
]


def delete_demo_groups(a: AccountClient) -> None:
    group_map = {g.display_name: g.id for g in a.groups.list()}
    for name in DEMO_GROUPS:
        group_id = group_map.get(name)
        if group_id is None:
            print(f"  [skip]    not found: {name}")
            continue
        a.groups.delete(id=group_id)
        print(f"  [deleted] {name}")


if __name__ == "__main__":
    a = AccountClient(host=DATABRICKS_ACCOUNT_HOST, account_id=DATABRICKS_ACCOUNT_ID)
    print("Removing demo account-level groups...\n")
    delete_demo_groups(a)
    print("\nDone.")
