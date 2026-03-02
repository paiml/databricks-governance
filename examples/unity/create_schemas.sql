-- =============================================================================
-- Lesson 1.1: Unity Catalog Overview
-- Creating Schemas (Databases) That Mirror Data Layers
-- =============================================================================
-- Schemas are the second level of the Unity Catalog hierarchy.
-- A common pattern is to create one schema per medallion layer (bronze/silver/gold)
-- or one schema per team/project within a catalog.
-- =============================================================================

USE CATALOG GovernanceCatalog;

-- Create schemas that mirror your data layers
CREATE SCHEMA IF NOT EXISTS GovernanceCatalog.bronze
  COMMENT 'Raw ingested data — untransformed, append-only';

CREATE SCHEMA IF NOT EXISTS GovernanceCatalog.silver
  COMMENT 'Cleaned and validated data — conformed types and deduplication applied';

CREATE SCHEMA IF NOT EXISTS GovernanceCatalog.gold
  COMMENT 'Business-ready aggregations and feature tables';

-- Create a schema for ML artifacts (models, feature tables, evaluation results)
CREATE SCHEMA IF NOT EXISTS GovernanceCatalog.ml
  COMMENT 'MLflow models, feature tables, and evaluation results';

-- List all schemas in the catalog
SHOW SCHEMAS IN GovernanceCatalog;

-- Inspect a schema's metadata
DESCRIBE SCHEMA GovernanceCatalog.silver;
