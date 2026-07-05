name=CENTRALIZED_LOGGING.md
# Centralized Logging for Otic Fortress

Purpose
-------
Centralized logging provides a single, searchable, and auditable platform for operational, security, and AI governance telemetry. This document describes architecture, telemetry contracts, instrumentation guidance, and integration patterns for Azure Functions, Event Hubs, Service Bus, and distributed services.

Goals
- Centralize logs, traces, and metrics into Log Analytics / Application Insights / Azure Monitor.
- Preserve high-fidelity data for audits (AI Shadow Records) while controlling cost via sampling and per-tenant knobs.
- Ensure end-to-end correlation across HTTP, Service Bus, Event Hubs, and background processors.
- Provide SIEM-ready outputs for Microsoft Sentinel.

Architecture Overview
- Ingestion points:
  - Azure Functions and services: instrument with OpenTelemetry or Application Insights SDKs.
  - Event Hubs / Service Bus: platform metrics + diagnostic logs; consumer apps emit Shadow Records.
  - AI Shadow Records: emitted as structured events (Event Hubs or Service Bus) in addition to App Insights.
- Collection:
  - Services export OTLP (traces/metrics) to an OpenTelemetry Collector (OTEL) deployed centrally (AKS/VM/Container App).
  - OTEL exports to Azure Monitor (Application Insights / Azure Monitor exporters) and/or to Event Hubs for SIEM ingestion.
- Storage & analysis:
  - Logs/Traces: Application Insights + Log Analytics.
  - Long-term audit evidence: immutable Blob Storage (private endpoints and RBAC).
  - SIEM: Event Hubs -> Sentinel.

Telemetry contract highlights
- Use structured JSON logs with fields: timestamp, severity, serviceName, environment, tenantId, agentId (if applicable), correlationId, traceId, spanId, operationName, eventType, message, properties (key/value).
- AI Shadow Record (summarized):
  - auditId, tenantId, agentId, correlationId, timestampUtc, eventType, riskScore, policyOutcome, promptHash, responseHash, evidenceLink

Correlation & propagation
- Use a stable correlationId format:
  fortress:{tenantId}:{agentId}:{short-uuid}
- Always propagate:
  - HTTP header X-Correlation-Id
  - Messaging property correlationId for Service Bus / Event Hubs
  - Map traceId/spanId to logs via OpenTelemetry

Sensitive data & redaction
- Do not log raw secrets or unredacted PII.
- Implement prompt sanitization before storing prompts; store raw evidence only in immutable protected store and only with strict RBAC and audit.
- Use hashing (SHA256) for searchable references.

Instrumentation guidance (summary)
- Prefer OpenTelemetry for new services (OTLP). Use Application Insights SDKs where direct AI/telemetry coupling exists.
- Emit traces for:
  - HTTP requests, DB calls, AI inference calls, message enqueue/dequeue, tool calls.
- Emit metrics for:
  - ai.inference.latency.ms, ai.inference.tokens.*, service.queue.depth, eventhub.ingress, servicebus.deadletters
- Emit structured events for policy violations and approvals.

Sampling & cost management
- Apply adaptive sampling in Application Insights for noisy traces; exempt high-risk events and AIPolicyViolation events.
- Allow per-tenant sampling settings via the Control Plane.

OTEL Collector pattern
- Use a central collector to normalize telemetry and route to backends.
- Example exporters: azuremonitor, logging, kafka/eventhub
- Secure collector endpoints with TLS and authentication.

Platform components: quick notes
- Azure Functions
  - Configure APPLICATIONINSIGHTS_CONNECTION_STRING or instrument with OpenTelemetry for Python/Node/.NET.
  - Use host.json to control logging level and sampling.
- Event Hubs / Service Bus
  - Enable resource diagnostic settings -> Log Analytics + Event Hubs (for SIEM).
  - Consumers should enrich messages with correlationId and emit trace spans for processing.
- Distributed services
  - Use consistent logging library and structured JSON output.
  - Adopt semantic field names.

Diagnostics & forwarding
- Use Azure Diagnostic Settings to forward platform logs to:
  - Log Analytics (for interactive queries)
  - Event Hubs (for SIEM and long-term throughput)
  - Storage account (for immutable archive)

KQL, dashboards, alerts
- Build role-focused dashboards: SRE, AI Ops, Security, Executive.
- KQL examples included in kql_queries.md.
- Define alerts for errors, throttling, dead-letter growth, missing telemetry sources.

Runbooks & incident response
- Each alert must include:
  - Owner, immediate checks (KQL/commands), remediation steps, escalation path, post-incident review.
- Save runbooks in a Playbooks repo and link from alert definitions.

Deployment checklist
- Instrument services, validate correlation, enable diagnostic settings, deploy OTEL collector with secured endpoints, wire to Log Analytics / Sentinel, implement sampling & retention settings.

References
- Application Insights: https://learn.microsoft.com/azure/azure-monitor/app/app-insights-overview
- OpenTelemetry: https://opentelemetry.io/
- Azure Monitor exporters and OTEL collector docs.