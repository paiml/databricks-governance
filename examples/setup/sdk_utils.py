# =============================================================================
# examples/setup/sdk_utils.py
# Shared helper for executing SQL via the Databricks SDK.
# Imported by every Python sidecar in examples/.
# =============================================================================
# Prerequisites:
#   export DATABRICKS_HOST=https://<workspace>.azuredatabricks.net
#   export DATABRICKS_TOKEN=<personal-access-token>
#   export DATABRICKS_WAREHOUSE_ID=<sql-warehouse-id>
#
# Find the warehouse ID in:
#   Databricks UI → SQL Warehouses → <warehouse> → Connection details
# =============================================================================

import os
import sys

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.sql import StatementState

WAREHOUSE_ID = os.environ.get("DATABRICKS_WAREHOUSE_ID", "")

if not WAREHOUSE_ID:
    print(
        "\nERROR: DATABRICKS_WAREHOUSE_ID is not set.\n"
        "Export it before running any example:\n\n"
        "  export DATABRICKS_WAREHOUSE_ID=<id>\n\n"
        "Find the ID: Databricks UI → SQL Warehouses → <warehouse> → Connection details\n"
    )
    sys.exit(1)

w = WorkspaceClient()


def _format_results(response) -> str:
    """Return a formatted string table for a statement execution response."""
    if not (response.result and response.result.data_array):
        return ""

    rows = response.result.data_array
    cols: list[str] = []
    if (
        response.manifest
        and response.manifest.schema
        and response.manifest.schema.columns
    ):
        cols = [c.name for c in response.manifest.schema.columns]

    widths = [len(c) for c in cols]
    for row in rows:
        for i, val in enumerate(row):
            if i < len(widths):
                widths[i] = max(widths[i], len(str(val or "")))

    lines: list[str] = []
    if cols:
        header = "  " + " | ".join(c.ljust(widths[i]) for i, c in enumerate(cols))
        lines.append(header)
        lines.append("  " + "-" * (len(header) - 2))

    for row in rows:
        lines.append(
            "  " + " | ".join(
                str(v or "").ljust(widths[i]) if i < len(widths) else str(v or "")
                for i, v in enumerate(row)
            )
        )

    row_word = "row" if len(rows) == 1 else "rows"
    lines.append(f"\n  ({len(rows)} {row_word})")
    return "\n".join(lines)


def run_sql(statement: str, description: str = "") -> bool:
    """Execute one SQL statement against the configured warehouse.

    Prints the description, a one-line preview of the SQL, the result table
    (if any), and an OK / FAILED status line.  Returns True on success.
    """
    if description:
        print(f"\n-- {description}")

    preview = statement.strip().splitlines()[0]
    print(f"   {preview}")

    response = w.statement_execution.execute_statement(
        warehouse_id=WAREHOUSE_ID,
        statement=statement.strip(),
        wait_timeout="60s",
    )

    if response.status.state == StatementState.FAILED:
        error_msg = (
            response.status.error.message
            if response.status.error
            else "unknown error"
        )
        print(f"   [FAILED] {error_msg}\n")
        return False

    table = _format_results(response)
    if table:
        print(table)

    print("   [OK]")
    return True
