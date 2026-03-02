-- =============================================================================
-- Lesson 1.1: Unity Catalog Overview
-- Creating Tables, Volumes, and Inspecting Objects
-- =============================================================================
-- Tables in Unity Catalog are Delta tables by default.
-- Volumes provide a governed path for unstructured files (CSV, JSON, images, etc.)
-- Both live within a catalog.schema namespace and appear in the lineage graph.
-- =============================================================================

USE CATALOG GovernanceCatalog;

-- ── Bronze layer: raw event ingest ──────────────────────────────────────────

CREATE TABLE IF NOT EXISTS GovernanceCatalog.bronze.raw_events (
  event_id    STRING    NOT NULL COMMENT 'Unique identifier for the event',
  event_time  TIMESTAMP           COMMENT 'UTC timestamp when the event occurred',
  source      STRING              COMMENT 'System or service that produced the event',
  payload     STRING              COMMENT 'Raw JSON payload from the source system'
)
USING DELTA
COMMENT 'Bronze-layer raw events — full fidelity, no transformations applied'
TBLPROPERTIES ('delta.enableChangeDataFeed' = 'true');

-- ── Silver layer: validated and typed ────────────────────────────────────────

CREATE TABLE IF NOT EXISTS GovernanceCatalog.silver.events_clean (
  event_id    STRING    NOT NULL COMMENT 'Unique identifier for the event',
  event_time  TIMESTAMP NOT NULL COMMENT 'UTC timestamp when the event occurred',
  source      STRING    NOT NULL COMMENT 'System or service that produced the event',
  event_type  STRING              COMMENT 'Parsed event type from the payload',
  user_id     STRING              COMMENT 'User associated with the event, if present'
)
USING DELTA
COMMENT 'Silver-layer events — deduplicated, typed, and null-checked';

-- ── Gold layer: business metric aggregation ───────────────────────────────────

CREATE TABLE IF NOT EXISTS GovernanceCatalog.gold.daily_event_counts (
  event_date  DATE      NOT NULL COMMENT 'Calendar date of the events',
  source      STRING    NOT NULL COMMENT 'System or service that produced the events',
  event_type  STRING    NOT NULL COMMENT 'Parsed event type',
  event_count BIGINT              COMMENT 'Number of events for this date/source/type'
)
USING DELTA
COMMENT 'Gold-layer daily event counts — pre-aggregated for dashboard queries';

-- ── Volume: unstructured file storage under Unity Catalog governance ──────────

CREATE VOLUME IF NOT EXISTS GovernanceCatalog.bronze.raw_files
  COMMENT 'Landing zone for raw CSV and JSON files before pipeline ingestion';

-- ── Inspection commands ───────────────────────────────────────────────────────

-- List all tables in a schema
SHOW TABLES IN GovernanceCatalog.bronze;
SHOW TABLES IN GovernanceCatalog.silver;
SHOW TABLES IN GovernanceCatalog.gold;

-- List volumes in a schema
SHOW VOLUMES IN GovernanceCatalog.bronze;

-- Describe a table's full schema and metadata
DESCRIBE TABLE EXTENDED GovernanceCatalog.silver.events_clean;
