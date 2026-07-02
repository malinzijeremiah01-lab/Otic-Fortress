# Azure Cosmos DB

## Purpose

Azure Cosmos DB is a fully managed, globally distributed NoSQL database service on Microsoft Azure. It is designed for low-latency access, elastic scalability, high availability, and flexible data models across globally distributed applications.

Within the Otic Fortress AI Governance and Cybersecurity Platform, Azure Cosmos DB supports dynamic, high-volume, and semi-structured data workloads. It is especially useful for telemetry, event streams, security analytics, AI inference metadata, and other data types that evolve quickly or do not require a fixed relational schema.

---

## Why Fortress Uses Azure Cosmos DB

Fortress uses Azure Cosmos DB for workloads that require flexible schemas, high ingestion rates, scalable reads and writes, and fast access to event-oriented data.

Examples include:

- AI telemetry
- AI shadow detection events
- Security events
- User activity logs
- Threat intelligence
- Incident timelines
- AI inference metadata
- Device telemetry
- Platform analytics
- Audit event streams

These workloads are often better suited to NoSQL storage than relational storage because events and telemetry can vary in structure, grow rapidly, and require partitioned access patterns at scale. Cosmos DB allows Fortress to store JSON-based documents with flexible properties while supporting efficient queries, global distribution, time-based retention, and event-driven processing through the change feed.

Relational data such as users, roles, permissions, tenants, and policy definitions belongs in Azure SQL. High-volume operational events, telemetry, and evolving analytics data belong in Azure Cosmos DB.

---

## Proposed Naming Convention

Proposed Cosmos DB account names:

```text
cosmos-otic-fortress-dev
cosmos-otic-fortress-test
cosmos-otic-fortress-prod
```

Proposed database names:

```text
otic-fortress-dev
otic-fortress-test
otic-fortress-prod
```

Proposed container names:

```text
shadow-events
security-events
audit-events
telemetry
device-events
ai-analysis
```

Account naming convention format:

```text
cosmos-<platform-name>-<environment>
```

Database naming convention format:

```text
<platform-name>-<environment>
```

Container names should describe the data domain stored in the container. Names should be short, lowercase, readable, and aligned with platform terminology.

- `cosmos`: Identifies the resource as an Azure Cosmos DB account.
- `otic-fortress`: Identifies the platform or workload.
- `dev`, `test`, `prod`: Identifies the target environment.
- Container names such as `shadow-events` and `audit-events`: Identify the primary event or data category.

---

## Data Organization

Cosmos DB data should be organized by environment, workload domain, and access pattern. Containers should group documents that share similar partitioning, retention, indexing, and query requirements.

| Database | Container | Purpose |
| --- | --- | --- |
| `otic-fortress-dev` | `shadow-events` | Stores AI shadow detection events, detections, and related metadata for development. |
| `otic-fortress-test` | `audit-events` | Stores audit event streams used for validation and compliance testing. |
| `otic-fortress-prod` | `telemetry` | Stores production platform telemetry and operational event data. |
| `otic-fortress-prod` | `threat-intelligence` | Stores threat intelligence indicators, enrichment data, and security context. |
| `otic-fortress-prod` | `device-events` | Stores device activity, endpoint signals, and related event metadata. |
| `otic-fortress-prod` | `ai-analysis` | Stores AI analysis results, inference metadata, risk scores, and model evaluation outputs. |

Logical separation should be based on data sensitivity, access patterns, retention requirements, and throughput needs. High-volume event streams should not share containers with low-volume reference data when their partitioning and indexing requirements differ.

Partitioning should be planned early. Recommended partition keys may include tenant identifiers, organization identifiers, event category, device identifier, or composite values derived from the dominant query pattern.

---

## Security

Cosmos DB should be protected with layered security controls appropriate for enterprise cybersecurity workloads.

- **Microsoft Entra ID authentication:** Enables identity-based access to Cosmos DB and reduces reliance on account keys.
- **RBAC:** Provides role-based access control for users, applications, managed identities, and automation workflows.
- **Managed Identity:** Allows Azure-hosted workloads to access Cosmos DB without storing credentials in application configuration.
- **Private Endpoints:** Restrict access to Cosmos DB through private Azure networking using Azure Private Link.
- **Encryption at Rest:** Protects stored data using Azure-managed or customer-managed encryption options.
- **Encryption in Transit:** Protects data moving between applications and Cosmos DB over secure connections.
- **Network Isolation:** Limits access using private networking, firewall controls, and approved network paths.
- **Key Vault integration:** Stores connection strings, account keys, certificates, and related secrets when key-based access is required.

Production Cosmos DB accounts should use the strictest access controls, network restrictions, monitoring, and approval processes.

---

## Partitioning Strategy

Partitioning is a core design decision for Cosmos DB. The partition key determines how data is distributed across physical partitions and directly affects scalability, performance, and cost.

Key considerations:

- **Partition Keys:** Choose partition keys based on common query filters, write distribution, and tenant isolation requirements.
- **Hot Partitions:** Avoid partition keys that concentrate too many reads or writes into a single logical partition.
- **Even Data Distribution:** Select keys that spread data evenly across tenants, devices, events, or time-aware categories.
- **Scalability:** Design partitioning so containers can grow without requiring disruptive redesign.
- **Query Performance:** Align partition keys with frequent queries to reduce cross-partition query costs.

Recommended Fortress partition key candidates:

- `/tenantId` for multi-tenant governance and audit workloads.
- `/organizationId` for organization-scoped analytics and reporting.
- `/deviceId` for device telemetry and endpoint event streams.
- `/eventType` only when event types have balanced volume.
- `/partitionKey` for application-managed composite keys such as `tenantId:eventDate`.

For high-volume telemetry and event data, Fortress should consider composite partition key strategies that combine tenant, device, or time-based values to reduce hot partitions and support efficient queries.

---

## Performance Strategy

Cosmos DB performance should be planned around throughput, indexing, retention, event processing, and geographic access requirements.

- **Autoscale Throughput:** Automatically scales RU/s based on workload demand, helping support variable ingestion and query patterns.
- **Request Units (RU/s):** Provide a normalized measure of database operation cost and should be monitored for capacity planning.
- **Indexing Policy:** Controls which document properties are indexed and can reduce cost for write-heavy event streams.
- **TTL (Time To Live):** Automatically expires older telemetry, logs, and transient analytics data according to retention policy.
- **Change Feed:** Enables event-driven processing for analytics, AI shadow detection, incident workflows, and downstream integrations.
- **Global Distribution:** Supports low-latency access and resilience across regions when multi-region architecture is required.

Fortress should use autoscale for workloads with variable demand and tune indexing policies for containers with high write volume. TTL should be applied to data categories with defined retention periods.

## Access Pattern Strategy

Fortress should design Cosmos DB containers around application access patterns rather than traditional database normalization.

Examples:

| Access Pattern | Recommended Container |
|----------------|-----------------------|
| Lookup AI events by tenant | shadow-events |
| Retrieve device history | device-events |
| Search incident timeline | security-events |
| Read telemetry | telemetry |
| Fetch AI analysis | ai-analysis |

Containers should be optimized for the application's most frequent read and write operations.
---

## Monitoring

Cosmos DB health and performance should be monitored using Azure-native observability services.

- **Azure Monitor:** Captures platform metrics, availability, throughput usage, latency, and service health.
- **Application Insights:** Correlates backend API requests with Cosmos DB dependency calls, latency, failures, and traces.
- **Diagnostic Logs:** Provide detailed operational and security events for analysis and compliance.
- **Metrics:** Track RU consumption, throttling, storage growth, request latency, availability, and replication status.
- **Alerts:** Notify operators about high RU usage, throttling, latency spikes, failed requests, availability issues, or abnormal access patterns.
- **Log Analytics:** Centralizes logs and metrics for dashboards, investigation, and long-term analysis.

Production monitoring should include alert thresholds, dashboards, and retention policies aligned with platform reliability and security requirements.

---

## Backup and Disaster Recovery

Cosmos DB provides managed capabilities that support backup, restore, and disaster recovery planning.

- **Automatic Backups:** Protect data through scheduled service-managed backups.
- **Point-in-Time Restore:** Supports recovery to a previous point in time when configured for supported accounts.
- **Geo-Replication:** Replicates data across Azure regions to improve resilience and regional availability.
- **Multi-region Availability:** Supports read and write availability strategies across regions based on application requirements.
- **Recovery Objectives:** Recovery Time Objective (RTO) and Recovery Point Objective (RPO) should be defined by environment and workload criticality.

Backup and recovery plans should be validated regularly, especially for production containers that store audit, cybersecurity, or governance data.

## Consistency Strategy

Azure Cosmos DB supports multiple consistency models.

Fortress should primarily use:

- Session Consistency (recommended)
- Strong Consistency only where business requirements demand it
- Eventual Consistency for analytics workloads

The selected consistency model should balance performance, availability, and data accuracy according to workload requirements.

## Data Lifecycle

Different Fortress datasets have different retention requirements.

Examples:

| Data | Retention |
|-------|-----------|
| AI Telemetry | 90 days |
| Security Events | 1 year |
| Audit Events | 7 years |
| Threat Intelligence Cache | 30 days |

TTL should automatically remove expired operational data while preserving regulated compliance records.

---

## Environment Separation

Development, Testing, and Production should each use separate Cosmos DB accounts.

Separate accounts provide:

- **Security isolation:** Prevents non-production identities and workloads from accessing production data.
- **Cost management:** Enables spend tracking and budget controls by environment.
- **Independent scaling:** Allows each environment to use appropriate throughput and capacity settings.
- **Independent monitoring:** Supports environment-specific alerts, dashboards, logs, and retention requirements.

Production event data, telemetry, and audit records should not be copied to non-production environments unless approved, sanitized, and governed by data protection requirements.

---

## Security Best Practices

- Apply least privilege access for users, applications, automation identities, and operators.
- Prefer Managed Identity and Microsoft Entra ID authentication over account keys.
- Store required secrets in Azure Key Vault.
- Never hardcode Cosmos DB keys, connection strings, or credentials.
- Use private networking for production workloads where appropriate.
- Rotate secrets and keys regularly when key-based access is used.
- Enable auditing through diagnostic logs and Azure Monitor.
- Perform regular access reviews for RBAC assignments and identities.
- Use separate Cosmos DB accounts for development, testing, and production.
- Configure alerts for throttling, abnormal access, high latency, and failed requests.

---

## Future Integration

Cosmos DB will integrate with several Fortress platform components:

- **Backend APIs:** Store and retrieve high-volume event, telemetry, and analytics data.
- **Azure Kubernetes Service (AKS):** Host workloads that connect securely to Cosmos DB using managed identity and private networking patterns.
- **Azure Key Vault:** Store Cosmos DB secrets when key-based access is required.
- **Azure SQL:** Store relational governance data while Cosmos DB stores high-volume NoSQL event and telemetry data.
- **Azure Monitor:** Provide metrics, logs, dashboards, and operational alerts.
- **GitHub Actions:** Support CI/CD validation and deployment workflows through approved identity and secret management patterns.
- **AI Shadow Engine:** Store AI shadow detection events, inference metadata, and analysis outputs.
- **Security Analytics:** Support event-driven investigation, threat intelligence enrichment, and incident timeline reconstruction.

Azure SQL and Cosmos DB complement one another. Azure SQL should store structured relational records requiring strong consistency, joins, and transactional integrity. Cosmos DB should store flexible, high-volume, event-oriented, and semi-structured data requiring scalable ingestion and low-latency access.

---

## Summary

Azure Cosmos DB provides the scalable NoSQL data foundation for Otic Fortress telemetry, cybersecurity analytics, audit event streams, AI shadow detection, and event-driven platform capabilities. It complements Azure SQL by supporting dynamic, high-volume, and semi-structured workloads while preserving enterprise requirements for security, monitoring, environment separation, and disaster recovery.
