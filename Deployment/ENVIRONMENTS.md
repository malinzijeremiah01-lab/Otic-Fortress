# Environment Configuration

**Owner:**Esiana Emmanuel: Cloud Infrastructure & DevOps Team  
**Version:** 1.0.0  
**Last Updated:** 2026-07-01  
**Audience:** Developers, DevOps Engineers, QA  

---

## Purpose

This document defines the environment configurations for the Fortress AI Cybersecurity Platform, covering Development, QA, Staging, and Production environments.

---

## Scope

This document covers:

- Environment definitions
- Configuration management
- Environment variables
- Environment-specific resource sizing

---

## Overview

### Why Environment Separation?

- **Development:** Fast iteration, experimental features
- **QA:** Validation before production
- **Staging:** Production-like testing
- **Production:** Live customer traffic

---

## Environments

### Development

| Attribute | Value |
|-----------|-------|
| **Purpose** | Developer testing |
| **Azure Subscription** | Non-Production |
| **Resource Group** | `fortress-dev-rg` |
| **Region** | East US |
| **AKS Tier** | Standard |
| **Node Size** | Standard_D2s_v3 |
| **Min Nodes** | 2 |
| **Max Nodes** | 5 |
| **Database Tier** | Basic (5 DTU) |
| **Cosmos Throughput** | 400 RU/s |
| **Auto-Deploy** | Yes |
| **Approval Required** | No |

### QA

| Attribute | Value |
|-----------|-------|
| **Purpose** | Quality assurance testing |
| **Azure Subscription** | Non-Production |
| **Resource Group** | `fortress-qa-rg` |
| **Region** | East US |
| **AKS Tier** | Standard |
| **Node Size** | Standard_D4s_v3 |
| **Min Nodes** | 2 |
| **Max Nodes** | 5 |
| **Database Tier** | Standard S0 (10 DTU) |
| **Cosmos Throughput** | 1000 RU/s |
| **Auto-Deploy** | Yes |
| **Approval Required** | No |

### Staging

| Attribute | Value |
|-----------|-------|
| **Purpose** | Pre-production validation |
| **Azure Subscription** | Non-Production |
| **Resource Group** | `fortress-staging-rg` |
| **Region** | East US |
| **AKS Tier** | Standard |
| **Node Size** | Standard_D4s_v3 |
| **Min Nodes** | 3 |
| **Max Nodes** | 10 |
| **Database Tier** | Standard S2 (50 DTU) |
| **Cosmos Throughput** | 2000 RU/s |
| **Auto-Deploy** | Yes |
| **Approval Required** | No |

### Production

| Attribute | Value |
|-----------|-------|
| **Purpose** | Live customer traffic |
| **Azure Subscription** | Production |
| **Resource Group** | `fortress-prod-rg` |
| **Region** | East US, West US (DR) |
| **AKS Tier** | Premium |
| **Node Size** | Standard_D8s_v3 |
| **Min Nodes** | 3 |
| **Max Nodes** | 20 |
| **Database Tier** | Premium P2 (250 DTU) |
| **Cosmos Throughput** | 4000 RU/s (autoscale) |
| **Auto-Deploy** | No |
| **Approval Required** | Yes |

---

## Configuration Management

### Environment Variables Pattern

```yaml
# Development
APP_ENV=development
LOG_LEVEL=DEBUG
DATABASE_URL=postgresql://dev:dev@localhost:5432/fortress
AZURE_OPENAI_ENDPOINT=https://openai-dev.openai.azure.com/

# Production
APP_ENV=production
LOG_LEVEL=INFO
DATABASE_URL=postgresql://fortress:${DB_PASSWORD}@fortress-prod-sql:5432/fortress
AZURE_OPENAI_ENDPOINT=https://openai-prod.openai.azure.com/
Kubernetes ConfigMap Example
yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fortress-api-config
  namespace: fortress-api
data:
  environment: production
  logLevel: info
  apiTimeout: "30"
Kubernetes Secret Example
yaml
apiVersion: v1
kind: Secret
metadata:
  name: fortress-api-secrets
  namespace: fortress-api
type: Opaque
data:
  db-password: <base64-encoded-password>
  api-key: <base64-encoded-api-key>
Environment Variables
Common Variables
Variable	Purpose
APP_ENV	Application environment
LOG_LEVEL	Log verbosity
DATABASE_URL	Database connection
REDIS_URL	Redis connection
AZURE_OPENAI_ENDPOINT	OpenAI endpoint
AZURE_OPENAI_KEY	OpenAI API key
STORAGE_CONNECTION	Azure Storage connection
KEY_VAULT_URI	Key Vault URI
Resource Sizing
Service	Dev	QA	Staging	Production
API Gateway	1 replica / 500m CPU / 1GB	2 / 1CPU / 2GB	2 / 1CPU / 2GB	3 / 2CPU / 4GB
Control Plane	1 / 500m / 1GB	2 / 1CPU / 2GB	2 / 1CPU / 2GB	3 / 2CPU / 4GB
AI Shadow	1 / 1CPU / 2GB	1 / 2CPU / 4GB	2 / 4CPU / 8GB	2 / 8CPU / 16GB
Event Processor	1 / 500m / 1GB	2 / 1CPU / 2GB	2 / 1CPU / 2GB	2 / 2CPU / 4GB
Monitoring
Metric	Dev/QA	Staging	Production
CPU Alert	85%	80%	75%
Memory Alert	85%	80%	75%
Checklist
Environments defined with appropriate sizing

Environment variables configured

Secrets stored in Key Vault

ConfigMaps created for each service

Monitoring thresholds set per environment

References
DEPLOYMENT.md

CI_CD.md

This document is part of the Fortress Engineering Knowledge System (EKS).

text