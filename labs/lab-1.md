# Lab 1: Unity Catalog Setup

## Objectives

- Understand the Unity Catalog three-level namespace (metastore → catalog → schema → table)
- Create a catalog, schemas, and Delta tables using SQL
- Explore the Unity Catalog UI and verify objects were created correctly
- Create a Volume for unstructured file storage

## Prerequisites

- A Databricks workspace with Unity Catalog enabled (all new workspaces since November 2023)
- Account admin or metastore admin role, OR a workspace admin who has granted you `CREATE CATALOG`

## Background

Before Unity Catalog, every Databricks workspace had its own isolated Hive metastore. This made it impossible to enforce consistent policies or track data usage across workspaces. Unity Catalog provides a **single governance layer** across all workspaces in a region — one place to define who can see what, with audit logs and lineage captured automatically.

The object hierarchy:

```
Metastore (one per region)
└── Catalog  (maps to a business unit or environment)
    └── Schema  (maps to a team, project, or data layer)
        ├── Table / View
        └── Volume  (for unstructured files)
```

## Exercise 1: Create a Catalog

Review [`examples/unity/create_catalog.sql`](../examples/unity/create_catalog.sql).

1. Open a SQL editor in your Databricks workspace (**SQL > SQL Editor**)
2. Run each statement in the file
3. Verify the catalog appears in the **Catalog Explorer** (left sidebar → Data)

### Questions

1. What privilege is required to create a catalog?
2. What does `SHOW CATALOGS` return in your workspace?
3. What is the difference between `USE CATALOG` and `SELECT current_catalog()`?

## Exercise 2: Create Schemas and Tables

Review [`examples/unity/create_schemas.sql`](../examples/unity/create_schemas.sql) and [`examples/unity/create_tables.sql`](../examples/unity/create_tables.sql).

1. Run `create_schemas.sql` to create the `bronze`, `silver`, `gold`, and `ml` schemas
2. Run `create_tables.sql` to create tables in those schemas
3. In the Catalog Explorer, navigate to `GovernanceCatalog > bronze` and verify the table and volume appear

### What to Observe

- Tables in Unity Catalog are Delta format by default — no `USING DELTA` is required (but it's explicit)
- Volumes appear alongside tables in the same schema
- `DESCRIBE TABLE EXTENDED` shows the table owner, created-by user, and creation time

## Exercise 3: Explore the Catalog Explorer

1. Navigate to **Data > Catalog Explorer** in the left sidebar
2. Find your `GovernanceCatalog` catalog
3. Click on `bronze.raw_events` and observe:
   - Schema (columns and types)
   - Details (owner, created time, table format)
   - Permissions tab (currently empty — you will populate this in Lab 2)
   - History tab (Delta transaction log entries)
   - Sample Data tab

## Key Takeaways

- Unity Catalog uses a three-level namespace: `catalog.schema.table`
- `CREATE CATALOG` is a privileged operation — standard users need `CREATE CATALOG` granted to them
- Schemas are logical containers for tables, views, and volumes within a catalog
- Volumes provide a governed path for unstructured files, just like tables provide governed structured storage
- All objects created in Unity Catalog are automatically tracked in the lineage graph
