# Capstone Project: End-to-End Governance Platform

## Overview

In this capstone project you will design and implement a governance layer for a Databricks workspace. Drawing on all three weeks of the course, you will combine Unity Catalog access control, automated CI/CD pipelines, and Lakehouse Monitoring into a cohesive system.

## Project Requirements

### Week 1 Requirements (Governance Foundation)

1. **Catalog and Schema Design**
   - Create a catalog with at least three schemas (e.g., `bronze`, `silver`, `gold` or equivalent)
   - Define at least two Delta tables per layer with meaningful column comments
   - Create at least one Volume for unstructured file storage

2. **Service Principal and Access Control**
   - Create a service principal using the Databricks Python SDK
   - Write `GRANT` and `REVOKE` statements at the catalog level using SQL
   - Use `SHOW GRANTS` to verify the resulting permission state and include the output in your submission

3. **CLI Verification**
   - Use the Databricks CLI to list your catalogs and confirm the catalog you created appears in the output
   - Use the CLI to list service principals and confirm the one you created is present
   - Include the terminal output for both commands in your submission

### Week 2 Requirements (Automation and CI/CD)

4. **GitHub Integration**
   - Connect your project repository to a Databricks workspace via the Git folder (Repos) interface
   - Create a feature branch, make at least one change, and open a pull request against `main`
   - Describe your branching strategy in a short `BRANCHING.md` file

5. **Running Notebooks as Jobs**
   - Create a Databricks job that runs a notebook sourced from your connected Git repository
   - Configure the job to reference a specific branch in that repository
   - Run the job manually and include a screenshot or description of the successful run output

6. **GitHub Actions CI/CD**
   - Write a GitHub Actions workflow that triggers on pull requests to `main`
   - The workflow must include at least one code quality step (e.g., a linter, a syntax check, or a Docker build validation)
   - Include the workflow YAML file in your submission

### Week 3 Requirements (Monitoring)

7. **Lakehouse Monitoring**
   - Enable monitoring on at least one table in your catalog using the Databricks UI
   - After the initial scan completes, document the quality results for that table: include the last scan timestamp, row count, and the freshness/completeness status
   - Describe in writing what threshold you would set to trigger an alert, and what action you would take if that threshold were breached

## Deliverables

Submit a single compressed archive (`.zip` or `.tar.gz`) containing:

1. **SQL scripts** — all `CREATE`, `GRANT`, `REVOKE`, and `SHOW GRANTS` queries
2. **Python script** — service principal creation via the Databricks SDK
3. **CLI output** — terminal screenshots or copied output from the `databricks catalogs list` and `databricks service-principals list` commands
4. **GitHub Actions YAML** — CI/CD workflow file
5. **BRANCHING.md** — description of your branching strategy
6. **Monitoring report** — a Markdown document containing:
   - The quality results for your monitored table (screenshot or query output)
   - Your alerting threshold and response strategy
7. **Architecture diagram** — a diagram (any tool) showing:
   - Catalog → schema → table hierarchy
   - Service principal and its granted permissions
   - CI/CD flow from feature branch to main
   - Monitoring scope and the table(s) being tracked

## Evaluation Rubric

| Criterion | Points |
|-----------|--------|
| Catalog and schema design correctness | 20 |
| Service principal creation via Python SDK | 15 |
| GRANT / REVOKE / SHOW GRANTS implementation | 20 |
| CLI verification output (catalogs and service principals) | 10 |
| GitHub integration, branching strategy, and pull request | 10 |
| Notebook job configuration and successful run | 15 |
| GitHub Actions CI/CD workflow | 5 |
| Lakehouse Monitoring setup and documentation | 5 |
| **Total** | **100** |

## Tips

- Use the examples in this repository as starting points — adapt them to your chosen dataset and business scenario
- The example dataset in `data/` provides a simple starting point if you do not have your own data
- Document every decision — "why" is more important than "what" for the access control and monitoring sections
- The Databricks CLI help system (`databricks help`) is useful for discovering the exact syntax of any command
