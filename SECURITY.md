# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it by:

1. **Do not** open a public GitHub issue
2. Email security concerns to the maintainers
3. Include details about the vulnerability
4. Allow time for a fix before public disclosure

## Security Considerations

This repository contains educational examples for governing data platforms and ML systems on Databricks. When using these examples:

- **Credentials**: Never commit Databricks tokens, cloud credentials, or API keys to version control
- **Secret Scopes**: Always use Databricks secret scopes (or Azure Key Vault / AWS Secrets Manager) rather than hardcoding secrets in notebooks or jobs
- **Permissions**: Apply the principle of least privilege — grant only the permissions a user or service principal actually needs
- **Audit Logs**: Enable Unity Catalog audit logging to track who accesses sensitive data
- **Network Security**: Configure IP access lists and private link for production workspaces

## Best Practices

1. Use `dbutils.secrets.get()` for all credential retrieval in notebooks and jobs
2. Rotate service principal credentials regularly and revoke unused tokens
3. Review `GRANT` statements carefully — prefer granting to groups rather than individual users
4. Keep Databricks runtime and cluster libraries updated
5. Use Unity Catalog column masks and row filters for PII protection
