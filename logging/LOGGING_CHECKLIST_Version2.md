name=LOGGING_CHECKLIST.md
# Centralized Logging — Pre-Production Checklist

Use this checklist before enabling production monitoring and alerts.

Instrumentation
- [ ] Services instrumented with OpenTelemetry or Application Insights SDK
- [ ] Structured logging format verified (JSON with required fields)
- [ ] Correlation ID and trace propagation validated across HTTP, Service Bus, Event Hubs
- [ ] AI Shadow events emitted and sanitized where needed

Collector & Ingestion
- [ ] OTEL Collector deployed and reachable by services
- [ ] Collector exports configured for Azure Monitor and Event Hubs
- [ ] Secrets (connection strings) stored in Key Vault and injected via managed identity

Platform & Diagnostic Settings
- [ ] Diagnostic settings enabled for Event Hubs, Service Bus, Azure SQL, AKS -> Log Analytics + Event Hubs + Storage (archive)
- [ ] Key Vault diagnostics enabled and forwarded to Sentinel/Log Analytics

Dashboards & Queries
- [ ] SRE, AI Ops, Security, and Exec dashboards created
- [ ] KQL queries validated (error rates, throttling, dead-letter growth, policy violations)

Alerts & Runbooks
- [ ] Critical alerts configured (API errors, Event Hubs throttling, dead-letter growth, AIPolicyViolation)
- [ ] Runbooks linked to each alert and owners assigned
- [ ] PagerDuty/Slack/Email action groups configured and tested

Data Protection & Retention
- [ ] Prompt sanitization implemented (no raw secrets in logs)
- [ ] Immutable evidence storage configured for high-fidelity audit logs
- [ ] Retention policies set per environment

Testing & Validation
- [ ] End-to-end test executed: simulate request -> trace -> message -> consumer -> Shadow Record
- [ ] Failover tests for collector and downstream storage
- [ ] Cost sampling rules validated (sampling config and exemptions)

Compliance & Review
- [ ] SOC/Compliance sign-off on retention and access controls
- [ ] Quarterly review schedule planned for roles and access assignments

Owner sign-off:
- Instrumentation owner: ______________________
- SRE owner: __________________________________
- Security owner: ______________________________
- Date: _______________________________________