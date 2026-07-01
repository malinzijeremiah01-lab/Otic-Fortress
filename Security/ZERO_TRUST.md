# Zero Trust Architecture

**Owner:**Esiana Emmanuel: Cloud Infrastructure & DevOps Team  
**Version:** 1.0.0  
**Last Updated:** 2026-07-01  
**Audience:** Security Engineers, Cloud Architects, DevOps Engineers  

---

## Purpose

This document defines the Zero Trust security principles and implementation for the Fortress AI Cybersecurity Platform.

---

## Scope

This document covers:

- Zero Trust principles
- Identity verification
- Network segmentation
- Device trust
- Continuous verification

---

## Overview

### Why Zero Trust?

- **Never trust, always verify** – Don't trust any request by default
- **Assume breach** – Design for compromise
- **Least privilege** – Only grant necessary access
- **Continuous monitoring** – Always check

---

## Zero Trust Architecture

```mermaid
graph TB
    subgraph "Zero Trust Pillars"
        ID[Identity & Access]
        NET[Network]
        DEV[Devices]
        DATA[Data]
        APPS[Applications]
        INFRA[Infrastructure]
    end

    subgraph "Verification"
        AUTH[Authentication]
        AUTHZ[Authorization]
        MON[Continuous Monitoring]
    end

    subgraph "Fortress Implementation"
        AAD[Entra ID]
        RBAC[Azure RBAC]
        NSG[Network Security Groups]
        DEF[Defender for Cloud]
        KV[Key Vault]
        WAF[WAF]
    end

    ID --> AAD
    NET --> NSG
    DEV --> RBAC
    DATA --> KV
    APPS --> WAF
    INFRA --> DEF
Zero Trust Principles
1. Verify Explicitly
Always authenticate and authorise based on all available data points.

Fortress Implementation:

Multi-factor authentication (MFA)

Conditional Access policies

Risk-based authentication

2. Use Least Privilege Access
Limit access with Just-In-Time and Just-Enough-Access (JIT/JEA).

Fortress Implementation:

RBAC roles

Managed Identity

Just-In-Time access for administrators

3. Assume Breach
Design systems for inevitable compromise.

Fortress Implementation:

Network segmentation

Encryption at rest and in transit

Immutable audit logs

Identity Verification
Authentication Methods
Method	Use Case
Entra ID	User authentication
Managed Identity	Azure resource authentication
Service Principal	CI/CD authentication
MFA	All administrative access
Conditional Access Policies
json
{
  "policy_name": "Require-MFA-For-All-Users",
  "conditions": {
    "userRiskLevels": ["medium", "high"],
    "signInRiskLevels": ["medium", "high"],
    "users": {
      "includeUsers": ["all"]
    },
    "locations": {
      "includeLocations": ["all"],
      "excludeLocations": ["trusted_ip"]
    }
  },
  "grantControls": {
    "operator": "AND",
    "builtInControls": ["mfa", "passwordChange"]
  }
}
Network Segmentation
Segmentation Strategy
Segment	Purpose	Access
Management	Admin access	VPN + JIT
Internal	Service-to-service	VNet
Data	Databases	Private Endpoints
Public	External access	WAF + Application Gateway
Network Policies
yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-api-to-sql
  namespace: fortress-api
spec:
  podSelector:
    matchLabels:
      app: fortress-api
  policyTypes:
  - Egress
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: fortress-data
    ports:
    - protocol: TCP
      port: 1433
Continuous Verification
Verification Points
Point	Verification	Frequency
User Login	MFA, Risk	Every session
API Request	Token, RBAC	Every request
Service Call	Managed Identity	Every call
Data Access	Audit, Encryption	Every access
Continuous Monitoring
kql
// Detect suspicious activity
SigninLogs
| where RiskLevel == "high"
| where ResultType == "50058"  // MFA required
| project UserPrincipalName, RiskLevel, CreatedDateTime
Threat Detection
Detection Methods
Method	Example
SIEM	Microsoft Sentinel
EDR	Defender XDR
Network	NSG Flow Logs
Identity	Entra ID Sign-in Logs
Application	Application Insights
Security Controls
Control	Implementation
Authentication	Entra ID + MFA
Authorization	Azure RBAC + K8s RBAC
Encryption	TLS + Azure Encryption
Network	VNet + NSGs + Firewall
Monitoring	Azure Monitor + Sentinel
Auditing	Key Vault + Storage
Checklist
MFA enabled for all users

Conditional Access policies defined

Network segmentation implemented

Network Policies in AKS

Continuous monitoring enabled

Threat detection configured

References
RBAC.md

NETWORKING.md

This document is part of the Fortress Engineering Knowledge System (EKS).

text