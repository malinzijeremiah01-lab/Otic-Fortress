# Monitoring & Observability Architecture

**Owner:**Esiana Emmanuel: Cloud Infrastructure & DevOps Team  
**Version:** 1.0.0  
**Last Updated:** 2026-07-01  
**Audience:** SREs, DevOps Engineers, Platform Engineers  

---

## Purpose

This document defines the monitoring, observability, and alerting architecture for the Fortress AI Cybersecurity Platform. It ensures comprehensive visibility into application performance, infrastructure health, security posture, and AI workload behaviour.

---

## Scope

This document covers:

- Azure Monitor and Log Analytics
- Application Insights
- Metrics collection and aggregation
- Alert rules and notification channels
- Dashboards and reporting
- Health checks and SLO tracking

---

## Overview

### Why Observability Matters for Fortress

Fortress monitors AI agents, security events, and critical business workflows. We need:

- **Real-time visibility** into AI agent behaviour
- **Performance tracking** of all services
- **Security monitoring** for threats and anomalies
- **Cost visibility** for AI workloads
- **Compliance evidence** for audits

---

## Architecture

```mermaid
graph TB
    subgraph "Data Sources"
        AKS[AKS Metrics]
        APP[Application Logs]
        AI[AI Services]
        SQL[Azure SQL]
        COSMOS[Cosmos DB]
        K8S[Kubernetes Events]
        SEC[Security Events]
    end

    subgraph "Ingestion"
        MON[Azure Monitor]
        AGENT[Log Analytics Agent]
        INSIGHT[Application Insights SDK]
        DIAG[Diagnostic Settings]
    end

    subgraph "Storage"
        LAW[Log Analytics Workspace]
        METRICS[Metrics Store]
        TRACES[Trace Store]
    end

    subgraph "Analysis"
        QUERY[Log Queries]
        ALERT[Alert Rules]
        DASH[Dashboards]
        WORKBOOK[Workbooks]
    end

    subgraph "Action"
        NOTIFY[Notifications]
        AUTO[Auto Remediation]
        TICKET[Incident Creation]
    end

    AKS --> MON
    APP --> INSIGHT
    AI --> MON
    SQL --> DIAG
    COSMOS --> DIAG
    K8S --> AGENT
    SEC --> MON

    MON --> LAW
    INSIGHT --> TRACES
    DIAG --> METRICS

    LAW --> QUERY
    LAW --> ALERT
    METRICS --> DASH
    TRACES --> WORKBOOK

    ALERT --> NOTIFY
    ALERT --> AUTO
    ALERT --> TICKET
Components
Azure Monitor
Centralized monitoring service that collects metrics, logs, and traces from all Azure resources.

Log Analytics Workspace
Environment	Workspace Name	Retention
Development	fortress-dev-la	30 days
QA	fortress-qa-la	30 days
Staging	fortress-staging-la	90 days
Production	fortress-prod-la	365 days
Application Insights
Used for application performance monitoring:

Request rates, response times, error rates

Dependency tracking (SQL, HTTP, AI services)

Performance exceptions and stack traces

User and session analytics

Key Metrics
Infrastructure Metrics
Category	Key Metrics
AKS	CPU, Memory, Pod count, Node health
Azure SQL	DTU, Connections, Query latency, Deadlocks
Cosmos DB	RU/s, Request rate, Throttling, Data size
Storage	Transactions, Availability, Latency
Key Vault	Secret access, Throttling, Errors
Application Metrics
Service	Key Metrics
API Gateway	Request rate, Error rate, P95 latency
Control Plane	Request rate, Error rate, P95 latency
AI Shadow Engine	Tokens processed, Inference time, Hallucination rate
Event Processor	Events/sec, Processing latency, Backlog size
Policy Engine	Policy evaluations/sec, Violation rate
AI Workload Metrics
Metric	Description	Alert Threshold
Token Usage	OpenAI token consumption	> 1M tokens/hour
Inference Latency	Time to generate response	> 2 seconds P95
Hallucination Rate	% of incorrect responses	> 5%
Policy Violations	Violations per 1000 requests	> 10
Alerting
Alert Rules
Alert Name	Severity	Condition	Action
AKS High CPU	Warning	CPU > 80% for 10 min	Email, Slack
API High Error Rate	Critical	Error Rate > 5% for 5 min	Email, Slack, PagerDuty
SQL DTU Exceeded	Warning	DTU > 75% for 15 min	Email
Cosmos Throttling	Warning	Throttling > 1% for 15 min	Email
AI Token Spike	Warning	Token usage > 1M/hour	Email
Key Vault Access Error	Critical	Failed access > 10 in 5 min	Email, PagerDuty
Event Hub Backlog	Warning	Backlog > 10,000 messages	Email
Notification Channels
Channel	Priority	Purpose
Slack	All	Team notifications
Email	All	Documentation and audit
PagerDuty	Critical	On-call escalation
Dashboards
Fortress Platform Health Dashboard






Sample KQL Queries
kql
// AKS CPU Usage
KubePodInventory
| where TimeGenerated > ago(1h)
| where Namespace startswith "fortress"
| summarize AvgCPU = avg(CPUUsage) by Namespace, PodName

// API Error Rate
requests
| where timestamp > ago(30m)
| where success == false
| summarize ErrorCount = count() by operation_Name
| extend ErrorRate = (ErrorCount / total) * 100

// AI Inference Latency
dependencies
| where timestamp > ago(1h)
| where type == "AzureOpenAI"
| summarize P95 = percentile(duration, 95) by operation_Name
SLO Tracking
Service	SLO	Measurement
API Gateway	99.95% availability	Request success rate
Control Plane	99.95% availability	Request success rate
AI Inference	< 2s P95 latency	Response time
Event Processing	< 5s latency	Event to processing time
Troubleshooting
Common Issues
Issue	Diagnosis	Solution
No logs in Log Analytics	Check Log Analytics agent	Restart agent, verify configuration
Alert not firing	Check alert query and threshold	Adjust query, verify data exists
Slow dashboard	Large query scope	Reduce time range, use summarization
Useful Commands
bash
# Query logs via Azure CLI
az monitor log-analytics query \
  --workspace fortress-prod-la \
  --analytics-query "traces | where severityLevel == 1"

# Get metrics
az monitor metrics list \
  --resource /subscriptions/xxx/resourceGroups/fortress-prod-rg/providers/Microsoft.ContainerService/managedClusters/fortress-prod-aks \
  --metric "node_cpu_usage"
Checklist
Log Analytics workspace created

Application Insights configured

Diagnostic settings enabled for all resources

Alert rules defined for critical metrics

Notification channels configured

Dashboards created for key stakeholders

SLOs defined and tracked

References
AKS.md

RUNBOOK.md

This document is part of the Fortress Engineering Knowledge System (EKS).

text
