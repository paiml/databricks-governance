# Lab 2: Access Control

## Objectives

- Understand Unity Catalog's principal model (users, groups, service principals)
- Write GRANT and REVOKE statements using ANSI SQL syntax
- Design a least-privilege permission model for a multi-team environment
- Apply column masks and row filters for fine-grained data protection

## Prerequisites

- Completed Lab 1 (GovernanceCatalog with schemas and tables created)
- Workspace admin or metastore admin role to grant privileges

## Background

Unity Catalog's permission model follows ANSI SQL standards — if you know how to write `GRANT SELECT ON TABLE foo TO bar`, you already know the syntax. The key concepts to internalize are:

- **Principals**: users, groups (recommended), and service principals
- **Privilege inheritance**: permissions cascade downward (granting `SELECT` on a schema grants it on all current tables, but not future ones unless you also grant `CREATE`)
- **Least privilege**: grant only what is needed, prefer groups over individuals, prefer schema-level grants over table-by-table grants

## Exercise 1: Grant and Revoke Basic Privileges

Review [`examples/access-control/grant_revoke.sql`](../examples/access-control/grant_revoke.sql).

1. In the SQL Editor, run the catalog-level grants at the top of the file
2. Run the schema-level grants for `analysts` and `etl-service-principal`
3. Verify the grants using `SHOW GRANTS ON SCHEMA GovernanceCatalog.silver`

### Questions

1. Why do you need to grant `USE CATALOG` before any schema-level grant?
2. What is the difference between `MODIFY` and `CREATE TABLE` on a schema?
3. After revoking a group's access to a schema, can individual users in that group still access it via direct table grants?

## Exercise 2: Design a Permission Model

Review [`examples/access-control/permission_model.sql`](../examples/access-control/permission_model.sql).

This script builds a full permission model with:
- Group-based grants at catalog, schema, and table levels
- A **column mask** that redacts email addresses for non-admin users
- A **row filter** that limits analysts to the last 90 days of data

1. Run the grants section (Steps 1–4)
2. Run the column mask function and `ALTER TABLE` statement
3. Run the row filter function and `ALTER TABLE` statement
4. Query `GovernanceCatalog.silver.events_clean` with two different identities (use impersonation or a test account) to verify the mask and filter are applied

### What to Observe

- Admin users see the full email; non-admin users see `a***@company.com`
- Non-admin, non-engineer users only see events within the last 90 days
- The masks and filters are enforced at query time — no changes to the underlying data

## Exercise 3: Audit the Permission Model

1. Run `SHOW GRANTS ON CATALOG GovernanceCatalog` — observe which principals have which privileges
2. Run `SHOW GRANTS ON SCHEMA GovernanceCatalog.silver` — observe schema-level grants
3. Run `SHOW GRANTS ON TABLE GovernanceCatalog.silver.events_clean` — observe table-level grants

### Questions

1. Which query shows you the combined effective permissions for a specific user?
2. How would you find all tables a specific service principal can read?

## Key Takeaways

- Always grant `USE CATALOG` before schema-level grants, and `USE SCHEMA` before table-level grants
- Prefer granting to groups — when a person leaves, you remove them from the group, not from every table
- Column masks and row filters enforce policy at query time without duplicating data
- `SHOW GRANTS` is your audit tool — run it regularly to catch permission drift
