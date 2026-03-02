-- =============================================================================
-- Lesson 1.4: Access Control
-- Designing a Permission Model for Real-World Teams
-- =============================================================================
-- This script demonstrates a least-privilege permission model built around
-- groups rather than individual users, using row filters and column masks
-- for fine-grained data protection.
-- =============================================================================

-- ── Step 1: Grant catalog access to all teams (required for any deeper access) ─

GRANT USE CATALOG ON CATALOG GovernanceCatalog
  TO `data-consumers`, `ml-engineers`, `etl-service-principal`, `data-admins`;

-- ── Step 2: Grant bronze access only to the ETL identity ──────────────────────

GRANT USE SCHEMA, SELECT, MODIFY ON SCHEMA GovernanceCatalog.bronze
  TO `etl-service-principal`;

-- ── Step 3: Grant silver access to engineers and read-only to analysts ─────────

GRANT USE SCHEMA, SELECT, MODIFY ON SCHEMA GovernanceCatalog.silver
  TO `data-engineers`;

GRANT USE SCHEMA, SELECT ON SCHEMA GovernanceCatalog.silver
  TO `analysts`;

-- ── Step 4: Grant gold access broadly — this layer is designed for consumption ─

GRANT USE SCHEMA, SELECT ON SCHEMA GovernanceCatalog.gold
  TO `data-consumers`, `analysts`, `ml-engineers`;

-- ── Step 5: Column mask for PII — hide raw email in silver for non-admins ───────

-- Create a masking function (requires Unity Catalog-enabled workspace)
CREATE OR REPLACE FUNCTION GovernanceCatalog.silver.mask_email(email STRING)
  RETURNS STRING
  RETURN CASE
    WHEN is_account_group_member('data-admins') THEN email
    ELSE regexp_replace(email, '(.).+(@.+)', '$1***$2')
  END;

-- Attach the mask to the column
ALTER TABLE GovernanceCatalog.silver.events_clean
  ALTER COLUMN user_id
  SET MASK GovernanceCatalog.silver.mask_email;

-- ── Step 6: Row filter — analysts only see events from the last 90 days ─────────

CREATE OR REPLACE FUNCTION GovernanceCatalog.silver.recent_events_only(event_time TIMESTAMP)
  RETURNS BOOLEAN
  RETURN CASE
    WHEN is_account_group_member('data-admins') THEN TRUE
    WHEN is_account_group_member('data-engineers') THEN TRUE
    ELSE event_time >= current_timestamp() - INTERVAL 90 DAYS
  END;

ALTER TABLE GovernanceCatalog.silver.events_clean
  SET ROW FILTER GovernanceCatalog.silver.recent_events_only ON (event_time);

-- ── Audit: verify the model looks correct ────────────────────────────────────

SHOW GRANTS ON CATALOG GovernanceCatalog;
SHOW GRANTS ON SCHEMA GovernanceCatalog.silver;
SHOW GRANTS ON TABLE GovernanceCatalog.silver.events_clean;
