# Risk Engine Security Architecture

## Document Control

| Item | Value |
|------|-------|
| Project | Otic Fortress |
| Document Type | Security Architecture |
| Version | 1.0.0 |
| Status | Draft |
| Owner | Cloud, Security & Governance Team |
| Lead | Emmanuel Opolot |

## Executive Summary

The Risk Engine calculates dynamic risk for identities, AI agents, actions, data access, tool use, and environment context. Risk scores influence policy decisions, approval requirements, monitoring priority, and trust score updates.

Risk scoring uses six risk levels so teams can apply proportional response, from normal informational activity through catastrophic actions that require executive escalation.

## Purpose

Define the risk scoring architecture used by Otic Fortress.

## Scope

User risk, workload risk, agent risk, action risk, data sensitivity, tool capability, operational impact, and historical behavior.

## Audience

Security engineers, risk owners, AI governance teams, platform engineers, compliance teams, and auditors.

## Business Context

Static permissions are insufficient for autonomous AI workflows. Dynamic risk scoring helps Otic Fortress apply proportional control to actions with different impact levels.

## Architecture Overview

```text
Signals -> Normalization -> Scoring Model -> Risk Tier -> Policy / Approval / Monitoring
             |                 |              |
             v                 v              v
          Evidence        Explanation      Trust Score
```

## Risk Levels

| Level | Meaning |
|------|---------|
| Informational | Normal activity |
| Low | Minor observation |
| Medium | Requires review |
| High | Requires immediate investigation |
| Critical | Requires immediate security response |
| Catastrophic | Requires executive escalation and mandatory human approval |

Dynamic risk changes as identity, action, data, and behavior signals change. Predictive risk uses historical patterns and leading indicators to flag actions likely to become unsafe. The Trust Score relationship is direct: risk scores are one of the primary inputs used to raise, lower, or explain an agent or product Trust Score.

## Core Components

| Component | Role |
|-----------|------|
| Signal Collector | Gathers identity, action, and behavior signals. |
| Scoring Model | Calculates risk score and tier. |
| Explanation Builder | Records score rationale. |
| Risk Store | Stores scores and historical trends. |

## Data Flow

Risk signals are collected from identity, policy, AI Shadow, application telemetry, and infrastructure. Scores are calculated, explained, stored, and passed to enforcement points.

## Azure Services Used

Azure Monitor, Log Analytics, Microsoft Sentinel, Microsoft Entra ID, Azure Storage or database services, and Azure API Management.

## Security Considerations

Risk scoring data can influence access decisions and must be protected from tampering. Score calculation must be explainable and resilient to missing signals.

## Governance Considerations

Risk tiers require defined thresholds, owners, review cadence, approval mappings, and documented business rationale.

## Monitoring and Observability

Monitor score distribution, sudden score changes, missing signals, high-risk action volume, false positives, false negatives, and approval overrides.

## Failure Scenarios

| Scenario | Response |
|----------|----------|
| Missing signal | Use conservative defaults for high-impact actions. |
| Score calculation failure | Route action to approval or deny by risk tier. |
| Score manipulation suspected | Freeze affected scores and investigate evidence. |

## Configuration Guidance

Define scoring inputs, weights, thresholds, risk tiers, approval routes, logging fields, and exception workflows.

## Design Decisions

Otic Fortress separates risk scoring from policy enforcement so policy can consume risk as one signal among several.

## Trade-offs

Dynamic scoring can be harder to explain than static rules, so each score must include rationale and contributing signals.

## Future Enhancements

Adaptive risk models, scenario simulation, confidence intervals, and customer-specific risk profiles.

## References

- [Trust Score](../governance/trust-score.md)
- [ADR-011 Risk Engine](../adr/ADR-011-Risk-Engine.md)
