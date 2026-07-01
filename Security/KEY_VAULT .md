# Azure Key Vault Standards

**Owner:**Esiana Emmanuel:Cloud Infrastructure & DevOps Team  
**Version:** 1.0.0  
**Last Updated:** 2026-07-01  
**Audience:** DevOps Engineers, Security Engineers, Developers  

---

## Purpose

This document defines the standards for using Azure Key Vault to securely store and manage secrets, certificates, and keys for the Fortress AI Cybersecurity Platform.

---

## Scope

This document covers:

- Key Vault architecture and configuration
- Secrets management
- Certificate management
- Key rotation
- Access policies and Managed Identity

---

## Overview

### Why Key Vault?

Key Vault provides:

- **Centralised secrets management** – Single source of truth
- **Security** – Hardware-backed security
- **Auditability** – All access is logged
- **Integration** – Native with Azure services

---

## Architecture

```mermaid
graph TB
    subgraph "Key Vault"
        KV[Key Vault]
        SECRETS[Secrets]
        KEYS[Keys]
        CERTS[Certificates]
    end

    subgraph "Access Methods"
        MI[Managed Identity]
        SP[Service Principal]
        USER[User Identity]
    end

    subgraph "Consumers"
        AKS[AKS Pods]
        APP[Applications]
        CI[CI/CD Pipelines]
        ADMIN[Administrators]
    end

    MI --> KV
    SP --> KV
    USER --> KV
    
    KV --> SECRETS
    KV --> KEYS
    KV --> CERTS
    
    AKS --> MI
    APP --> MI
    CI --> SP
    ADMIN --> USER
Key Vault Configuration
Naming Convention
text
{project}-{environment}-{region}-kv-{number}
Example: fortress-prod-eastus-kv-001

SKU Selection
Environment	SKU	Soft Delete	Purge Protection
Development	Standard	7 days	Disabled
QA	Standard	7 days	Disabled
Staging	Standard	90 days	Enabled
Production	Premium	90 days	Enabled
Creating Key Vault
bash
az keyvault create \
  --name fortress-prod-eastus-kv-001 \
  --resource-group fortress-prod-rg \
  --location eastus \
  --sku premium \
  --enable-soft-delete true \
  --soft-delete-retention 90 \
  --enable-purge-protection true
Secrets Management
Secret Naming Convention
text
{service}-{secret-type}-{description}
Examples:

sql-connection-string

api-gateway-jwt-key

ai-engine-openai-key

event-hub-connection-string

Storing Secrets
bash
# Store secret
az keyvault secret set \
  --vault-name fortress-prod-eastus-kv-001 \
  --name sql-connection-string \
  --value "Server=tcp:...;Database=fortress;User Id=fortress;Password=..."

# Store from file
az keyvault secret set \
  --vault-name fortress-prod-eastus-kv-001 \
  --name jwt-private-key \
  --file ./jwt-private-key.pem
Accessing Secrets
python
# Python using Managed Identity
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
client = SecretClient(
    vault_url="https://fortress-prod-eastus-kv-001.vault.azure.net/",
    credential=credential
)

secret = client.get_secret("sql-connection-string")
Kubernetes Integration
yaml
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: fortress-kv-secrets
  namespace: fortress-api
spec:
  provider: azure
  parameters:
    usePodIdentity: "false"
    useVMManagedIdentity: "true"
    userAssignedIdentityID: "xxx"
    keyvaultName: "fortress-prod-eastus-kv-001"
    objects: |
      array:
        - |
          objectName: sql-connection-string
          objectType: secret
        - |
          objectName: jwt-key
          objectType: secret
Certificate Management
Storing Certificates
bash
# Import certificate
az keyvault certificate import \
  --vault-name fortress-prod-eastus-kv-001 \
  --name fortress-tls-cert \
  --file ./fortress-prod-tls.pfx \
  --password ""

# Create self-signed certificate
az keyvault certificate create \
  --vault-name fortress-prod-eastus-kv-001 \
  --name fortress-tls-cert \
  --policy @policy.json
Certificate Policy
json
{
  "issuerParameters": {
    "name": "Self"
  },
  "keyProperties": {
    "keySize": 2048
  },
  "lifetimeActions": [
    {
      "action": {
        "actionType": "AutoRenew"
      },
      "trigger": {
        "daysBeforeExpiry": 30
      }
    }
  ]
}
Key Rotation
Rotation Policy
Secret Type	Rotation Frequency	Method
Database Password	90 days	Manual or automated
API Keys	180 days	Manual
JWT Signing Key	365 days	Manual
TLS Certificates	365 days	Automated
Automated Rotation Script
powershell
# Rotate SQL password
$newPassword = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | % {[char]$_})

# Update SQL server
Set-AzSqlServer -ResourceGroupName "fortress-prod-rg" `
  -ServerName "fortress-prod-sql" `
  -AdministratorLoginPassword $newPassword

# Update Key Vault
$secret = ConvertTo-SecureString -String $newPassword -AsPlainText -Force
Set-AzKeyVaultSecret -VaultName "fortress-prod-kv" `
  -Name "sql-password" `
  -SecretValue $secret

# Restart services
kubectl rollout restart deployment/fortress-api -n fortress-api
Access Policies
Role Assignments
Role	Scope	Purpose
Key Vault Administrator	Management	Full access (limited users)
Key Vault Secrets User	AKS, Apps	Read secrets
Key Vault Secrets Officer	CI/CD	Create/update secrets
Assigning Access
bash
# Assign Managed Identity access
az keyvault set-policy \
  --name fortress-prod-eastus-kv-001 \
  --object-id <managed-identity-object-id> \
  --secret-permissions get list

# Assign Service Principal access
az keyvault set-policy \
  --name fortress-prod-eastus-kv-001 \
  --spn <service-principal-id> \
  --secret-permissions get list set delete
Monitoring
Metric	Alert Threshold
Secret Access	> 1000/hour
Throttling	> 100 operations
Failed Access	> 10 in 5 min
Certificate Expiry	< 30 days
Monitoring Query
kql
AzureDiagnostics
| where ResourceProvider == "MICROSOFT.KEYVAULT"
| where OperationName == "SecretGet"
| summarize Count = count() by bin(TimeGenerated, 1h)
Troubleshooting
Issue	Solution
Access denied	Check Managed Identity assignment
Secret not found	Verify name and vault
Certificate expired	Check rotation policy
Checklist
Key Vault created with correct SKU

Soft delete enabled

Purge protection enabled (production)

Managed Identity configured

Access policies assigned

Secret rotation policy defined

Certificate expiration monitoring configured

References
SECRETS.md

RBAC.md

This document is part of the Fortress Engineering Knowledge System (EKS).

text

---