# Azure Container Registry (ACR) Standards

**Owner:**Esiana Emmanuel: Cloud Infrastructure & DevOps Team  
**Version:** 1.0.0  
**Last Updated:** 2026-07-01  
**Audience:** DevOps Engineers, Platform Engineers, Developers  

---

## Purpose

This document defines the standards for using Azure Container Registry (ACR) to store, manage, and secure container images for the Fortress AI Cybersecurity Platform. It covers image lifecycle, versioning, security scanning, and integration with CI/CD and AKS.

---

## Scope

This document covers:

- ACR overview and architecture
- Image lifecycle management
- Versioning and tagging conventions
- Image security and vulnerability scanning
- Integration with GitHub Actions and AKS
- Access control and authentication

---

## Overview

### Why ACR?

ACR is Fortress's container registry of choice because:

| Requirement | ACR Capability |
|-------------|----------------|
| **Azure Integration** | Native integration with AKS, Entra ID, Azure Policy |
| **Security** | Defender integration, vulnerability scanning |
| **Geo-Replication** | Multi-region replication for fast image pulls |
| **Compliance** | Azure compliance certifications |
| **CI/CD Integration** | GitHub Actions, Azure DevOps, Docker integration |

---

## Architecture

```mermaid
graph LR
    subgraph "Image Lifecycle"
        DEV[Developer] --> BUILD[Build Image]
        BUILD --> TAG[Tag Image]
        TAG --> SCAN[Security Scan]
        SCAN --> PUSH[Push to ACR]
        PUSH --> REPLICA[Geo-Replication]
        REPLICA --> AKS1[AKS East US]
        REPLICA --> AKS2[AKS West US]
    end

    subgraph "ACR Security"
        SCAN --> DEF[Defender for Cloud]
        DEF --> ALERT[Security Alerts]
        DEF --> SBOM[SBOM Generation]
    end
Components
ACR SKU Selection
Environment	SKU	Tier	Geo-Replication
Development	Basic	10GB storage	No
QA	Standard	100GB storage	No
Staging	Premium	500GB storage	Yes
Production	Premium	Unlimited	Yes (East US + West US)
Registry Naming
text
fortress[env][region]acr[number]
Examples:

fortressdeveastusacr001 – Development

fortressprodeastusacr001 – Production (East US)

fortressprodwestusacr001 – Production (West US)

Image Lifecycle
Tagging Convention
text
{registry}/{repository}:{version}-{variant}
Tag Type	Format	Example
Semantic Version	{major}.{minor}.{patch}	fortress-api:1.2.3
Git SHA	sha-{commit}	fortress-api:sha-abc1234
Environment	{env}	fortress-api:staging
Build Number	build-{date}.{seq}	fortress-api:build-20260701.001
Retention Policy
Image Type	Retention Period	Rule
Latest	7 days	Keep only latest version
Semantic Version (prod)	Indefinite	Keep all production releases
Git SHA (dev)	14 days	Keep until cleanup
Untagged	1 day	Delete immediately
Lifecycle Policy Example
json
{
  "rules": [
    {
      "action": "delete",
      "condition": "tag == 'latest'",
      "age": 7
    },
    {
      "action": "delete",
      "condition": "tag matches 'sha-*'",
      "age": 14
    },
    {
      "action": "delete",
      "condition": "tag is empty",
      "age": 1
    }
  ]
}
Image Security
Vulnerability Scanning
ACR integrates with Microsoft Defender for Cloud to scan all images:

bash
# Enable scanning
az acr security-scan enable --name fortressprodeastusacr001

# Trigger scan on push
az acr security-scan create --image fortress-api:1.2.3

# View scan results
az acr security-scan list --name fortressprodeastusacr001
Scan Thresholds
Severity	Action
Critical	Block deployment, create security ticket
High	Block deployment, require review
Medium	Warning, review before deployment
Low	Informational, scheduled fix
Trust & Signing
Images must be signed in production:

bash
# Sign image
az acr sign --image fortress-prod:1.2.3 --key vault-key

# Verify image
az acr check-health --image fortress-prod:1.2.3
Integration with CI/CD
GitHub Actions Authentication
yaml
- name: Login to ACR
  uses: azure/docker-login@v1
  with:
    login-server: ${{ env.REGISTRY }}
    username: ${{ secrets.ACR_USERNAME }}
    password: ${{ secrets.ACR_PASSWORD }}
Managed Identity
Better than username/password:

yaml
- name: Login to ACR using Managed Identity
  run: |
    az acr login --name fortressprodeastusacr001
Best Practices
Image Optimization
Practice	Benefit
Multi-stage builds	Reduce image size by 50-70%
Slim base images	Reduce attack surface
Layer caching	Faster builds
Delete temporary files	Reduce size
Repository Organization
text
acr/
├── fortress-api/
├── fortress-control-plane/
├── fortress-data-plane/
├── fortress-ai-shadow/
├── fortress-policy-engine/
├── fortress-event-processor/
├── fortress-audit/
└── fortress-notification/
Security Considerations
Security Control	Implementation
Authentication	Managed Identity, Entra ID
Network Access	Private Endpoint, VNet injection
Data Encryption	Azure-managed keys, Customer-managed keys
Audit Logging	Azure Monitor, diagnostic settings
RBAC	Least privilege: AcrPull, AcrPush, AcrDelete
Role Assignments
Role	Permission	Purpose
AcrPull	Pull images	AKS cluster access
AcrPush	Push images	CI/CD pipeline
AcrDelete	Delete images	Cleanup automation
Monitoring
Metric	Alert Threshold
Storage Usage	> 80%
Failed Logins	> 10 in 5 min
Push Failures	> 5 in 5 min
Scan Vulnerabilities	Critical found
Troubleshooting
Issue	Solution
ImagePullBackOff	Check image name, tag, authentication
ACR login failed	Verify Managed Identity permissions
Storage full	Run retention policy, delete old images
Useful Commands
bash
# List repositories
az acr repository list --name fortressprodeastusacr001

# List tags
az acr repository show-tags --name fortressprodeastusacr001 --repository fortress-api

# Delete tag
az acr repository delete --name fortressprodeastusacr001 --image fortress-api:old

# Show vulnerabilities
az acr security-scan list --name fortressprodeastusacr001
Checklist
ACR created with correct SKU

Geo-replication enabled for production

Retention policy configured

Security scanning enabled

Managed Identity configured

RBAC roles assigned (AcrPull, AcrPush)

Private Endpoint configured

Integration with CI/CD tested

References
AKS.md

DOCKER.md

CI_CD.md

This document is part of the Fortress Engineering Knowledge System (EKS).

text

---
