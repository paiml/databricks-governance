# Examples

Code examples for each module of the Production Governance and MLOps with Databricks course.

> **Note on namespaces:** SQL examples use `GovernanceCatalog` as the demonstration catalog name. Replace it with your actual catalog name before running.

## Directory Structure

| Directory | Description | Course Lesson |
|-----------|-------------|---------------|
| `unity/` | Create catalogs, schemas, tables, and volumes | 1.1 Unity Catalog Overview |
| `access-control/` | GRANT/REVOKE and permission model design | 1.4 Access Control |
| `lineage/` | Query lineage and audit data from system tables | 1.6 Data Lineage |
| `repos/` | GitHub Actions workflow for Databricks Repos | 2.1 Databricks Repos |
| `cicd/` | Multi-environment CI/CD for notebook promotion | 2.3 CI/CD for Notebooks |
| `mlops/` | MLflow training, registration, and registry promotion | 2.6 ML Model CI/CD |
| `monitoring/` | Lakehouse Monitoring table monitors and alerts | 3.1 Lakehouse Monitoring |
| `ml-monitoring/` | Inference table drift detection | 3.3 ML Model Monitoring |
| `secrets/` | Secret scopes and cloud vault integration | 3.6 Secrets Management |

## Running SQL Examples

SQL files are designed to run in a **Databricks SQL warehouse** or a notebook connected to a cluster:

1. Open a SQL editor or notebook in your Databricks workspace
2. Paste or import the `.sql` file
3. Update catalog/schema names to match your environment
4. Run each statement in order (statements are separated by semicolons)

## Setup (run first)

Run `examples/setup/setup.sql` once in the **Databricks SQL console** before executing any other examples. It creates the catalog, all schemas, all tables, and the volume in a single pass — all statements use `IF NOT EXISTS` so it is safe to re-run.

Alternatively, use the Python scripts if you prefer the SDK:

```bash
python examples/setup/setup_catalog.py   # creates GovernanceCatalog + all schemas
python examples/setup/create_groups.py   # creates demo workspace groups
```

## Running Python Examples

Python files are designed to run as **Databricks notebooks**:

1. Import the `.py` file into your Databricks workspace
2. Attach to a cluster with the required libraries (MLflow, Delta Lake)
3. Run cells top to bottom
4. Update any hardcoded paths or catalog names to match your environment
