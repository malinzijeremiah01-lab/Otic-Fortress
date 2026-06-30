# Threat Detection Architecture

## Document Control

| Item | Value |
|------|-------|
| Project | Otic Fortress |
| Document Type | Security Detection Architecture |
| Version | 1.0.0 |
| Status | Draft |
| Owner | Cloud, Security & Governance Team |
| Lead | Emmanuel Opolot |

## Executive Summary

Threat detection for Otic Fortress correlates identity, cloud, application, API, AI Shadow, policy, risk, and compliance signals to identify malicious activity, unsafe AI behavior, and operational abuse.

## Purpose

Define the detection strategy and signal model for Otic Fortress.

## Scope

Authentication events, authorization failures, AI tool calls, policy decisions, risk scores, administrative actions, cloud posture alerts, network events, and data access logs.

## Audience

SOC analysts, security engineers, cloud engineers, platform engineers, incident responders, and auditors.

## Business Context

Otic Fortress must detect threats against both traditional cloud workloads and AI governance workflows. Detection must include attacks on prompts, tools, policies, approvals, and evidence.

## Architecture Overview

```text
Signals -> Log Analytics -> Sentinel Analytics -> Alert -> Triage -> Incident Response
   |             |                 |             |
   v             v                 v             v
AI Shadow    Cloud Logs       Correlation     Evidence Pack
```

## Core Components

| Component | Role |
|-----------|------|
| Signal Sources | Emit security telemetry. |
| Log Analytics | Central log workspace. |
| Sentinel | Correlation, alerting, and investigation. |
| Detection Rules | Encoded suspicious behavior patterns. |

## Data Flow

Events are collected from platform components, normalized in logging workspaces, correlated through analytics rules, enriched with context, and routed to incident response workflows.

## Azure Services Used

Microsoft Sentinel, Azure Monitor, Log Analytics, Microsoft Defender for Cloud, Microsoft Entra ID, Azure API Management, and Azure Storage.

## Security Considerations

Detection coverage must include privileged access, policy tampering, suspicious AI prompts, denied tool calls, data exfiltration patterns, and monitoring pipeline failures.

## Threat Coverage

| Threat Area | Detection Focus |
|-------------|-----------------|
| AI threats | Prompt attacks, rogue agents, unsafe tool use, model abuse, and Shadow AI. |
| Cloud threats | Misconfigured resources, exposed services, vulnerable workloads, and suspicious Azure activity. |
| Identity threats | Risky sign-ins, privilege escalation, impossible travel, and token misuse. |
| API threats | Abuse, credential stuffing, malformed payloads, rate anomalies, and unauthorized access. |
| Insider threats | Unusual administrative actions, data access spikes, and policy bypass attempts. |
| Data leakage | Sensitive data movement, suspicious exports, and unauthorized document access. |

Microsoft Sentinel integration provides correlation, incident creation, hunting, and response workflows. Microsoft Defender integration contributes cloud posture, workload protection, and vulnerability signals.

## Governance Considerations

Detection rules require owners, severity definitions, tuning history, evidence requirements, and response playbooks.

## Monitoring and Observability

Track alert volume, false positives, rule health, ingestion latency, coverage gaps, time to detect, and time to triage.

## Failure Scenarios

| Scenario | Response |
|----------|----------|
| Log ingestion delayed | Alert on pipeline health and preserve source logs. |
| Detection rule noisy | Tune rule and document rationale. |
| Critical alert missed | Conduct post-incident detection review. |

## Configuration Guidance

Enable diagnostic settings, define Sentinel analytics rules, configure watchlists, tag critical assets, and map alerts to incident playbooks.

## Design Decisions

Otic Fortress treats AI governance events as first-class detection signals, not only application logs.

## Trade-offs

Broad telemetry improves detection but increases cost and requires careful retention management.

## Future Enhancements

AI-specific detection packs, behavior analytics, threat hunting notebooks, and automated enrichment.

## References

- [Security Monitoring](security-monitoring.md)
- [Incident Response](incident-response.md)
