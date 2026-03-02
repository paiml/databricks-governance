# =============================================================================
# Lesson 3.6: Secrets Management
# Creating Secret Scopes and Retrieving Credentials Securely
# =============================================================================
# Never hardcode credentials in notebooks or job configs.
# This file demonstrates the three secrets patterns covered in the lesson:
#   1. Databricks-backed secret scope (managed by Databricks)
#   2. Azure Key Vault-backed secret scope (secrets stored in Azure)
#   3. AWS Secrets Manager-backed scope (secrets stored in AWS)
#
# The Databricks CLI commands in the comments are run from a terminal or the
# Databricks notebook %sh magic — they are not Python.
# The Python cells demonstrate how to retrieve secrets inside a notebook/job.
# =============================================================================

# COMMAND ----------
# Cell 1: Create a Databricks-backed secret scope via the CLI
#
# Run these in a terminal (not inside a notebook):
#
#   databricks secrets create-scope \
#     --scope governance-course \
#     --initial-manage-principal users
#
# Then add a secret to the scope:
#
#   databricks secrets put \
#     --scope governance-course \
#     --key jdbc-password
#   (prompts for the secret value — it is never stored in shell history)

print("See comments above for CLI commands to create a Databricks-backed scope.")

# COMMAND ----------
# Cell 2: Retrieve a secret inside a notebook

# dbutils.secrets.get() returns the value as a Python string.
# Databricks NEVER displays the raw value in notebook output — it is redacted.

jdbc_password = dbutils.secrets.get(scope="governance-course", key="jdbc-password")

jdbc_url = (
    "jdbc:sqlserver://myserver.database.windows.net:1433;"
    "database=mydb;"
    f"password={jdbc_password};"
    "encrypt=true;"
)

print("Secret retrieved (value is redacted in output):", repr(jdbc_password[:3] + "***"))

# COMMAND ----------
# Cell 3: List available scopes and keys (values are always hidden)

scopes = dbutils.secrets.listScopes()
for scope in scopes:
    print(f"Scope: {scope.name}")
    keys = dbutils.secrets.list(scope.name)
    for key in keys:
        print(f"  key: {key.key}  (metadata bytes: {key.metadata})")

# COMMAND ----------
# Cell 4: Azure Key Vault-backed scope
#
# CLI command to create a Key Vault-backed scope:
#
#   databricks secrets create-scope \
#     --scope azure-kv-scope \
#     --scope-backend-type AZURE_KEYVAULT \
#     --resource-id /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.KeyVault/vaults/<vault-name> \
#     --dns-name https://<vault-name>.vault.azure.net/
#
# After creation, secrets in the Key Vault are automatically available.
# You can read them with the same dbutils.secrets.get() API:

# api_key = dbutils.secrets.get(scope="azure-kv-scope", key="my-api-key")

print("Azure Key Vault-backed scopes use the same dbutils.secrets.get() API.")
print("Secrets are managed in Azure Key Vault — Databricks never stores them.")

# COMMAND ----------
# Cell 5: AWS Secrets Manager-backed scope
#
# CLI command to create an AWS Secrets Manager-backed scope:
#
#   databricks secrets create-scope \
#     --scope aws-sm-scope \
#     --scope-backend-type AWS_SSM \
#     --ssm-parameter-store-path /databricks/governance-course
#
# Retrieve the secret exactly the same way:
#
#   db_password = dbutils.secrets.get(scope="aws-sm-scope", key="db-password")

print("AWS Secrets Manager-backed scopes are read-only from Databricks.")
print("Manage secret rotation and auditing in the AWS console.")

# COMMAND ----------
# Cell 6: Best practices summary

best_practices = """
Best Practices for Secrets in Databricks
─────────────────────────────────────────
1. NEVER use dbutils.secrets.get() output in a print() without redacting it.
2. Prefer group-level scope permissions over granting access to individual users.
3. Use cloud-native vaults (Key Vault / Secrets Manager) so rotation is centralized.
4. Audit secret access via Unity Catalog audit logs in system.access.audit.
5. Rotate credentials on a schedule; remove unused keys promptly.
"""
print(best_practices)
