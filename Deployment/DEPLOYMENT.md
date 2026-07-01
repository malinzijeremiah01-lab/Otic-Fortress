# Deployment Strategy

**Owner:**Esiana Emmanuel: Cloud Infrastructure & DevOps Team  
**Version:** 1.0.0  
**Last Updated:** 2026-07-01  
**Audience:** DevOps Engineers, Developers, Platform Engineers  

---

## Purpose

This document defines the deployment strategies for the Fortress AI Cybersecurity Platform, covering the different deployment models (Blue-Green, Rolling, Canary) and environment-specific approaches.

---

## Scope

This document covers:

- Deployment strategies (Blue-Green, Rolling, Canary)
- Environment-specific deployment approaches
- Rollback procedures
- Deployment gates and approvals

---

## Overview

### Why Multiple Deployment Strategies?

Different Fortress services have different risk profiles:

- **Critical services** (API Gateway, Control Plane) require zero-downtime, low-risk deployments
- **AI services** require careful monitoring for regression
- **Internal services** can accept more risk for faster iteration

---

## Deployment Strategies

### Blue-Green Deployment

**Used for:** API Gateway, Control Plane, Audit Service

```mermaid
graph LR
    subgraph "Blue (Current)"
        BLUE[API Gateway v1]
    end
    
    subgraph "Green (New)"
        GREEN[API Gateway v2]
    end
    
    LB[Load Balancer] --> BLUE
    LB -.->|Switch| GREEN
    GREEN -->|Validate| TEST[Smoke Tests]
    TEST -->|Pass| SWITCH[Switch Traffic]
    BLUE -->|Standby| ROLLBACK[Rollback if needed]
Pros: Zero downtime, instant rollback
Cons: Doubles resource usage during deployment

Rolling Update
Used for: AI Shadow Engine, Event Processor, Notification Service

yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
Pros: Gradual, resource-efficient
Cons: Longer deployment time, partial failure possible

Canary Deployment
Used for: AI Inference Service, Policy Engine












Pros: Low risk, gradual exposure
Cons: Complex monitoring, longer rollout

Environment-Specific Strategies
Environment	Strategy	Approval Required	Auto-Deploy
Development	Rolling Update	No	Yes
QA	Rolling Update	No	Yes
Staging	Blue-Green	No	Yes
Production	Canary (10%→50%→100%)	Yes	No
Deployment Workflow
Rollback Procedures
Rollback Triggers
Trigger	Timeframe	Action
High error rate	Immediate	Rollback
Deployment failure	Immediate	Rollback
Customer complaint	< 30 min	Rollback
Performance degradation	< 1 hour	Rollback
Rollback Commands
bash
# Blue-Green: Switch back to blue
kubectl patch service fortress-api -n fortress-api -p '{"spec":{"selector":{"version":"blue"}}}'

# Rolling Update: Revert to previous image
kubectl set image deployment/fortress-api fortress-api=fortress.azurecr.io/fortress-api:1.2.2

# Canary: Reduce canary traffic to 0%
kubectl patch virtualservice fortress-api -n fortress-api -p '{"spec":{"http":[{"route":[{"destination":{"host":"fortress-api","subset":"stable"},"weight":100}]}]}}'
Deployment Gates
Gate	Description	Owner
Build Passes	All tests pass	CI
Security Scan	No critical vulnerabilities	Security
Performance Test	No regression	QA
Manual Approval	For production	Approver
Health Check	All pods healthy	CI
Smoke Test	Critical flows work	CI
Troubleshooting
Issue	Solution
Deployment stuck	Check pod status, resources
Rollback failed	Force apply previous manifest
Approval not triggered	Check approval configuration
Checklist
Deployment strategy defined per service

Rollback procedures documented

Approval gates configured

Canary configuration tested

Blue-Green testing complete

References
CI_CD.md

ENVIRONMENTS.md

This document is part of the Fortress Engineering Knowledge System (EKS).

text

---
