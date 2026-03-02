# Lab 3: Data Lineage

## Objectives

- Understand how Unity Catalog captures lineage automatically
- Query the `system.lineage` and `system.access` system tables
- Use lineage data to answer compliance questions (e.g., "who touched this data?")
- Identify all downstream consumers of a sensitive column

## Prerequisites

- Completed Lab 1 and Lab 2
- Metastore admin or a user with `SELECT` granted on `system.access` and `system.lineage` schemas

## Background

Unity Catalog captures lineage for every read and write operation across SQL, Python, Scala, and R — without any instrumentation on your part. Every time a notebook runs, a job executes, or a query completes, Databricks records which tables and columns were read and which were written. This data is stored in system tables that you can query with standard SQL.

System schemas are not enabled by default. An admin must run:

```sql
-- Enable the system schemas (run once as metastore admin)
ALTER SYSTEM ENABLE SCHEMA lineage;
ALTER SYSTEM ENABLE SCHEMA access;
```

## Exercise 1: Enable System Table Access

1. As a metastore admin, run the `ALTER SYSTEM ENABLE SCHEMA` commands above
2. Grant your demo user access to the system tables (see the first section of [`examples/lineage/query_lineage.sql`](../examples/lineage/query_lineage.sql))
3. Verify access by running `SELECT COUNT(*) FROM system.lineage.table_lineage`

## Exercise 2: Query Table Lineage

Review [`examples/lineage/query_lineage.sql`](../examples/lineage/query_lineage.sql).

1. Run the "upstream sources" query for `GovernanceCatalog.silver.events_clean`
2. Run the "downstream consumers" query for `GovernanceCatalog.gold.daily_event_counts`

### Questions

1. What does it mean if a table appears in `system.lineage.table_lineage` but was never queried through a SQL warehouse? (Hint: lineage is captured across all runtimes)
2. How would you find all tables written by a specific service principal in the last week?

## Exercise 3: Column-Level Lineage for PII Compliance

1. Run the column lineage query that traces `user_id` in `silver.events_clean` back to its origin
2. Run the downstream query that finds every table containing data derived from the `payload` column in `bronze.raw_events`

This answers the compliance question: **"If the `payload` column contains PII, which downstream tables may also expose it?"**

### What to Observe

- Column lineage traces individual columns through transformations — not just tables
- The result is a map of PII propagation across your entire data platform

## Exercise 4: Audit Log Queries

1. Run the query that shows who accessed `silver.events_clean` in the last 7 days
2. Run the query that detects `DROP TABLE` or `DROP SCHEMA` events in the last 30 days

### Questions

1. What action names appear in `system.access.audit` for read vs. write operations?
2. How would you build a daily report of all schema drop operations to send to your security team?

## Key Takeaways

- Unity Catalog lineage is automatic — no code changes required
- `system.lineage.table_lineage` and `system.lineage.column_lineage` power impact analysis
- `system.access.audit` powers security investigations and compliance reporting
- Column-level lineage is essential for answering "where does this PII appear downstream?"
