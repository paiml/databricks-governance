# Lab 4: CI/CD for Notebooks

## Objectives

- Connect a Databricks workspace to a GitHub repository using Databricks Repos
- Understand branching strategies for data and ML teams
- Set up a GitHub Actions workflow that runs a notebook in staging on pull request
- Promote a tested notebook to production automatically on merge to main

## Prerequisites

- A GitHub account and a forked copy of this repository
- A Databricks workspace with Repos (Git Folders) enabled
- GitHub repository secrets configured (workspace URL and access token)

## Background

Notebooks are the most productive artifact in a data platform — and the riskiest when deployed without review. Databricks Repos (now called Git Folders) lets you check out a full Git repository into your workspace, so notebooks live alongside Python modules, YAML configs, and test files in a standard project layout.

The CI/CD pattern for notebooks has three stages:

1. **Development** — Data scientists iterate in personal branches or dev workspaces
2. **Staging** — Pull requests trigger automated notebook runs against staging data and infrastructure
3. **Production** — Merges to `main` deploy the tested notebook to the production workspace

## Exercise 1: Connect a Repo to Databricks

1. In your Databricks workspace, navigate to **Workspace > Repos**
2. Click **Add Repo** and paste the URL of your forked repository
3. Authenticate with GitHub using a personal access token
4. Observe the cloned directory structure in the Databricks workspace

### Questions

1. What is the difference between a Databricks Repo and a regular workspace folder?
2. Can you run a notebook directly from a Repo without importing it?

## Exercise 2: Review the GitHub Actions Sync Workflow

Review [`examples/repos/github_actions_sync.yml`](../examples/repos/github_actions_sync.yml).

This workflow:
1. Triggers on pushes to `main` or `staging`
2. Calls the Databricks Repos API (`PATCH /api/2.0/repos/{id}`) to update the workspace repo to the latest branch commit

1. Add the required secrets to your GitHub repository settings:
   - `DATABRICKS_HOST`
   - `DATABRICKS_TOKEN`
   - `REPO_ID` (find this in the URL when you open the repo in the Databricks workspace)
2. Push a small change to the `staging` branch and observe the workflow run in **Actions**
3. Verify the workspace Repo updated by checking the commit hash in the Databricks UI

## Exercise 3: Review the Notebook CI/CD Workflow

Review [`examples/cicd/notebook_ci.yml`](../examples/cicd/notebook_ci.yml).

This workflow has two jobs:
- `test-in-staging` — runs on every pull request, imports the notebook and runs it on a staging cluster
- `deploy-to-production` — runs on merges to `main`, imports to the production workspace and updates the Repo

1. Observe how the `PATCH /api/2.0/runs/submit` call passes environment-specific parameters via `base_parameters`
2. Observe the polling loop that waits for the run to complete and checks `result_state`

### Questions

1. What happens if the notebook run fails in staging? Does the pull request merge?
2. How does the workflow ensure that the production workspace only ever receives code that passed staging?

## Key Takeaways

- Databricks Repos lets you version-control notebooks alongside regular Python files
- The Repos API endpoint (`PATCH /api/2.0/repos/{id}`) is the single call needed to sync a workspace to a Git branch
- GitHub Actions provides event-driven automation: PRs trigger staging runs, merges trigger production promotion
- Passing `base_parameters` to `notebook_task` is how you inject environment-specific configuration at runtime
