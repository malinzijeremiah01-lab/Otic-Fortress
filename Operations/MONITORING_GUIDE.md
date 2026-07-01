# Monitoring Guide

**Owner:**Esiana Emmanuel: Cloud Infrastructure & DevOps Team  
**Version:** 1.0.0  
**Last Updated:** 2026-07-01  
**Audience:** SREs, DevOps Engineers, On-call Engineers  

---

## Purpose

This document provides operational guidance for monitoring the Fortress AI Cybersecurity Platform.

---

## Scope

This document covers:

- Operational dashboards
- Alert thresholds
- Daily health checks
- Weekly maintenance
- Monthly review

---

## Operational Dashboards

### Primary Dashboards

| Dashboard | Purpose | Link |
|-----------|---------|------|
| **Platform Health** | Overall service health | Azure Portal |
| **AKS Status** | Kubernetes cluster health | Azure Portal |
| **AI Performance** | AI service metrics | Application Insights |
| **Security Posture** | Security alerts | Defender Portal |
| **Cost Management** | Azure cost tracking | Cost Management |

### Dashboard Queries

```kql
// Platform Health
traces
| where timestamp > ago(1h)
| summarize total=count(), failed=countif(severityLevel == 1) by operation_Name
| extend success_rate = (total - failed) * 100 / total

// AKS Node Status
KubeNodeInventory
| where TimeGenerated > ago(1h)
| summarize count() by Status
Alert Thresholds
Critical Alerts
Alert	Threshold	Action
Service Down	500 errors > 1/min	Page on-call
AKS Node Down	Node not ready > 5 min	Page on-call
Database Down	Connection failure	Page on-call
Security Breach	Any critical alert	Page on-call
Warning Alerts
Alert	Threshold	Action
High CPU	> 80% for 10 min	Email
High Memory	> 80% for 10 min	Email
Error Rate	> 5% for 5 min	Email
High Latency	> 1s for 5 min	Email
Daily Health Checks
Morning Checklist
bash
# 1. Platform Health
kubectl get pods -n fortress-api
kubectl get pods -n fortress-control

# 2. Service Availability
curl -f https://api.fortress.ai/health

# 3. Database Status
az sql db show --resource-group fortress-prod-rg --server fortress-prod-sql --name fortress-prod

# 4. Key Vault Status
az keyvault show --name fortress-prod-kv

# 5. Security Alerts
az security alerts list --resource-group fortress-prod-rg

# 6. Cost
az consumption usage list --billing-period-name 2026-07
Health Check Script
bash
#!/bin/bash
# check-health.sh

echo "Checking Fortress Platform Health..."

# Check pods
kubectl get pods -n fortress-api -o wide

# Check services
kubectl get svc -n fortress-api

# Check ingress
kubectl get ingress -n fortress-api

# Check nodes
kubectl get nodes

echo "Health check complete."
Weekly Maintenance
Weekly Tasks
Day	Task	Owner
Monday	Review last week's alerts	On-call Engineer
Tuesday	Check backup status	DevOps Engineer
Wednesday	Review security alerts	Security Engineer
Thursday	Cost review	DevOps Engineer
Friday	Review incidents	Engineering Manager
Weekly Maintenance Script
bash
#!/bin/bash
# weekly-maintenance.sh

echo "Running Weekly Maintenance..."

# 1. Rotate logs
kubectl delete pods -l job-type=cleanup -n fortress-api

# 2. Check backup status
az sql db list -g fortress-prod-rg --server fortress-prod-sql

# 3. Clean temporary files
kubectl exec -n fortress-api <pod> -- rm -rf /tmp/*

echo "Weekly maintenance complete."
Monthly Review
Monthly Tasks
Task	Purpose
Review SLO adherence	Ensure SLAs are met
Review budget	Optimise costs
Review incidents	Identify patterns
Review security posture	Identify vulnerabilities
Monthly Metrics Report
sql
-- Monthly uptime report
SELECT
    DATEPART(year, timestamp) as year,
    DATEPART(month, timestamp) as month,
    (COUNT(IF(success = true)) * 100.0 / COUNT(*)) as uptime_percent
FROM requests
WHERE timestamp > DATEADD(month, -1, GETDATE())
GROUP BY DATEPART(year, timestamp), DATEPART(month, timestamp)
Troubleshooting Monitoring
Issue	Solution
Alerts not firing	Check alert query, data availability
Dashboard blank	Check permissions, data retention
Logs missing	Check Log Analytics agent
Useful Commands
bash
# View active alerts
az monitor alert list

# View metrics
az monitor metrics list --resource fortress-prod-aks --metric node_cpu_usage

# Query logs
az monitor log-analytics query --workspace fortress-prod-la --analytics-query "traces | top 10 by timestamp desc"

# Dashboard operations
az portal dashboard list
az portal dashboard show --name fortress-dashboard
Checklist
Dashboards created

Alert thresholds configured

Daily health checks documented

Weekly maintenance tasks defined

Monthly review process in place

