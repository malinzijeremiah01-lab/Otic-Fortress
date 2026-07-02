# Azure Key Vault

## Purpose

Azure Key Vault is a managed Azure service for securely storing and controlling access to secrets, keys, and certificates. It centralizes sensitive configuration and reduces the risk of exposing credentials in source code, configuration files, build pipelines, container images, or runtime environments.

For Otic Fortress, Azure Key Vault provides the foundation for secure secret management across cloud infrastructure, backend services, CI/CD workflows, and future Kubernetes deployments.

## Why Fortress Uses Azure Key Vault

Otic Fortress is an enterprise AI Governance and Cybersecurity Platform. The platform must protect sensitive application secrets, infrastructure credentials, database access details, certificates, and integration keys across multiple environments.

Azure Key Vault helps Fortress:

- Centralize secret storage and access control.
- Keep credentials out of source control and application packages.
- Apply least privilege access using Azure RBAC.
- Support managed identity authentication for Azure-hosted workloads.
- Enable secret rotation and controlled credential lifecycle management.
- Provide auditing and monitoring for secret access.

## Secrets to Store

The following sensitive values should be stored in Azure Key Vault rather than committed to the repository or stored directly in application configuration files:

- **JWT secrets:** Signing secrets used for authentication tokens.
- **Azure service credentials:** Client secrets, service principal credentials, or integration credentials when managed identity is not available.
- **Database connection strings:** Azure SQL and other database connection strings containing credentials or sensitive endpoints.
- **API keys:** External service keys, AI service keys, webhook secrets, and platform integration tokens.
- **Certificates:** TLS certificates, signing certificates, and other certificate-based credentials.

Only placeholder values should appear in `.env.example`, documentation, test fixtures, or sample configuration files.

## Access Control

Access to Key Vault should follow RBAC and least privilege principles. Users, service principals, managed identities, and automation workflows should receive only the permissions required for their role.

Recommended access patterns:

- Grant read access to applications that only need to retrieve secrets.
- Grant write or rotation permissions only to approved operators or automation identities.
- Separate administrative access from runtime application access.
- Review access assignments regularly.
- Avoid broad subscription-level permissions when Resource Group or Key Vault scoped permissions are sufficient.

Production Key Vault access should be more restrictive than development and testing access.

## Managed Identity Usage

Azure Managed Identity should be the preferred authentication method for Azure-hosted Fortress workloads. Managed identities remove the need to store Azure service credentials directly in application configuration.

Future AKS, application services, automation jobs, and Azure-hosted backend components should use managed identity where supported to retrieve secrets from Azure Key Vault. This approach improves security by eliminating long-lived credentials and enabling Azure-native identity lifecycle management.

## Naming Convention

Proposed Key Vault names:

```text
kv-otic-fortress-dev
kv-otic-fortress-test
kv-otic-fortress-prod
```

Naming convention format:

```text
kv-<platform-name>-<environment>
```

- `kv`: Identifies the resource as an Azure Key Vault.
- `otic-fortress`: Identifies the platform or workload.
- `dev`, `test`, `prod`: Identifies the target environment.

This naming convention supports clear ownership, predictable automation, and environment-specific access control.

## Environment Separation

Otic Fortress should use separate Key Vault instances for Development, Testing, and Production environments.

Environment separation helps:

- Prevent non-production workloads from accessing production secrets.
- Apply stricter RBAC and monitoring to production.
- Support independent secret rotation schedules.
- Reduce the blast radius of accidental changes or credential exposure.
- Maintain clean lifecycle management for each environment.

Development, testing, and production secrets must not be shared unless explicitly approved and documented.

## Secret Rotation

Secrets should be rotated regularly according to enterprise security requirements and platform risk classification. Rotation should also occur after suspected exposure, personnel changes, credential misuse, or changes to dependent systems.

Secret rotation planning should include:

- Defined owners for each secret.
- Expiration dates where supported.
- Rotation frequency based on sensitivity.
- Application restart or reload requirements.
- Rollback planning for critical services.
- Validation after rotation.

Where possible, prefer short-lived credentials, managed identity, certificates with lifecycle policies, and automated rotation workflows.

## Auditing and Monitoring

Key Vault access should be monitored through Azure-native logging and security tools. Diagnostic settings should send relevant logs and metrics to approved monitoring destinations such as Azure Monitor, Log Analytics, Microsoft Defender for Cloud, or a centralized SIEM.

Monitoring should include:

- Secret read, write, update, and delete activity.
- Access denied events.
- Administrative changes.
- RBAC assignment changes.
- Secret expiration and certificate expiration events.
- Unusual access patterns.

Production Key Vaults should have alerting for suspicious access, failed access attempts, and critical secret lifecycle events.

## GitHub Actions Integration

GitHub Actions workflows should not store long-lived production secrets directly in repository files. CI/CD workflows should use approved GitHub secrets, environment protection rules, OpenID Connect federation, or managed deployment identities to access Azure securely.

For future Azure deployment workflows, GitHub Actions should retrieve required values from Azure Key Vault only through approved identities and scoped permissions. Workflow access should be environment-specific, auditable, and protected by branch policies and required reviews.

## Future AKS Integration

Future AKS deployments should integrate with Azure Key Vault using managed identity and approved secret access patterns. Workloads should avoid baking secrets into container images or Kubernetes manifests.

Recommended AKS patterns include:

- Use managed identity for workload access to Azure resources.
- Retrieve secrets from Azure Key Vault at runtime.
- Keep Kubernetes secrets limited, controlled, and synchronized only when required.
- Use environment-specific Key Vault instances.
- Monitor secret access from cluster identities.

## Fortress Secret Classification

The following categories of secrets should be managed according to their sensitivity:

| Secret Type | Storage Location | Rotation Required |
|--------------|------------------|-------------------|
| JWT Secrets | Azure Key Vault | Yes |
| Azure Client Secrets | Azure Key Vault | Yes |
| Database Connection Strings | Azure Key Vault | Yes |
| Cosmos DB Keys | Azure Key Vault | Yes |
| Storage Account Keys | Azure Key Vault | Yes |
| SMTP Credentials | Azure Key Vault | Yes |
| API Keys | Azure Key Vault | Yes |
| TLS Certificates | Azure Key Vault | Yes |

No production secret should exist in:
- GitHub repositories
- Source code
- Docker images
- Configuration files
- Documentation

## Security Best Practices

- Store all sensitive values in Azure Key Vault or an approved secret management system.
- Never commit real secrets, credentials, certificates, tokens, or connection strings.
- Use Azure RBAC with least privilege access.
- Prefer managed identity over client secrets.
- Separate Key Vaults by environment.
- Enable auditing, monitoring, and alerting.
- Rotate secrets regularly.
- Apply expiration dates to secrets and certificates where appropriate.
- Restrict production access to approved users and workload identities.
- Review access permissions and secret inventory on a regular schedule.

## Summary

Azure Key Vault is the primary secret management service for the Otic Fortress Azure infrastructure strategy. It protects sensitive platform values, supports RBAC and managed identity, enables auditing and rotation, and provides a secure foundation for GitHub Actions, backend services, and future AKS deployments.
