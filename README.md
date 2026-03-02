# Production Governance and MLOps with Databricks

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![Databricks](https://img.shields.io/badge/Databricks-Unity%20Catalog-red)](https://docs.databricks.com/aws/en/data-governance/unity-catalog/)

<p align="center">
  <strong>Hands-on labs for governing data and AI with Unity Catalog, MLflow, and Databricks Lakehouse Monitoring</strong><br>
  Unity Catalog | Access Control | Data Lineage | CI/CD | MLOps | Secrets Management
</p>

---

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Course Outline](#course-outline)
- [Project Structure](#project-structure)
- [Resources](#resources)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Learn to govern production data platforms and ML systems on Databricks. This course covers:

- **Unity Catalog** — Centralized governance with metastores, catalogs, schemas, and tables
- **Access Control** — GRANT/REVOKE permissions, row/column-level security, and least-privilege design
- **Data Lineage** — Automatic lineage capture and compliance querying via system tables
- **CI/CD for Notebooks** — GitHub Actions, multi-environment promotion (dev → staging → prod)
- **MLOps** — MLflow experiment tracking, model registration, and promotion through the model registry
- **Lakehouse Monitoring** — Data quality alerts, drift detection, and retraining triggers
- **Secrets Management** — Databricks secret scopes, Azure Key Vault, and AWS Secrets Manager integration

---

## Quick Start

1. Sign up for a [Databricks workspace](https://www.databricks.com/try-databricks) (Unity Catalog enabled by default on new workspaces)
2. Clone this repository:
   ```bash
   git clone https://github.com/alfredodeza/databricks-governance.git
   ```
3. Upload example files from `examples/` to your Databricks workspace
4. Run SQL examples in a SQL warehouse or attach Python notebooks to a cluster
5. Follow the labs in `labs/` for guided exercises

---

## Usage

### Run Examples

| Example | Files | Description |
|---------|-------|-------------|
| Unity Catalog | `examples/unity/` | Create catalogs, schemas, tables, and volumes |
| Access Control | `examples/access-control/` | GRANT/REVOKE and permission model design |
| Lineage | `examples/lineage/` | Query lineage system tables |
| Repos / Git | `examples/repos/` | GitHub Actions workflow for Databricks Repos |
| CI/CD for Notebooks | `examples/cicd/` | Multi-environment notebook deployment |
| MLOps | `examples/mlops/` | MLflow training, registration, and promotion |
| Lakehouse Monitoring | `examples/monitoring/` | Table monitors and alerting |
| ML Monitoring | `examples/ml-monitoring/` | Inference table drift detection |
| Secrets | `examples/secrets/` | Secret scopes and credential retrieval |

### Complete the Labs

| Lab | Topic | Examples |
|-----|-------|----------|
| [Lab 1](./labs/lab-1.md) | Unity Catalog Setup | `unity/` |
| [Lab 2](./labs/lab-2.md) | Access Control | `access-control/` |
| [Lab 3](./labs/lab-3.md) | Data Lineage | `lineage/` |
| [Lab 4](./labs/lab-4.md) | CI/CD for Notebooks | `repos/`, `cicd/` |
| [Lab 5](./labs/lab-5.md) | ML Model CI/CD | `mlops/` |
| [Lab 6](./labs/lab-6.md) | Monitoring and Secrets | `monitoring/`, `ml-monitoring/`, `secrets/` |

---

## Course Outline

### Week 1: Unity Catalog Governance

- [Lesson 1.1 – Unity Catalog Overview](./examples/unity/) — Metastores, catalogs, schemas, tables
- [Lesson 1.4 – Access Control](./examples/access-control/) — GRANT, REVOKE, and permission design
- [Lesson 1.6 – Data Lineage](./examples/lineage/) — System table queries and compliance reporting

### Week 2: CI/CD and MLOps

- [Lesson 2.1 – Databricks Repos](./examples/repos/) — GitHub integration and branching strategies
- [Lesson 2.3 – CI/CD for Notebooks](./examples/cicd/) — GitHub Actions and multi-environment promotion
- [Lesson 2.6 – ML Model CI/CD](./examples/mlops/) — MLflow lifecycle and model registry promotion

### Week 3: Monitoring and Security

- [Lesson 3.1 – Lakehouse Monitoring](./examples/monitoring/) — Table monitors and anomaly alerting
- [Lesson 3.3 – ML Model Monitoring](./examples/ml-monitoring/) — Drift detection and retraining triggers
- [Lesson 3.6 – Secrets Management](./examples/secrets/) — Secret scopes, Key Vault, and Secrets Manager

See the full [course outline](./course_outline.md) for detailed lesson breakdowns.

---

## Project Structure

```
databricks-governance/
├── examples/
│   ├── unity/               # Unity Catalog: catalogs, schemas, tables, volumes
│   ├── access-control/      # GRANT/REVOKE and permission model design
│   ├── lineage/             # Lineage system table queries
│   ├── repos/               # GitHub Actions for Databricks Repos
│   ├── cicd/                # CI/CD pipelines for notebook promotion
│   ├── mlops/               # MLflow training, registration, and promotion
│   ├── monitoring/          # Lakehouse Monitoring table monitors
│   ├── ml-monitoring/       # Inference table drift detection
│   └── secrets/             # Secret scopes and credential handling
├── labs/                    # Hands-on lab instructions
├── docs/                    # Capstone project and supplementary docs
├── data/                    # Sample datasets for demonstrations
└── assets/                  # Course banner and graphics
```

---

## Resources

- [Unity Catalog Documentation](https://docs.databricks.com/aws/en/data-governance/unity-catalog/)
- [MLflow Model Registry](https://mlflow.org/docs/latest/model-registry/)
- [Databricks Lakehouse Monitoring](https://docs.databricks.com/aws/en/lakehouse-monitoring/)
- [Databricks Secret Management](https://learn.microsoft.com/en-us/azure/databricks/security/secrets/)
- [GitHub Actions for Databricks](https://www.databricks.com/blog/2022/06/02/automate-your-data-and-ml-workflows-with-github-actions-for-databricks.html)

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## License

Apache License 2.0 — see [LICENSE](LICENSE) for details.

---

<p align="center">
  Made with care by <a href="https://paiml.com">Pragmatic AI Labs</a>
</p>
