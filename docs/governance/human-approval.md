# Human Approval Model

## Document Control

| Item | Value |
|------|-------|
| Project | Otic Fortress |
| Document Type | Governance Procedure |
| Version | 1.0.0 |
| Status | Draft |
| Owner | Cloud, Security & Governance Team |
| Lead | Emmanuel Opolot |

## Executive Summary

Human approval ensures that high-impact AI actions are reviewed by accountable people before execution. Approval requirements are based on policy, risk score, data sensitivity, tool capability, and business impact.

## Purpose

Define when and how Otic Fortress routes AI actions for human approval.

## Scope

High-risk AI actions, administrative actions, sensitive data access, external communications, irreversible operations, compliance-sensitive workflows, and approval evidence.

## Audience

Governance leads, approvers, AI engineers, security teams, product owners, and auditors.

## Business Context

AI systems can recommend or perform actions that affect customers, finances, operations, and compliance. Human approval provides accountability where automation alone is not appropriate.

## Governance Overview

Human approval workflows for high-impact AI actions pause execution, present evidence to accountable approvers, capture the decision rationale, and release or deny the action based on policy. Approval is required for the following actions:

| Action Requiring Approval | Reason |
|---------------------------|--------|
| Creating AI agents | Prevent unowned or ungoverned agent creation. |
| Deleting AI agents | Preserve operational continuity and auditability. |
| Production deployment | Ensure release readiness and control validation. |
| Granting new tools | Prevent unauthorized capability expansion. |
| Connecting to databases | Protect sensitive structured data. |
| Connecting to Microsoft 365 | Protect enterprise collaboration and document data. |
| Accessing confidential documents | Enforce data classification and need-to-know access. |
| Sending external communications | Prevent unauthorized customer or partner impact. |
| Financial transactions | Require accountability for monetary impact. |
| Customer-facing autonomous actions | Protect customer trust and service quality. |
| Updating enterprise policies | Preserve governance integrity. |
| Changing security settings | Prevent unauthorized control weakening. |
| Disabling monitoring | Protect detection and audit visibility. |
| Deleting audit records | Preserve evidence and compliance records. |

## Architecture Overview

```text
AI Action -> Policy Decision -> Risk Tier -> Approval Queue -> Approver Decision -> Execution / Denial
                              |                 |                 |
                              v                 v                 v
                         Rationale          SLA Tracking       Evidence
```

## Core Components

| Component | Role |
|-----------|------|
| Approval Gateway | Holds actions requiring review. |
| Approver Groups | Define accountable reviewers. |
| Decision Record | Captures approval or denial rationale. |
| SLA Monitor | Tracks pending approvals. |

## Data Flow

Actions requiring approval are paused, enriched with context, routed to the appropriate approver, decided, logged, and then executed or denied.

## Azure Services Used

Microsoft Entra ID, Azure Monitor, Log Analytics, Azure Storage, Azure API Management, and notification integrations.

## Security Considerations

Approver identity must be verified. Approval links must not allow unauthorized action. Emergency approvals require additional monitoring.

## Governance Considerations

Approval policies must define who can approve, what evidence is shown, how conflicts are handled, and when approval expires.

## Monitoring and Observability

Monitor approval volume, approval latency, denial rates, expired approvals, emergency approvals, and repeated overrides.

## Failure Scenarios

| Scenario | Response |
|----------|----------|
| Approver unavailable | Escalate based on governance policy. |
| Approval timeout | Deny or expire action by default. |
| Conflicting approvals | Route to governance owner for resolution. |

## Configuration Guidance

Configure approver groups, escalation paths, approval SLAs, risk thresholds, evidence fields, and expiry rules.

## Design Decisions

Otic Fortress requires explicit human accountability for material AI actions.

## Trade-offs

Approval gates slow automation but protect against irreversible or harmful AI behavior.

## Future Enhancements

Delegated approvals, adaptive approval thresholds, mobile approval workflows, and approval quality analytics.

## References

- [ADR-009 Human Approval](../adr/ADR-009-Human-Approval.md)
- [Risk Engine](../security/risk-engine.md)
