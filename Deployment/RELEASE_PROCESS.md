# Release Process

**Owner:**Esiana Emmanuel: Cloud Infrastructure & DevOps Team  
**Version:** 1.0.0  
**Last Updated:** 2026-07-01  
**Audience:** Developers, DevOps Engineers, Engineering Managers  

---

## Purpose

This document defines the release process for the Fortress AI Cybersecurity Platform, covering Git Flow, pull requests, versioning, release tagging, and production rollout.

---

## Scope

This document covers:

- Git branching strategy
- Pull request workflow
- Semantic versioning
- Release tagging
- Release approval
- Production rollout
- Rollback process

---

## Overview

### Why a Standardised Release Process?

- **Consistency** – Everyone follows the same process
- **Quality** – Code review and testing before release
- **Traceability** – Every release is tagged and documented
- **Safety** – Approval gates prevent accidental deployments

---

## Git Flow

### Branching Model

```mermaid
graph LR
    subgraph "Main Branches"
        MAIN[main] --> PROD[Production]
        DEVELOP[develop] --> MAIN
    end

    subgraph "Feature Branches"
        FEAT1[feature/new-feature] --> DEVELOP
        FEAT2[feature/bug-fix] --> DEVELOP
    end

    subgraph "Release Branches"
        RELEASE[release/v1.2.3] --> MAIN
        RELEASE --> DEVELOP
    end

    subgraph "Hotfix Branches"
        HOTFIX[hotfix/v1.2.4] --> MAIN
        HOTFIX --> DEVELOP
    end
Branch Naming
Branch Type	Naming Convention	Example
Main	main	main
Develop	develop	develop
Feature	feature/{description}	feature/add-ai-shadow
Release	release/{version}	release/v1.2.3
Hotfix	hotfix/{version}	hotfix/v1.2.4
Pull Request Workflow
PR Requirements
Tests pass

No security vulnerabilities

At least one review

All conversations resolved

Branch up-to-date

Versioning
Semantic Versioning (SemVer)
text
MAJOR.MINOR.PATCH

v1.2.3
Version	Change
Major	Breaking changes
Minor	New features (backward compatible)
Patch	Bug fixes (backward compatible)
Version Determination
Type	Example	Version Bump
Bug Fix	Fix memory leak	Patch (1.2.3 → 1.2.4)
Feature	Add AI Shadow	Minor (1.2.3 → 1.3.0)
Breaking Change	New API contract	Major (1.2.3 → 2.0.0)
Release Tagging
Tag Naming
text
v{MAJOR}.{MINOR}.{PATCH}
Example: v1.2.3

Creating a Release Tag
bash
# Create tag
git tag -a v1.2.3 -m "Release v1.2.3"

# Push tag
git push origin v1.2.3

# Create GitHub Release
gh release create v1.2.3 \
  --title "v1.2.3" \
  --notes-file release-notes.md
Release Approval
Approval Matrix
Environment	Approver	Required
Development	None	No
QA	QA Lead	No
Staging	Engineering Manager	No
Production	Engineering Manager + VP	Yes
Production Deployment Request
markdown
# Production Deployment Request

**Release:** v1.2.3
**Date:** 2026-07-01
**Approver:** @john_doe

## Changes
- Feature: AI Shadow engine
- Bug fix: Memory leak in policy evaluation
- Performance: 20% faster event processing

## Risk Assessment
- Low risk: Features tested in staging
- Rollback time: < 5 minutes

## Testing
- Unit tests: ✅
- Integration tests: ✅
- Security scan: ✅
- Smoke tests: ✅
- Performance tests: ✅
Production Rollout
Rollout Steps
Step	Action	Time
1	Deploy to 10% (Canary)	0 min
2	Monitor for 30 minutes	30 min
3	Deploy to 50%	30 min
4	Monitor for 30 minutes	60 min
5	Deploy to 100%	60 min
6	Final health check	90 min
Production Deployment Command
bash
# Canary deployment
kubectl set image deployment/fortress-api \
  fortress-api=fortress.azurecr.io/fortress-api:v1.2.3

# Increase to 50%
kubectl patch virtualservice fortress-api \
  -p '{"spec":{"http":[{"route":[{"destination":{"host":"fortress-api","subset":"v123"},"weight":50},{"destination":{"host":"fortress-api","subset":"stable"},"weight":50}]}]}}'

# Full rollout
kubectl rollout status deployment/fortress-api
Rollback
Rollback Triggers
Trigger	Action
Error rate > 5%	Immediate rollback
Customer complaint	Immediate rollback
Performance degradation	Immediate rollback
Rollback Command
bash
# Immediate rollback
kubectl rollout undo deployment/fortress-api

# Rollback to specific version
kubectl rollout undo deployment/fortress-api --to-revision=2
Hotfix Process









Checklist
Branch naming convention followed

PR requirements met

Version determined correctly

Release tag created

Release notes written

Deployment approved

Production rollout completed

Rollback tested

References
CI_CD.md

DEPLOYMENT.md

This document is part of the Fortress Engineering Knowledge System (EKS).

text

---
