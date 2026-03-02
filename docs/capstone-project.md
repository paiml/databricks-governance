# Capstone Project: End-to-End Governance Platform

## Overview

In this capstone project, you will design and implement a production-ready governance layer for a data platform of your choice. Drawing on all three weeks of the course, you will combine Unity Catalog access control, CI/CD pipelines, MLflow model management, Lakehouse Monitoring, and secrets management into a cohesive system.

## Project Requirements

### Week 1 Requirements (Governance Foundation)

1. **Catalog and Schema Design**
   - Create a catalog with at least three schemas (e.g., `bronze`, `silver`, `gold` or equivalent)
   - Define at least two Delta tables per layer with meaningful column comments
   - Create at least one Volume for unstructured file storage

2. **Access Control**
   - Define at least three groups representing distinct organizational roles (e.g., `analysts`, `data-engineers`, `ml-team`)
   - Write a complete GRANT model that applies least privilege across all schemas
   - Implement at least one column mask or row filter on a table containing simulated PII

3. **Lineage Verification**
   - Run at least two write operations (e.g., `INSERT INTO`) and one transformation (e.g., `CREATE TABLE AS SELECT`)
   - Query `system.lineage.table_lineage` and document the captured lineage graph
   - Query `system.access.audit` to verify that read access is being logged

### Week 2 Requirements (CI/CD and MLflow)

4. **Databricks Repos Integration**
   - Connect your project repository to a Databricks workspace via Repos
   - Configure a GitHub Actions workflow (or equivalent) that updates the workspace Repo on push

5. **ML Model Lifecycle**
   - Train a model on a dataset of your choice and log it to MLflow with `autolog()`
   - Register the model in the Unity Catalog-backed Model Registry
   - Write a validation script that checks at least one metric against a threshold
   - Promote the validated model to a `champion` alias

### Week 3 Requirements (Monitoring and Security)

6. **Lakehouse Monitoring**
   - Attach a snapshot monitor to at least one silver-layer table
   - Query the generated profile metrics table and document the null rates and cardinality for at least three columns
   - Design (or implement) a SQL alert that would fire when a null rate exceeds 5%

7. **ML Model Monitoring**
   - Attach an inference log monitor to your model's inference table (real or simulated)
   - Query the drift metrics table after at least two refresh windows
   - Document the drift threshold you would use to trigger retraining

8. **Secrets Management**
   - Create a Databricks-backed secret scope
   - Store at least one credential (e.g., a JDBC connection string or API key)
   - Retrieve the secret in a notebook using `dbutils.secrets.get()` and verify it is redacted in output

## Deliverables

Submit a single compressed archive (`.zip` or `.tar.gz`) containing:

1. **SQL scripts** — all `CREATE`, `GRANT`, and lineage verification queries
2. **Python notebooks** — MLflow training, validation, and promotion scripts
3. **GitHub Actions YAML** — CI/CD workflow file
4. **Monitoring report** — Markdown document with:
   - Screenshot or query result of the profile metrics table
   - Screenshot or query result of the drift metrics table
   - Description of the alerting strategy you designed
5. **Architecture diagram** — A diagram (any tool) showing:
   - Catalog → schema → table hierarchy
   - Access control groups and their privileges
   - CI/CD flow from development to production
   - Monitoring and alerting flow

## Evaluation Rubric

| Criterion | Points |
|-----------|--------|
| Catalog and schema design correctness | 15 |
| Access control model completeness and correctness | 20 |
| Column mask or row filter implementation | 10 |
| Lineage verification queries | 10 |
| MLflow model training and registration | 15 |
| Model validation and promotion logic | 10 |
| Lakehouse Monitoring setup and query | 10 |
| Secrets management implementation | 5 |
| Architecture diagram clarity | 5 |
| **Total** | **100** |

## Tips

- Use the examples in this repository as starting points — adapt them to your chosen dataset and business scenario
- The example dataset in `data/` provides a simple starting point if you do not have your own data
- For local development, MLflow can be run locally with `mlflow ui` before pushing to Databricks
- Document every decision — "why" is more important than "what" for the access control and monitoring sections
