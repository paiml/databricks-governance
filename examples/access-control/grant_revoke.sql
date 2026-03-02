-- =============================================================================
-- Lesson 1.4: Access Control
-- Writing GRANT and REVOKE Statements
-- =============================================================================
-- Unity Catalog uses ANSI SQL privilege syntax.
-- Privileges cascade down the hierarchy: granting USE CATALOG allows a principal
-- to see the catalog, but you still need to grant USE SCHEMA and SELECT/MODIFY
-- on the objects inside.
-- =============================================================================

-- ── Catalog-level privileges ──────────────────────────────────────────────────

-- Allow a group to discover the catalog (required before any schema-level grants)
GRANT USE CATALOG ON CATALOG GovernanceCatalog TO `data-consumers`;

-- Allow a service principal to create new schemas in the catalog
GRANT CREATE SCHEMA ON CATALOG GovernanceCatalog TO `etl-service-principal`;

-- ── Schema-level privileges ───────────────────────────────────────────────────

-- Allow analysts to query everything in the silver schema
GRANT USE SCHEMA, SELECT ON SCHEMA GovernanceCatalog.silver TO `analysts`;

-- Allow the ETL pipeline identity to read and write the bronze schema
GRANT USE SCHEMA, SELECT, MODIFY ON SCHEMA GovernanceCatalog.bronze TO `etl-service-principal`;

-- Allow the ML team to read gold tables and write to the ml schema
GRANT USE SCHEMA, SELECT ON SCHEMA GovernanceCatalog.gold TO `ml-engineers`;
GRANT USE SCHEMA, SELECT, MODIFY, CREATE TABLE ON SCHEMA GovernanceCatalog.ml TO `ml-engineers`;

-- ── Table-level privileges ────────────────────────────────────────────────────

-- Grant the current user (you) read access to one specific table only
-- Replace current_user() with a real email when demonstrating to a class
GRANT SELECT ON TABLE GovernanceCatalog.gold.daily_event_counts TO current_user();

-- Allow the analysts group to query the gold layer (illustrates a service-principal grant)
-- In production you would use: GRANT SELECT ... TO `<service-principal-app-id>`;
GRANT SELECT ON TABLE GovernanceCatalog.gold.daily_event_counts TO `analysts`;

-- ── Revoking access ───────────────────────────────────────────────────────────

-- Remove the current user's direct table grant (mirrors the GRANT above)
REVOKE SELECT ON TABLE GovernanceCatalog.gold.daily_event_counts FROM current_user();

-- Remove a group's schema-level access entirely
REVOKE USE SCHEMA, SELECT ON SCHEMA GovernanceCatalog.silver FROM `contractors`;

-- ── Inspecting existing privileges ────────────────────────────────────────────

-- Show who has access to a specific table
SHOW GRANTS ON TABLE GovernanceCatalog.silver.events_clean;

-- Show what privileges a specific principal holds across the catalog
SHOW GRANTS `analysts` ON SCHEMA GovernanceCatalog.silver;
