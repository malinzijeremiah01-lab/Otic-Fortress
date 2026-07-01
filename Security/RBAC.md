# Role-Based Access Control (RBAC)

**Owner:**Esiana Emmanuel: Cloud Infrastructure & DevOps Team  
**Version:** 1.0.0  
**Last Updated:** 2026-07-01  
**Audience:** DevOps Engineers, Security Engineers, Platform Engineers  

---

## Purpose

This document defines the Role-Based Access Control (RBAC) strategy for the Fortress AI Cybersecurity Platform, covering Azure RBAC and Kubernetes RBAC.

---

## Scope

This document covers:

- Azure RBAC roles and assignments
- Kubernetes RBAC roles and bindings
- Least privilege principle
- Managed Identity integration

---

## Overview

### Why RBAC?

- **Security** – Limit access to only what is needed
- **Auditability** – Track who did what
- **Compliance** – Meet regulatory requirements
- **Operational** – Separate duties

---

## Azure RBAC Architecture

```mermaid
graph TB
    subgraph "Azure RBAC"
        AAD[Entra ID]
        SP[Service Principals]
        MI[Managed Identities]
        USER[Users]
    end

    subgraph "Roles"
        OWNER[Owner]
        CONTRIB[Contributor]
        READER[Reader]
        KEYVAULT_ADMIN[Key Vault Admin]
        KEYVAULT_USER[Key Vault User]
        ACR_PULL[ACR Pull]
        ACR_PUSH[ACR Push]
    end

    subgraph "Resources"
        RG[Resource Groups]
        AKS[AKS]
        SQL[Azure SQL]
        KV[Key Vault]
        ACR[ACR]
        STORAGE[Storage]
    end

    AAD --> USER
    SP --> CONTRIB
    MI --> ACR_PULL
    
    USER --> OWNER
    USER --> KEYVAULT_ADMIN
    SP --> CONTRIB
    
    OWNER --> RG
    CONTRIB --> AKS
    CONTRIB --> SQL
    KEYVAULT_USER --> KV
    ACR_PULL --> ACR
    READER --> STORAGE
Azure RBAC Roles
Role Definitions
Role	Permissions	Assignees
Owner	Full access	Cloud Infrastructure Team
Contributor	Create/delete resources	DevOps Team
Reader	Read only	Monitoring, Support
Key Vault Administrator	Full access to Key Vault	Security Team
Key Vault Secrets User	Read secrets	AKS, Apps
ACR Pull	Pull images	AKS
ACR Push	Push images	CI/CD
Virtual Machine Contributor	Manage VMs	DevOps
Role Assignments
bash
# Assign Contributor role
az role assignment create \
  --assignee <service-principal-id> \
  --role Contributor \
  --scope /subscriptions/xxx/resourceGroups/fortress-prod-rg

# Assign Key Vault Secrets User
az role assignment create \
  --assignee <managed-identity-id> \
  --role "Key Vault Secrets User" \
  --scope /subscriptions/xxx/resourceGroups/fortress-prod-rg/providers/Microsoft.KeyVault/vaults/fortress-prod-kv
Kubernetes RBAC
Namespaces
Namespace	Purpose
fortress-api	API Gateway
fortress-control	Control Plane
fortress-data	Data Plane
fortress-ai	AI Services
fortress-policy	Policy Engine
fortress-event	Event Processing
fortress-audit	Audit Service
Cluster Roles
yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: fortress-admin
rules:
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["*"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: fortress-viewer
rules:
- apiGroups: [""]
  resources: ["pods", "services", "configmaps"]
  verbs: ["get", "list", "watch"]
Role Bindings
yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: fortress-admin-binding
  namespace: fortress-api
subjects:
- kind: Group
  name: fortress-devops
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: fortress-admin
  apiGroup: rbac.authorization.k8s.io
Managed Identity
User-Assigned Managed Identity
bash
# Create Managed Identity
az identity create \
  --name fortress-identity \
  --resource-group fortress-prod-rg

# Assign to AKS
az aks update \
  --resource-group fortress-prod-rg \
  --name fortress-prod-aks \
  --enable-managed-identity \
  --assign-identity $(az identity show --name fortress-identity -g fortress-prod-rg --query principalId -o tsv)
Pod Identity
yaml
apiVersion: aadpodidentity.k8s.io/v1
kind: AzureIdentity
metadata:
  name: fortress-identity
spec:
  type: 0
  resourceID: /subscriptions/xxx/resourceGroups/fortress-prod-rg/providers/Microsoft.ManagedIdentity/userAssignedIdentities/fortress-identity
  clientID: xxx
---
apiVersion: aadpodidentity.k8s.io/v1
kind: AzureIdentityBinding
metadata:
  name: fortress-identity-binding
spec:
  azureIdentity: fortress-identity
  selector: fortress-identity
Least Privilege Principles
Principle	Implementation
Minimal Access	Only grant necessary permissions
Just-in-Time	Elevate only when needed
Separation of Duties	Different roles for different tasks
Regular Reviews	Quarterly access reviews
Monitoring
Metric	Alert Threshold
Failed Authentication	> 10 in 5 min
Unauthorized Access	Any occurrence
Role Assignment Change	Any change
Checklist
Azure RBAC roles assigned

Kubernetes RBAC configured

Managed Identity created and assigned

Least privilege principle applied

Access reviews scheduled

References
KEY_VAULT.md

ZERO_TRUST.md

This document is part of the Fortress Engineering Knowledge System (EKS).

text
