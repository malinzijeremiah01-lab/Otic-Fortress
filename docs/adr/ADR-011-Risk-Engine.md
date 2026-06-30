# ADR-011: Risk Engine

## Status

Accepted

## Context

Otic Fortress needs proportional controls for identities, agents, tools, data access, and high-impact AI actions.

## Problem

Static permissions cannot represent changing risk from behavior, data sensitivity, tool capability, and operating context.

## Decision

Use a dedicated Risk Engine to calculate dynamic risk scores and tiers.

## Alternatives Considered

- Static risk labels only.
- Policy rules without separate risk scoring.
- Manual risk review for every AI action.

## Rationale

Dedicated scoring lets policy and approval workflows consume explainable risk without embedding scoring logic everywhere.

## Consequences

Risk signals, scoring output, and explanations must be logged and protected.

## Trade-offs

Dynamic scoring requires explanation and tuning, but it enables proportional governance.

## Related Documents

- [Risk Engine Security Architecture](../security/risk-engine.md)
- [Trust Score](../governance/trust-score.md)

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

Otic Fortress will use a dedicated Risk Engine to calculate dynamic risk for AI actions, identities, workloads, tools, data access, and operating context.

## Purpose

Record the decision to separate risk scoring from policy enforcement while allowing policy to consume risk signals.

## Scope

Risk inputs, scoring models, risk tiers, trust score inputs, approval thresholds, monitoring signals, and evidence.

## Audience

Security engineers, risk owners, AI governance teams, platform engineers, compliance teams, and auditors.

## Business Context

AI actions vary in impact. Dynamic risk scoring allows Otic Fortress to apply proportional controls rather than treating every action the same.

## Architecture Overview

```text
Signals -> Risk Model -> Score + Tier -> Policy / Approval / Monitoring -> Evidence
```

## Core Components

| Component | Decision Role |
|-----------|---------------|
| Signal Collector | Gathers risk inputs. |
| Scoring Runtime | Calculates scores. |
| Explanation Builder | Records score rationale. |
| Risk Store | Stores score history. |

## Data Flow

Signals are collected from identity, AI Shadow, policy decisions, data classification, and monitoring. The Risk Engine computes a score and tier that are used by enforcement and dashboards.

## Azure Services Used

Azure Monitor, Log Analytics, Microsoft Sentinel, Microsoft Entra ID, Azure Storage or database services, and Azure API Management.

## Security Considerations

Risk inputs and outputs must be protected because they influence approval and enforcement decisions.

## Governance Considerations

Risk tiers require definitions, owners, thresholds, review cadence, and documented actions.

## Monitoring and Observability

Monitor high-risk actions, score drift, missing inputs, scoring failures, overrides, and false positive rates.

## Failure Scenarios

| Scenario | Response |
|----------|----------|
| Scoring unavailable | Use conservative risk tier for high-impact actions. |
| Score anomaly | Trigger review and preserve evidence. |

## Configuration Guidance

Define input signals, weights, thresholds, score ranges, approval mappings, and logging requirements.

## Design Decisions

Otic Fortress separates risk calculation from policy enforcement so each capability can evolve independently.

## Trade-offs

Dynamic scoring requires explanation and tuning, but it enables proportional governance.

## Future Enhancements

Adaptive scoring, customer-specific risk profiles, model validation, and score simulation.

## References

- [Risk Engine Security Architecture](../security/risk-engine.md)
- [Trust Score](../governance/trust-score.md)
