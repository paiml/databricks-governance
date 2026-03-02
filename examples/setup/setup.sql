-- =============================================================================
-- Course Setup: GovernanceCatalog — run this once in the Databricks SQL console
-- before executing any other examples.
-- =============================================================================
-- Requires: CREATE CATALOG privilege on the metastore.
-- All objects use IF NOT EXISTS so this script is safe to re-run.
-- =============================================================================

-- ── Catalog ───────────────────────────────────────────────────────────────────

CREATE CATALOG IF NOT EXISTS GovernanceCatalog
  COMMENT 'Demonstration catalog for the Production Governance and MLOps course';

-- ── Schemas ───────────────────────────────────────────────────────────────────

CREATE SCHEMA IF NOT EXISTS GovernanceCatalog.bronze
  COMMENT 'Raw ingest layer — full fidelity, no transformations';

CREATE SCHEMA IF NOT EXISTS GovernanceCatalog.silver
  COMMENT 'Validated and typed layer — deduplicated and null-checked';

CREATE SCHEMA IF NOT EXISTS GovernanceCatalog.gold
  COMMENT 'Pre-aggregated business metrics for dashboards and reporting';

CREATE SCHEMA IF NOT EXISTS GovernanceCatalog.ml
  COMMENT 'ML models, inference tables, and training datasets';

CREATE SCHEMA IF NOT EXISTS GovernanceCatalog.monitoring
  COMMENT 'Lakehouse Monitoring output tables (profile and drift metrics)';

-- ── Bronze tables ─────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS GovernanceCatalog.bronze.raw_events (
  event_id    STRING    NOT NULL COMMENT 'Unique identifier for the event',
  event_time  TIMESTAMP           COMMENT 'UTC timestamp when the event occurred',
  source      STRING              COMMENT 'System or service that produced the event',
  payload     STRING              COMMENT 'Raw JSON payload from the source system'
)
USING DELTA
COMMENT 'Bronze-layer raw events — full fidelity, no transformations applied'
TBLPROPERTIES ('delta.enableChangeDataFeed' = 'true');

-- ── Silver tables ─────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS GovernanceCatalog.silver.events_clean (
  event_id    STRING    NOT NULL COMMENT 'Unique identifier for the event',
  event_time  TIMESTAMP NOT NULL COMMENT 'UTC timestamp when the event occurred',
  source      STRING    NOT NULL COMMENT 'System or service that produced the event',
  event_type  STRING              COMMENT 'Parsed event type from the payload',
  user_id     STRING              COMMENT 'User associated with the event, if present'
)
USING DELTA
COMMENT 'Silver-layer events — deduplicated, typed, and null-checked';

-- ── Gold tables ───────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS GovernanceCatalog.gold.daily_event_counts (
  event_date  DATE      NOT NULL COMMENT 'Calendar date of the events',
  source      STRING    NOT NULL COMMENT 'System or service that produced the events',
  event_type  STRING    NOT NULL COMMENT 'Parsed event type',
  event_count BIGINT              COMMENT 'Number of events for this date/source/type'
)
USING DELTA
COMMENT 'Gold-layer daily event counts — pre-aggregated for dashboard queries';

-- ── ML tables ─────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS GovernanceCatalog.ml.event_classifier_inference (
  request_id      STRING    NOT NULL  COMMENT 'Unique serving request identifier',
  timestamp       TIMESTAMP NOT NULL  COMMENT 'UTC time the prediction was made',
  sepal_length_cm DOUBLE              COMMENT 'Input feature',
  sepal_width_cm  DOUBLE              COMMENT 'Input feature',
  petal_length_cm DOUBLE              COMMENT 'Input feature',
  petal_width_cm  DOUBLE              COMMENT 'Input feature',
  prediction      INT                 COMMENT 'Model output class label (0, 1, or 2)',
  ground_truth    INT                 COMMENT 'Actual label — populated after feedback loop'
)
USING DELTA
COMMENT 'Inference log written by the model serving endpoint'
TBLPROPERTIES ('delta.enableChangeDataFeed' = 'true');

CREATE TABLE IF NOT EXISTS GovernanceCatalog.ml.event_classifier_training_baseline
USING DELTA
COMMENT 'Training-split baseline used for drift comparison in Lakehouse Monitoring'
AS
SELECT
  sepal_length_cm,
  sepal_width_cm,
  petal_length_cm,
  petal_width_cm,
  prediction,
  ground_truth
FROM GovernanceCatalog.ml.event_classifier_inference
LIMIT 0;  -- empty schema-only baseline; populate with your actual training data

-- ── Volume ────────────────────────────────────────────────────────────────────

CREATE VOLUME IF NOT EXISTS GovernanceCatalog.bronze.raw_files
  COMMENT 'Landing zone for raw CSV and JSON files before pipeline ingestion';

-- ── Grants ────────────────────────────────────────────────────────────────────
-- The user who runs this script owns GovernanceCatalog and already has full
-- access. Use the statements below to grant access to other principals.
-- Replace `user@company.com` with a real user email or group name.

-- GRANT USE CATALOG ON CATALOG GovernanceCatalog TO `user@company.com`;

-- GRANT USE SCHEMA, SELECT          ON SCHEMA GovernanceCatalog.gold   TO `user@company.com`;
-- GRANT USE SCHEMA, SELECT          ON SCHEMA GovernanceCatalog.silver TO `user@company.com`;
-- GRANT USE SCHEMA, SELECT, MODIFY  ON SCHEMA GovernanceCatalog.bronze TO `user@company.com`;
