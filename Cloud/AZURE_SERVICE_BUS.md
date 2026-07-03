# Azure Service Bus

## Purpose

Azure Service Bus is Microsoft's enterprise messaging service for reliable asynchronous communication between distributed services, applications, and workloads. It provides queues, topics, subscriptions, dead-letter handling, retries, scheduling, duplicate detection, and ordered message processing for cloud-native and hybrid architectures.

Within the Otic Fortress AI Governance and Cybersecurity Platform, Azure Service Bus provides a reliable messaging layer between backend services, workflow processors, security automation, governance components, and notification systems.

Service Bus is important in an event-driven architecture because it decouples producers from consumers. Services can publish work or events without requiring the downstream service to be available at the same moment. This improves resilience, supports independent scaling, reduces tight coupling, and allows Fortress workflows to continue even when individual components are busy, restarting, or temporarily unavailable.

---

## Why Fortress Uses Azure Service Bus

Fortress uses Azure Service Bus for workloads that require reliable asynchronous processing, controlled delivery, and durable communication across distributed backend services.

Primary use cases include:

- **Approval workflows:** Route access requests, policy exceptions, AI usage approvals, and administrative approvals to the correct workflow processors.
- **AI Governance workflows:** Coordinate review, classification, escalation, and remediation actions related to AI model usage, policy violations, and governance decisions.
- **Policy enforcement:** Deliver policy evaluation events and enforcement actions to backend services without blocking the original user or system request.
- **Incident response orchestration:** Coordinate security investigation steps, enrichment tasks, remediation actions, and notification flows.
- **Notification delivery:** Queue email, webhook, dashboard, and operational notifications for reliable background delivery.
- **Background processing:** Offload long-running tasks such as report generation, evidence collection, compliance checks, and telemetry enrichment.
- **Communication between backend microservices:** Allow independently deployed services to exchange commands and events without direct point-to-point dependencies.
- **Reliable message delivery:** Preserve work items and business events until they are successfully processed or explicitly moved to a dead-letter queue.

These workloads require reliable messaging instead of direct synchronous API calls because they often involve multi-step processing, downstream service dependencies, retries, operational delays, and security-sensitive audit trails. Direct synchronous calls increase coupling and can cause user-facing failures when a dependent service is slow or unavailable. Service Bus allows Fortress to accept work, persist it durably, process it independently, retry safely, and preserve failed messages for investigation.

---

## Proposed Naming Convention

Proposed Service Bus namespace names:

```text
sb-otic-fortress-dev
sb-otic-fortress-test
sb-otic-fortress-prod
```

Proposed queue names:

```text
approval-queue
incident-queue
notification-queue
workflow-queue
```

Proposed topic names:

```text
policy-events
security-events
system-events
```

Proposed subscription names:

```text
audit-service
notification-service
governance-service
```

Namespace naming convention format:

```text
sb-<platform-name>-<environment>
```

Messaging entity naming convention format:

```text
<domain>-<entity-type>
```

- `sb`: Identifies the Azure resource as a Service Bus namespace.
- `otic-fortress`: Identifies the platform or workload.
- `dev`, `test`, `prod`: Identifies the target environment.
- Queue names such as `approval-queue` and `incident-queue`: Identify durable work queues for a specific processing domain.
- Topic names such as `policy-events` and `security-events`: Identify event streams that can be consumed by multiple subscribers.
- Subscription names such as `audit-service` and `governance-service`: Identify the downstream service or capability that receives a filtered copy of topic messages.

This convention supports predictable automation, clear ownership, environment separation, monitoring, access control, and operational troubleshooting.

---

## Messaging Architecture

Fortress should use Service Bus queues, topics, and subscriptions according to the communication pattern required by each workload.

- **Queues:** Provide one-to-one durable messaging where each message is processed by a single consumer. Queues should be used for commands, work items, approvals, notifications, incident tasks, and background processing jobs.
- **Topics:** Provide publish-subscribe messaging where a single event can be delivered to multiple independent subscribers. Topics should be used for policy events, security events, platform events, and AI governance events.
- **Subscriptions:** Provide independent views of a topic for downstream services. Each subscription can have its own filters, delivery state, retry behavior, and dead-letter queue.
- **Dead-letter queues:** Store messages that cannot be delivered or processed successfully. Dead-letter queues should be monitored and reviewed as part of operational incident handling.
- **Message retry:** Allows transient processing failures to be retried before the message is considered failed. Retries should be used for temporary dependency failures such as downstream API timeouts or database throttling.
- **Duplicate detection:** Prevents duplicate messages from being accepted within a configured detection window. Duplicate detection should be used for critical commands, approval actions, and workflow triggers that must not be processed more than once.
- **Message ordering:** Preserves processing sequence where order matters. Ordering should be used for state transitions, incident timelines, approval lifecycle events, and policy version changes.
- **Scheduled messages:** Delay message delivery until a specific time. Scheduled messages should be used for delayed reminders, escalation windows, deferred workflow steps, and follow-up checks.
- **Message sessions:** Group related messages and support ordered, stateful processing. Sessions should be used when multiple messages belong to the same approval request, incident, tenant workflow, or governance case.

Service Bus should be treated as a reliability boundary in the Fortress control plane. Producers should publish commands or events quickly, and consumers should process messages idempotently with clear retry, failure, and observability behavior.

---

## Queue Strategy

Queues should be used when Fortress needs reliable one-to-one delivery of commands or work items. Each queue should have a clear owner, message schema, retry policy, dead-letter handling process, and monitoring threshold.

| Queue | Purpose |
| --- | --- |
| `approval-queue` | Carries approval requests, access decisions, exception reviews, AI usage approval tasks, and governance review actions. |
| `incident-queue` | Carries incident response tasks, investigation requests, enrichment jobs, containment actions, and remediation work items. |
| `notification-queue` | Carries email, webhook, dashboard, alert, and integration notification requests for asynchronous delivery. |
| `workflow-queue` | Carries general workflow execution tasks, state transitions, scheduled actions, and background orchestration steps. |

### Approval Queue

The Approval Queue should support governance and administrative approval flows. Messages may include requester context, tenant identifiers, requested action, policy reference, approval status, risk level, and correlation identifiers.

This queue should prioritize idempotency, ordering by approval case, and strong audit traceability.

### Incident Queue

The Incident Queue should support security response orchestration. Messages may include incident identifiers, severity, affected resource, recommended action, enrichment status, ownership, and escalation metadata.

This queue should support retries, dead-letter review, and integration with monitoring and alerting workflows.

### Notification Queue

The Notification Queue should support reliable outbound notification delivery. Messages may include recipient information, notification type, template reference, delivery channel, priority, and correlation identifiers.

Notification processing should tolerate transient failures from downstream providers and should avoid blocking core platform workflows.

### Workflow Queue

The Workflow Queue should support background workflow execution across the platform. Messages may include workflow name, workflow instance identifier, tenant context, next step, schedule time, and execution metadata.

This queue should support scheduled messages, sessions, and retry policies for long-running governance and cybersecurity processes.


## Message Lifecycle

Typical Fortress message flow:

Producer
↓
Queue / Topic
↓
Consumer
↓
Business Processing
↓
Complete Message

If processing fails:

Retry
↓
Dead-letter Queue
↓
Operations Review
↓
Replay or Archive
---

## Topic Strategy

Topics should be used when Fortress publishes events that multiple backend services may need to consume independently. Topics allow producers to publish once while audit, notification, analytics, governance, and workflow services each receive their own copy through subscriptions.

Recommended topics:

| Topic | Purpose |
| --- | --- |
| `policy-events` | Publishes policy creation, update, evaluation, violation, exception, and enforcement events. |
| `security-events` | Publishes detections, incidents, alerts, threat intelligence matches, enrichment events, and response outcomes. |
| `platform-events` | Publishes tenant, user, system configuration, operational state, deployment, and service health events. |
| `ai-events` | Publishes AI usage, AI shadow detections, model evaluation results, prompt risk events, inference metadata, and governance signals. |

Subscriptions should be named for the consuming service or bounded context, such as `audit-service`, `notification-service`, `governance-service`, `workflow-engine`, or `security-analytics`.

Multiple backend services can subscribe independently without affecting one another. For example, a policy violation event can be consumed by the audit service for compliance logging, the notification service for alerts, the governance service for review, and the workflow engine for remediation orchestration. Each subscriber can process at its own pace, apply its own filters, and maintain its own failure handling.

---

## Reliability Strategy

Azure Service Bus improves Fortress reliability by providing durable message storage, controlled delivery, retry handling, and failure isolation between services.

- **Guaranteed delivery:** Messages are persisted until successfully completed, expired, or moved to a dead-letter queue.
- **Retry policies:** Transient failures can be retried without losing the original message or forcing the producer to retry the entire workflow.
- **Dead-letter handling:** Failed messages are preserved for investigation, correction, replay, or manual intervention.
- **Poison messages:** Messages that repeatedly fail processing should be isolated in the dead-letter queue to prevent them from blocking healthy workload processing.
- **Message expiration:** Time-sensitive messages should use appropriate time-to-live values so stale approvals, alerts, or workflow tasks do not execute after they are no longer valid.
- **Idempotent processing:** Consumers should safely handle duplicate deliveries, repeated retries, and replayed messages by using message identifiers, correlation identifiers, and operation state checks.
- **High availability:** Service Bus provides managed availability capabilities that reduce the operational burden of running messaging infrastructure directly.

Reliability planning should include clear ownership for each queue and topic, defined retry thresholds, dead-letter review procedures, monitoring alerts, and message schema versioning. Critical governance and security workflows should be designed so that processing can resume safely after service restarts, deployment changes, or transient Azure service issues.

---

## Security

Azure Service Bus should be protected with layered security controls appropriate for enterprise AI governance and cybersecurity workloads.

- **Microsoft Entra ID authentication:** Enables identity-based access to Service Bus without relying only on shared access keys or connection strings.
- **Managed Identity:** Allows Azure-hosted Fortress workloads to send and receive messages without storing credentials in application settings, container images, or pipeline files.
- **RBAC:** Controls management-plane and data-plane access using least privilege role assignments for users, services, automation identities, and workload identities.
- **Private Endpoints:** Provide private connectivity to Service Bus through Azure Private Link, reducing public network exposure for production messaging workloads.
- **Encryption at Rest:** Protects persisted messages and metadata using Azure-managed encryption capabilities.
- **Encryption in Transit:** Protects messages moving between Fortress services and Service Bus over secure network connections.
- **Network Isolation:** Restricts access paths using private networking, firewall controls, approved virtual networks, and environment-specific network boundaries.
- **Azure Key Vault integration:** Stores connection strings, shared access keys, certificates, and related secrets when key-based access is required. Managed identity should remain the preferred access pattern.

Production Service Bus namespaces should use the strictest identity, networking, monitoring, and operational controls. Shared access policies and connection strings should be minimized, scoped narrowly, stored securely, and rotated according to enterprise security requirements.

---

## Monitoring

Service Bus monitoring should provide visibility into messaging health, consumer performance, reliability risks, and security-relevant activity.

- **Azure Monitor:** Captures platform metrics for queues, topics, subscriptions, message counts, errors, throttling, and resource health.
- **Application Insights:** Correlates producer and consumer operations with application traces, dependency calls, exceptions, and end-to-end workflow latency.
- **Diagnostic Logs:** Provide operational and audit logs for management activity, runtime behavior, and troubleshooting.
- **Metrics:** Track active messages, dead-lettered messages, scheduled messages, completed messages, abandoned messages, server errors, user errors, and throttled requests.
- **Alerts:** Notify operators when message backlog, dead-letter count, processing latency, or delivery failures exceed approved thresholds.
- **Log Analytics:** Centralizes Service Bus logs and metrics for dashboards, investigation, retention, and correlation with application and security telemetry.
- **Dead-letter monitoring:** Detects messages that failed processing and require review, correction, replay, or escalation.
- **Queue depth monitoring:** Tracks backlog growth to identify slow consumers, failed processors, capacity constraints, or downstream outages.
- **Message latency monitoring:** Measures the time between message enqueue and successful processing to validate workflow performance and service-level objectives.

Production monitoring should include dashboards and alerts for critical queues, topics, and subscriptions. Dead-letter queues for approval, incident, and policy workflows should be treated as operationally significant and reviewed regularly.

---

## Environment Separation

Development, Testing, and Production should each have separate Service Bus namespaces.

Environment separation provides:

- **Security isolation:** Prevents non-production identities and workloads from sending to or receiving from production messaging entities.
- **Operational safety:** Reduces the risk of development or testing activity triggering production workflows.
- **Independent lifecycle management:** Allows queues, topics, schemas, and subscriptions to evolve safely by environment.
- **Environment-specific monitoring:** Supports separate alert thresholds, dashboards, log retention, and operational response policies.
- **Cost tracking:** Enables messaging costs to be reported and governed by environment.
- **Data protection:** Prevents production governance, security, approval, and incident messages from leaking into non-production environments.

Production messages should not be copied into development or testing environments unless explicitly approved, sanitized, and governed by data protection requirements.

---

## Security Best Practices

- Apply least privilege access to users, applications, managed identities, service principals, and automation workflows.
- Prefer Managed Identity and Microsoft Entra ID authentication over connection strings and shared access keys.
- Do not hardcode Service Bus connection strings, keys, or credentials in source code, pipeline files, documentation, container images, or configuration files.
- Store required secrets in Azure Key Vault and rotate them according to enterprise security policy.
- Use private networking for production namespaces where appropriate.
- Enable diagnostic logs, Azure Monitor metrics, alerting, and centralized Log Analytics collection.
- Monitor dead-letter queues, failed processing, abnormal access patterns, and unusual message volume.
- Use separate namespaces for development, testing, and production.
- Review RBAC assignments, shared access policies, managed identities, and subscription filters on a regular schedule.
- Define message schemas, ownership, retention, retry, and dead-letter procedures for each queue and topic.

---

## Future Integration

Azure Service Bus will integrate with several Fortress platform components:

- **Backend APIs:** Publish commands and events for approvals, workflows, governance decisions, notifications, and incident orchestration without blocking user-facing requests.
- **Azure Kubernetes Service (AKS):** Host message producers and consumers as containerized microservices using managed identity, private networking, and environment-specific configuration.
- **GitHub Actions:** Support CI/CD workflows that validate messaging-related configuration and deploy services using approved identity and secret management patterns.
- **Azure Key Vault:** Store Service Bus secrets only when key-based access is required and support secure retrieval by approved workloads.
- **Azure Event Hubs:** Complement Service Bus for high-volume telemetry and streaming scenarios. Event Hubs should be used for large-scale event ingestion, while Service Bus should be used for reliable commands, workflows, and enterprise messaging.
- **Azure Monitor:** Provide metrics, logs, alerts, dashboards, and operational visibility across queues, topics, subscriptions, and message consumers.
- **AI Shadow Engine:** Publish and consume AI shadow detection events, governance signals, analysis tasks, and remediation workflows.
- **Workflow Engine:** Coordinate long-running approvals, incident response steps, scheduled tasks, retries, escalations, and policy enforcement workflows.

Service Bus fits into the Fortress event-driven architecture as the durable messaging backbone for control-plane workflows. It allows the platform to separate request handling from background processing, publish events to multiple consumers, recover from transient failures, and preserve security-critical work items for audit and investigation.

# Architecture Flow
Backend APIs
      │
      ▼
Azure Service Bus
      │
 ┌────┼────────────┐
 │    │            │
 ▼    ▼            ▼
Workflow Service
Notification Service
Audit Service
      │
      ▼
Azure SQL

---

## Summary

Azure Service Bus is the reliable messaging backbone of the Fortress Control Plane. It enables durable asynchronous communication between distributed services, supports approval and governance workflows, powers incident response orchestration, and improves reliability through retries, dead-letter handling, idempotent processing, and environment isolation.

By combining Microsoft Entra ID, Managed Identity, RBAC, private networking, encryption, Azure Key Vault, Azure Monitor, and Log Analytics, Service Bus provides an enterprise-ready foundation for secure, observable, and resilient event-driven architecture across the Otic Fortress AI Governance and Cybersecurity Platform.
