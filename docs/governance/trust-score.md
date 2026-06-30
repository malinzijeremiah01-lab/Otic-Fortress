# Trust Score

## Document Control

| Item | Value |
|------|-------|
| Project | Otic Fortress |
| Document Type | Governance Architecture |
| Version | 1.0.0 |
| Status | Draft |
| Owner | Cloud, Security & Governance Team |
| Lead | Emmanuel Opolot |

## Executive Summary

Trust Score represents confidence in an AI agent, workflow, identity, or action. It summarizes risk signals, policy history, approval outcomes, observed behavior, and compliance evidence into a governance indicator.

## Purpose

Define the Trust Score model and its role in governance decisions.

## Scope

Agent trust, workflow trust, action trust, user trust signals, risk scores, policy outcomes, approvals, and monitoring events.

## Audience

AI governance teams, security engineers, product owners, auditors, and risk stakeholders.

## Business Context

Trust must be measurable for enterprises to safely scale AI. Trust Score helps teams compare AI behavior, identify degraded confidence, and apply proportional oversight.

## Governance Overview

AI agents and Otic products receive Trust Scores based on identity assurance, policy compliance, risk history, approval outcomes, tool behavior, monitoring findings, and compliance evidence. Scores are reviewed over time so governance teams can identify trustworthy automation, degraded workflows, and products that need additional controls.

## Architecture Overview

```text
Risk Signals + Policy Outcomes + Approval History + Behavior -> Trust Score -> Governance Action
```

## Core Components

| Component | Role |
|-----------|------|
| Signal Inputs | Feed score calculation. |
| Score Model | Computes score and tier. |
| Explanation | Shows contributing factors. |
| Trend Store | Tracks score movement over time. |

## Data Flow

Signals are collected from AI Shadow, Risk Engine, Policy Engine, approvals, and monitoring. The score is calculated, explained, stored, and shown in dashboards.

## Azure Services Used

Azure Monitor, Log Analytics, Azure Storage or database services, Microsoft Sentinel, and Microsoft Entra ID.

## Security Considerations

Trust scores can affect access and approval. Score inputs and calculations must be protected from tampering and reviewed for abuse.

## Governance Considerations

Trust tiers must have clear meaning, thresholds, business actions, and review procedures.

## Monitoring and Observability

Monitor score changes, low-trust agents, score volatility, missing inputs, manual overrides, and trust recovery trends.

## Failure Scenarios

| Scenario | Response |
|----------|----------|
| Score unavailable | Use risk tier and conservative governance rules. |
| Sudden score drop | Trigger review and increase monitoring. |
| Score override requested | Require documented approval and expiry. |

## Configuration Guidance

Define score ranges, weights, minimum signal requirements, dashboard views, and governance actions per tier.

## Design Decisions

Trust Score is a governance signal, not a standalone permission grant.

## Trade-offs

Summarized scores improve usability but must remain explainable to avoid false confidence.

## Future Enhancements

Customer-specific trust models, confidence metrics, score simulation, and trust decay rules.

## References

- [Risk Engine](../security/risk-engine.md)
- [Explainability](explainability.md)
