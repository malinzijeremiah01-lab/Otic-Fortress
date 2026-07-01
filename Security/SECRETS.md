# Secrets Management

**Owner:**Esiana Emmanuel: Cloud Infrastructure & DevOps Team  
**Version:** 1.0.0  
**Last Updated:** 2026-07-01  
**Audience:** Developers, DevOps Engineers, Security Engineers  

---

## Purpose

This document defines the standards for managing secrets (passwords, API keys, certificates) across the Fortress AI Cybersecurity Platform.

---

## Scope

This document covers:

- Secrets management principles
- Environment variables
- Secret rotation
- Best practices
- Do's and Don'ts

---

## Overview

### Why Secrets Management?

- **Security** – Prevent credential exposure
- **Compliance** – Audit trails for secret access
- **Consistency** – Centralised secrets store
- **Rotation** – Automated secret rotation

---

## Secrets Management Architecture

```mermaid
graph TB
    subgraph "Secret Sources"
        USER[User Input]
        CI[CI/CD Pipeline]
        ADMIN[Administrator]
    end

    subgraph "Secret Store"
        KV[Azure Key Vault]
        SECRETS[Encrypted Secrets]
    end

    subgraph "Secret Consumers"
        AKS[AKS Pods]
        APP[Applications]
        CI_CD[CI/CD Pipelines]
        DEV[Developers]
    end

    USER --> KV
    CI --> KV
    ADMIN --> KV
    
    KV --> SECRETS
    
    AKS -->|CSI Driver| KV
    APP -->|SDK| KV
    CI_CD -->|Managed Identity| KV
    DEV -->|Azure CLI| KV
    Environment Variables
Use Environment Variables, Not Hardcoded Secrets
python
# ❌ BAD – Hardcoded secret
API_KEY = "abc123def456"

# ✅ GOOD – Environment variable
import os
API_KEY = os.environ.get("API_KEY")
Kubernetes Integration
yaml
apiVersion: v1
kind: Pod
metadata:
  name: fortress-api
spec:
  containers:
  - name: api
    env:
    - name: API_KEY
      valueFrom:
        secretKeyRef:
          name: fortress-secrets
          key: api-key
Secret Rotation
Rotation Policy
Secret Type	Frequency	Method
Database Passwords	90 days	Automated
API Keys	180 days	Manual
JWT Signing Keys	365 days	Manual
Certificates	365 days	Automated
Automated Rotation Script
python
import azure.identity
import azure.keyvault.secrets

def rotate_secret(secret_name, new_value):
    credential = azure.identity.DefaultAzureCredential()
    client = azure.keyvault.secrets.SecretClient(
        vault_url="https://fortress-kv.vault.azure.net/",
        credential=credential
    )
    client.set_secret(secret_name, new_value)
Best Practices
DOs
✅ Store secrets in Azure Key Vault

✅ Use Managed Identity for authentication

✅ Rotate secrets regularly

✅ Use different secrets per environment

✅ Encrypt secrets at rest and in transit

✅ Audit secret access

✅ Use least privilege permissions

DON'Ts
❌ Hardcode secrets in code

❌ Store secrets in environment variables (unencrypted)

❌ Share secrets via email or chat

❌ Use the same secret across environments

❌ Commit secrets to Git

Secret Scanning
GitHub Secret Scanning
yaml
# Enable secret scanning in GitHub repo
# Settings > Security > Secret scanning
Pre-commit Hooks
bash
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.16.0
    hooks:
      - id: gitleaks
Monitoring
Metric	Alert Threshold
Failed Secret Access	> 10 in 5 min
Secret Expiration	< 7 days
Large Number of Secrets	> 100 per service
Troubleshooting
Issue	Solution
Secret not found	Check name and environment
Access denied	Check Managed Identity permissions
Secret rotation failed	Check connectivity to Key Vault
Checklist
Secrets stored in Key Vault

Managed Identity configured

Secret rotation policy defined

Secret scanning enabled

Pre-commit hooks configured

