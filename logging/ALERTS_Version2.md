name=ALERTS.md
# Example Alerts & Runbook Pointers

This file lists example alerts you should create and short runbook actions.

1) API High Error Rate (Critical)
- Condition: 5xx error rate > 1% over 5 minutes (Application Insights)
- Action Group: PagerDuty + Slack + Email + Security Webhook
- Immediate checks:
  - Check recent deployments
  - KQL: requests | where timestamp > ago(10m) | summarize errs=countif(success==false) , total=count() by operation_Name | extend rate=errs*100.0/total
  - Check dependency failures (dependencies table)
- Remediation:
  - Rollback last deploy if correlated to deployment
  - Fix dependency or scale backend
- Escalation: SRE lead -> Engineering on-call

2) Event Hubs Throttling (Critical)
- Condition: ThrottledRequests > 0 for 5 minutes
- Immediate checks:
  - Check Event Hubs metrics and partition distribution
  - Verify producer rates and autoscale settings
- Remediation:
  - Increase throughput unit or enable auto-inflate
  - Throttle producers or queue bursts into storage

3) Service Bus Dead-Letter Growth (Critical)
- Condition: DeadletteredMessages growth > baseline over 10 minutes
- Immediate checks:
  - Inspect dead-letter reasons for recent messages
  - KQL sample in kql_queries.md
- Remediation:
  - Pause producers, restart consumers, reprocess after fix

4) Missing Telemetry from a Service (Warning)
- Condition: No traces/logs from cloud_RoleName X for 15 minutes
- Immediate checks:
  - Validate service health and pod status (AKS)
  - Check collector connectivity
- Remediation:
  - Restart service pod/instance, investigate network

5) AIPolicyViolation Spike (Critical)
- Condition: > N policy violations in 5 minutes for a tenant
- Immediate checks:
  - Display top Shadow Records and evidence links
  - Check agent configuration and recent changes
- Remediation:
  - Pause agent actions if high risk, escalate to Security & Product Owner

Runbook guidance
- Each alert should link to a full runbook in Playbooks repo.
- Runbooks must include: owner, KQL commands, CLI snippets (kubectl/az), immediate remediation, escalation contacts, and post-incident tasks.