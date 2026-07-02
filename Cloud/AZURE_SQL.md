# Azure SQL Database

## Purpose

Azure SQL Database is a fully managed relational database service on Microsoft Azure. It provides enterprise-grade availability, security, backup, monitoring, and performance capabilities for structured data workloads.

Within the Otic Fortress AI Governance and Cybersecurity Platform, Azure SQL Database is used for data that requires strong consistency, relational modeling, transactional integrity, structured querying, and controlled access patterns.

## Why Fortress Uses Azure SQL

Fortress uses Azure SQL for core relational platform data, including:

- User accounts
- Roles and permissions
- Authentication records
- Organizations and tenants
- AI policy definitions
- Audit metadata
- System configuration
- Compliance records

This data benefits from a relational database model because it often requires well-defined schemas, referential integrity, joins, constraints, transactions, and predictable query behavior. Azure SQL is appropriate for governance and cybersecurity workloads where data accuracy, traceability, access control, and reporting consistency are critical.

## Proposed Database Naming Convention

Proposed Azure SQL server names:

```text
sql-otic-fortress-dev
sql-otic-fortress-test
sql-otic-fortress-prod
```

Proposed database names:

```text
otic_fortress_dev
otic_fortress_test
otic_fortress_prod
```

Server naming convention format:

```text
sql-<platform-name>-<environment>
```

Database naming convention format:

```text
<platform_name>_<environment>
```

- `sql`: Identifies the resource as an Azure SQL server.
- `otic-fortress` or `otic_fortress`: Identifies the platform or workload.
- `dev`, `test`, `prod`: Identifies the target environment.

This convention supports clear ownership, environment separation, automation, monitoring, and cost reporting.

## Database Security

Azure SQL Database should be configured with layered security controls appropriate for enterprise cloud workloads.

- **Azure Active Directory Authentication:** Enables identity-based authentication instead of relying only on SQL usernames and passwords.
- **Microsoft Entra ID integration:** Provides centralized identity governance, conditional access, and access lifecycle management for database administrators and approved users.
- **RBAC:** Controls management-plane access to Azure SQL resources through Azure role assignments.
- **Firewall Rules:** Restrict network access to approved IP ranges and trusted Azure services where required.
- **Private Endpoints:** Provide private network access to Azure SQL over Azure Private Link, reducing public exposure.
- **Transparent Data Encryption (TDE):** Encrypts data at rest to protect database files, backups, and transaction logs.
- **Always Encrypted:** Protects sensitive columns by encrypting data client-side so protected values remain encrypted in the database engine.
- **Dynamic Data Masking:** Limits exposure of sensitive data in query results for non-privileged users.
- **Row-Level Security:** Restricts row access based on user identity, tenant, organization, or application context.

Security controls should be applied according to data classification, environment sensitivity, and compliance requirements.

## Backup and Disaster Recovery

Azure SQL Database provides managed backup and restore capabilities that support operational recovery and business continuity planning.

- **Automated Backups:** Azure automatically creates database backups according to the configured service tier and retention policy.
- **Point-in-Time Restore:** Supports recovery to a specific point within the backup retention period after accidental data modification or deletion.
- **Geo-Redundant Backups:** Protects against regional failures by storing backups in a paired Azure region when enabled.
- **Recovery Objectives:** Recovery Time Objective (RTO) and Recovery Point Objective (RPO) should be defined for each environment, with stricter requirements for production.
- **Backup Validation:** Restore procedures should be tested regularly to confirm that backups are usable and recovery documentation is accurate.

Production databases should have clearly documented retention, restore, and disaster recovery requirements.

## Monitoring

Azure SQL monitoring should provide visibility into health, performance, security, and operational activity.

- **Azure Monitor:** Collects database metrics, resource health signals, and platform-level telemetry.
- **Application Insights:** Correlates backend application behavior with database dependency calls, latency, failures, and request traces.
- **SQL Auditing:** Records database access, queries, permission changes, and security-relevant events for compliance and investigation.
- **Query Performance Insights:** Helps identify expensive queries, performance regressions, and optimization opportunities.
- **Alerts:** Notify operators of availability issues, high resource utilization, failed connections, security events, or abnormal query behavior.
- **Log Analytics:** Centralizes logs and metrics for investigation, dashboards, long-term retention, and security analytics.

Monitoring should be configured separately for each environment, with production requiring stricter alerting and retention.

## Performance Strategy

Azure SQL performance planning should align with workload requirements, cost constraints, and growth expectations.

- **DTU vs vCore:** DTU-based purchasing can simplify early sizing, while vCore-based purchasing provides more control over compute, memory, storage, and licensing options.
- **Autoscaling:** Scaling strategy should account for predictable workload growth, peak usage periods, and environment-specific performance requirements.
- **Index Optimization:** Indexes should be designed and maintained based on query patterns, data volume, and performance telemetry.
- **Query Optimization:** Queries should be reviewed for efficient joins, filtering, pagination, parameterization, and execution plans.
- **Connection Pooling:** Backend services should use connection pooling to reduce overhead and improve database efficiency under load.

Performance decisions should be validated with telemetry and load testing rather than assumptions.

## Environment Separation

Development, Testing, and Production databases should be completely separate. Each environment should have its own Azure SQL server and database unless an approved enterprise architecture decision defines otherwise.

Separation helps:

- Prevent non-production access to production data.
- Reduce the risk of accidental production changes.
- Support environment-specific RBAC and firewall rules.
- Enable independent backup and restore policies.
- Improve cost tracking by environment.
- Support safer testing of schema changes and migrations.

Production data should not be copied into non-production environments unless it is approved, sanitized, and handled according to data protection requirements.

## Security Best Practices

- Apply least privilege access to users, applications, automation identities, and administrators.
- Use Managed Identity for Azure-hosted workloads where supported.
- Store database credentials and connection strings in Azure Key Vault.
- Do not hardcode connection strings in source code, container images, pipeline files, or documentation.
- Rotate secrets and credentials regularly.
- Keep SQL platform configuration, dependencies, and client libraries updated.
- Follow the principle of least access for both management-plane and data-plane permissions.
- Use private networking where appropriate for production workloads.
- Enable auditing, monitoring, and alerting for sensitive database activity.

## Data Classification

Azure SQL should store structured relational data that requires transactional consistency.

Examples include:

| Data Type | Stored in Azure SQL |
|------------|---------------------|
| Users | ✅ |
| Roles | ✅ |
| Permissions | ✅ |
| Organizations | ✅ |
| Compliance Policies | ✅ |
| Audit Metadata | ✅ |
| AI Governance Rules | ✅ |
| Platform Configuration | ✅ |

The following data should not primarily reside in Azure SQL:

| Data Type | Preferred Service |
|------------|-------------------|
| Large telemetry streams | Azure Cosmos DB |
| Event logs | Azure Monitor / Log Analytics |
| Files and evidence | Azure Storage |
| Secrets | Azure Key Vault |

## Future Integration

Azure SQL will integrate with several Fortress platform components:

- **Backend APIs:** Store and query relational application data such as users, roles, tenants, policy definitions, and compliance records.
- **Azure Kubernetes Service (AKS):** Host backend workloads that connect securely to Azure SQL using approved network and identity patterns.
- **Azure Key Vault:** Store connection strings, credentials, certificates, and database-related secrets.
- **GitHub Actions:** Support CI/CD workflows that validate database-related changes while using approved secret and identity management patterns.
- **Azure Monitor:** Provide operational metrics, logs, alerts, and performance visibility.
- **AI Governance services:** Persist structured governance metadata, policy relationships, audit metadata, and compliance state.

Integration patterns should prioritize secure identity, private connectivity, observability, and environment-specific isolation.
## Database Migration Strategy

Database schema changes should be version-controlled and executed through approved migration tools.

Recommendations:

- Store migrations in source control.
- Review schema changes through Pull Requests.
- Validate migrations in Development before Testing or Production.
- Back up production databases before major schema changes.
- Never modify production schemas manually without an approved change process.

## Summary

Azure SQL Database provides the relational data foundation for the Otic Fortress platform. It supports structured governance data, secure access, transactional integrity, monitoring, backup, and enterprise-grade operational controls across Development, Testing, and Production environments.
