name=kql_queries.md
# Useful KQL Queries for Centralized Logging

## Recent errors by service
requests
| where timestamp > ago(1h)
| where success == false
| summarize Errors = count() by cloud_RoleName, operation_Name, bin(timestamp, 5m)
| order by Errors desc

## Event Hubs ingress & throttling (last hour)
AzureMetrics
| where TimeGenerated > ago(1h)
| where ResourceProvider == "MICROSOFT.EVENTHUB"
| where MetricName in ("IncomingMessages", "ThrottledRequests")
| summarize Total = sum(Total) by Resource, MetricName, bin(TimeGenerated, 5m)

## Service Bus dead-letter growth
AzureMetrics
| where TimeGenerated > ago(24h)
| where ResourceProvider == "MICROSOFT.SERVICEBUS"
| where MetricName == "DeadletteredMessages"
| summarize Total = sum(Total) by EntityName, bin(TimeGenerated, 10m)
| order by Total desc

## AI Policy Violations (Shadow Records)
customEvents
| where timestamp > ago(24h) and name == "AIPolicyViolation"
| extend tenantId = tostring(customDimensions.tenantId), agentId = tostring(customDimensions.agentId)
| summarize Violations = count() by tenantId, agentId, bin(timestamp, 1h)
| order by Violations desc

## Missing telemetry (no traces from a service in last 15m)
traces
| where timestamp > ago(1h)
| summarize LastSeen = max(timestamp) by cloud_RoleName
| where LastSeen < ago(15m)

## Prompt redaction heuristic (detect prompt-like content with sensitive tokens)
customEvents
| where timestamp > ago(24h) and name == "PromptCaptured"
| extend promptSnippet = tostring(customDimensions.promptSnippet)
| where promptSnippet matches regex @"\b(SSN|social security|credit card|ccv|password|pwd|api_key|secret)\b"
| project timestamp, TenantId = tostring(customDimensions.tenantId), AgentId = tostring(customDimensions.agentId), promptSnippet