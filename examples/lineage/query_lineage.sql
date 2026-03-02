-- =============================================================================
-- Lesson 1.6: Data Lineage
-- Querying Unity Catalog System Tables for Lineage and Audit Data
-- =============================================================================
-- Unity Catalog automatically captures lineage for every read and write
-- across all supported languages (SQL, Python, Scala, R).
-- Lineage data is surfaced in system.access and system.lineage schemas.
-- You must be a metastore admin or have SELECT granted on system schemas
-- before running these queries.
-- =============================================================================

-- ── Enable access to system tables (run once as metastore admin) ──────────────

-- Grant the analysts group read access to the access and lineage system schemas
GRANT USE SCHEMA ON SCHEMA system.access TO `data-admins`;
GRANT SELECT ON TABLE system.access.audit TO `data-admins`;

GRANT USE SCHEMA ON SCHEMA system.lineage TO `data-admins`;
GRANT SELECT ON TABLE system.lineage.table_lineage TO `data-admins`;
GRANT SELECT ON TABLE system.lineage.column_lineage TO `data-admins`;

-- ── Table-level lineage ───────────────────────────────────────────────────────

-- Show all upstream sources that write into the silver events_clean table
SELECT
  source_table_full_name,
  target_table_full_name,
  created_by,
  event_time
FROM system.lineage.table_lineage
WHERE target_table_full_name = 'GovernanceCatalog.silver.events_clean'
ORDER BY event_time DESC
LIMIT 50;

-- Show all downstream consumers of the gold daily_event_counts table
SELECT
  source_table_full_name,
  target_table_full_name,
  created_by,
  event_time
FROM system.lineage.table_lineage
WHERE source_table_full_name = 'GovernanceCatalog.gold.daily_event_counts'
ORDER BY event_time DESC
LIMIT 50;

-- ── Column-level lineage ──────────────────────────────────────────────────────

-- Trace where the user_id column in silver.events_clean originates
SELECT
  source_table_full_name,
  source_column_name,
  target_table_full_name,
  target_column_name,
  event_time
FROM system.lineage.column_lineage
WHERE
  target_table_full_name = 'GovernanceCatalog.silver.events_clean'
  AND target_column_name = 'user_id'
ORDER BY event_time DESC;

-- ── Audit log queries ─────────────────────────────────────────────────────────

-- Who accessed the silver events_clean table in the last 7 days?
SELECT
  user_identity.email   AS user_email,
  action_name,
  request_params.table  AS table_name,
  event_time
FROM system.access.audit
WHERE
  action_name IN ('selectTable', 'describeTable')
  AND request_params.table LIKE '%events_clean%'
  AND event_time >= current_timestamp() - INTERVAL 7 DAYS
ORDER BY event_time DESC;

-- Detect any DROP TABLE or DROP SCHEMA events in the last 30 days
SELECT
  user_identity.email AS user_email,
  action_name,
  request_params,
  event_time
FROM system.access.audit
WHERE
  action_name IN ('deleteTable', 'deleteSchema', 'deleteCatalog')
  AND event_time >= current_timestamp() - INTERVAL 30 DAYS
ORDER BY event_time DESC;

-- ── Data lineage for compliance: find all tables containing a PII column ──────

-- Identify every table downstream of the raw user_id source column
SELECT DISTINCT
  target_table_full_name,
  target_column_name
FROM system.lineage.column_lineage
WHERE
  source_table_full_name = 'GovernanceCatalog.bronze.raw_events'
  AND source_column_name = 'payload'   -- payload may contain user identifiers
ORDER BY target_table_full_name;
