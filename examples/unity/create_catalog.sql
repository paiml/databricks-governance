-- =============================================================================
-- Lesson 1.1: Unity Catalog Overview
-- Creating and Inspecting a Catalog
-- =============================================================================
-- Unity Catalog uses a three-level namespace: catalog.schema.table
-- A catalog is the top-level container — think of it as a database server
-- that maps to a business unit, environment (dev/prod), or project boundary.
-- =============================================================================

-- Create a new catalog for this course
-- Requires: metastore admin or CREATE CATALOG privilege
CREATE CATALOG IF NOT EXISTS GovernanceCatalog
  COMMENT 'Demonstration catalog for the Governance and MLOps course';

-- Inspect the catalog just created
DESCRIBE CATALOG GovernanceCatalog;

-- List all catalogs the current user can see
SHOW CATALOGS;

-- Switch the default catalog for the session
USE CATALOG GovernanceCatalog;

-- Verify the active catalog
SELECT current_catalog();
