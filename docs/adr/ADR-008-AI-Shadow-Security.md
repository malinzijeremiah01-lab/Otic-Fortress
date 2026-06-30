# ADR-008: AI Shadow Security

## Status

Accepted

## Context

AI activity must be observable for security monitoring, compliance evidence, incident response, and governance review.

## Problem

Traditional application logs do not fully capture prompts, model decisions, tool calls, approvals, or AI-specific risk.

## Decision

Use AI Shadow as the observation and evidence layer for AI behavior.

## Alternatives Considered

- Rely only on application logs.
- Rely only on model provider logs.
- Capture AI evidence manually during audits.

## Rationale

AI Shadow gives Otic Fortress first-class telemetry for AI security and governance decisions.

## Consequences

AI workflows must produce structured, protected, and retention-controlled evidence.

## Trade-offs

Deep AI telemetry improves governance but requires careful privacy and retention controls.

## Related Documents

- [AI Security](../security/ai-security.md)
- [AI Governance Framework](../governance/ai-governance-framework.md)

## Document Control

| Item | Value |
|------|-------|
| Project | Otic Fortress |
| Document Type | Architecture Decision Record |
| Version | 1.0.0 |
| Status | Draft |
| Owner | Cloud, Security & Governance Team |
| Lead | Emmanuel Opolot |

## Executive Summary

Otic Fortress will use AI Shadow as the evidence and observation layer for AI behavior, including prompts, context, tool calls, decisions, approvals, and outcomes.

## Purpose

Record the decision to capture AI activity as security and governance telemetry.

## Scope

AI prompts, model responses, tool calls, agent identity, data access, policy decisions, risk scores, approval records, and output actions.

## Audience

AI engineers, security engineers, governance teams, SOC analysts, compliance teams, and auditors.

## Business Context

AI activity can create business impact without leaving traditional application logs. AI Shadow provides visibility needed for security, governance, and compliance.

## Architecture Overview

```text
AI Runtime -> AI Shadow Capture -> Normalization -> Evidence Store -> Monitoring / Governance
```

## Core Components

| Component | Decision Role |
|-----------|---------------|
| Capture Layer | Observes AI activity. |
| Normalizer | Structures events. |
| Evidence Store | Preserves governance records. |
| Monitoring Integration | Sends signals to security operations. |

## Data Flow

AI events are captured from runtime workflows, normalized, enriched with policy and risk context, stored, and forwarded to monitoring and governance dashboards.

## Azure Services Used

Azure Monitor, Log Analytics, Microsoft Sentinel, Azure Storage, Microsoft Entra ID, Azure API Management, and Azure Key Vault.

## Security Considerations

AI Shadow data may include sensitive prompts or data references. It requires strict access control, retention, redaction, and tamper resistance.

## Governance Considerations

Captured events must support explainability, approvals, compliance mapping, and incident response.

## Monitoring and Observability

Monitor capture failures, event volume, redaction failures, suspicious prompt patterns, and denied tool calls.

## Failure Scenarios

| Scenario | Response |
|----------|----------|
| Capture pipeline fails | Block high-risk actions or mark evidence degraded. |
| Sensitive data captured unexpectedly | Redact, restrict access, and review controls. |

## Configuration Guidance

Define event schemas, retention rules, redaction policies, access roles, and ingestion health alerts.

## Design Decisions

Otic Fortress will make AI activity observable as a first-class security signal.

## Trade-offs

Deep AI telemetry improves governance but requires careful privacy and retention controls.

## Future Enhancements

Prompt attack detection, event minimization profiles, and evidence integrity verification.

## References

- [AI Security](../security/ai-security.md)
