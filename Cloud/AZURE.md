# Azure Cloud Architecture & Standards

**Owner:** Esiana Emmanuel: Cloud Infrastructure & DevOps Team  
**Version:** 1.0.0  
**Last Updated:** 2026-07-01  
**Audience:** Cloud Architects, DevOps Engineers, Platform Engineers  

---

## Purpose

This document defines the Azure cloud architecture, resource organisation, naming conventions, tagging strategy, and cost optimisation practices for the Fortress AI Cybersecurity Platform. It ensures that all Azure resources are provisioned, managed, and governed consistently across all environments.

---

## Scope

This document covers:

- Azure subscription and resource group structure
- Region selection and multi-region strategy
- Identity and access management foundation
- Networking and security boundaries
- Resource naming conventions
- Tagging strategy for cost and operational management
- Cost optimisation techniques

This applies to **all** Fortress environments: Development, QA, Staging, and Production.

---

## Overview

### Why Azure for Fortress?

Fortress is built on Microsoft Azure for the following reasons:

| Requirement | Azure Capability |
|-------------|-------------------|
| **AI Workloads** | Azure OpenAI, AI Foundry, Machine Learning |
| **Container Orchestration** | Azure Kubernetes Service (AKS) |
| **Security & Compliance** | Microsoft Defender, Sentinel, Purview, Zero Trust architecture |
| **Global Scale** | 60+ regions, global CDN, geo-redundant storage |
| **Hybrid Integration** | Azure Arc, on-premises connectivity options |
| **Enterprise Governance** | Azure Policy, Blueprints, Management Groups |

---

## Architecture

### High-Level Azure Architecture

```mermaid
graph TB
    subgraph "Azure Management"
        MG[Management Groups]
        SUB[Subscriptions]
        RG[Resource Groups]
    end

    subgraph "Identity & Security"
        AAD[Microsoft Entra ID]
        KV[Key Vault]
        DEF[Microsoft Defender for Cloud]
    end

    subgraph "Networking"
        VNET[Virtual Network]
        SUBNET[Subnets]
        NSG[Network Security Groups]
        FW[Azure Firewall]
        LB[Load Balancer]
    end

    subgraph "Compute"
        AKS[Azure Kubernetes Service]
        AC[App Configuration]
        FUNC[Azure Functions]
    end

    subgraph "Data & Storage"
        SQL[Azure SQL Database]
        COSMOS[Azure Cosmos DB]
        STORAGE[Blob Storage]
        DATALAKE[Data Lake Storage]
    end

    subgraph "AI Services"
        OPENAI[Azure OpenAI]
        AIFOUNDRY[AI Foundry]
        MLS[Machine Learning]
    end

    subgraph "Monitoring & Observability"
        MON[Azure Monitor]
        INSIGHTS[Application Insights]
        LOG[Log Analytics Workspace]
        ALERTS[Alert Rules]
    end

    subgraph "Eventing & Integration"
        EH[Event Hubs]
        SB[Service Bus]
        EG[Event Grid]
        API[API Management]
    end

    MG --> SUB
    SUB --> RG
    RG --> AKS
    RG --> SQL
    RG --> STORAGE
    RG --> KV
    RG --> VNET
    VNET --> SUBNET
    SUBNET --> NSG
    AAD --> KV
    AAD --> AKS
    AKS --> MON
    AKS --> EH
    AKS --> SB
    OPENAI --> AIFOUNDRY
    MLS --> AIFOUNDRY