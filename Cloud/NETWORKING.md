# Networking Architecture & Standards

**Owner:**Esiana Emmanuel: Cloud Infrastructure & DevOps Team  
**Version:** 1.0.0  
**Last Updated:** 2026-07-01  
**Audience:** Network Engineers, Cloud Architects, DevOps Engineers  

---

## Purpose

This document defines the networking architecture, security boundaries, and connectivity standards for the Fortress AI Cybersecurity Platform on Azure. It ensures secure, high-performance, and reliable network connectivity for all Fortress services and customer integrations.

---

## Scope

This document covers:

- Virtual Network (VNet) architecture
- Subnet design and segmentation
- Network Security Groups (NSGs)
- Azure Firewall and security policies
- Load balancing and Ingress
- DNS and Private Endpoints
- Traffic flow patterns

---

## Overview

### Why This Architecture?

Fortress handles sensitive AI workloads, customer data, and security telemetry. Networking must provide:

- **Isolation:** Separate environments (dev, staging, prod) and services
- **Security:** Zero Trust, perimeter firewall, private endpoints
- **Performance:** Low latency, high throughput
- **Resilience:** Multi-zone, multi-region design

---

## Architecture

### High-Level VNet Architecture

```mermaid
graph TB
    subgraph "Hub VNet (Central)"
        HUB_FW[Azure Firewall]
        HUB_MGMT[Management Subnet]
        HUB_BASTION[Bastion Subnet]
    end

    subgraph "Production VNet (Spoke)"
        PROD_AKS[AKS Subnet - 10.0.0.0/20]
        PROD_DB[Database Subnet - 10.0.16.0/24]
        PROD_STORAGE[Storage Subnet - 10.0.17.0/24]
        PROD_API[API Management Subnet - 10.0.18.0/24]
        PROD_PE[Private Endpoints Subnet - 10.0.19.0/24]
    end

    subgraph "Non-Production VNet (Spoke)"
        NP_AKS[AKS Subnet - 10.1.0.0/20]
        NP_DB[Database Subnet - 10.1.16.0/24]
    end

    subgraph "Management VNet (Spoke)"
        MGMT_JUMP[Jump Hosts]
        MGMT_MON[Monitoring]
    end

    HUB_FW --> PROD_AKS
    HUB_FW --> NP_AKS
    PROD_VNET[Production VNet] --> PROD_AKS
    NP_VNET[Non-Production VNet] --> NP_AKS
    HUB_VNET[Hub VNet] --> HUB_FW

    PROD_AKS --> PROD_PE
    PROD_PE --> P_KEYVAULT[Key Vault]
    PROD_PE --> P_SQL[Azure SQL]
    PROD_PE --> P_COSMOS[Cosmos DB]
Components
VNet Design
Environment	VNet Name	Address Space	Subnets
Hub	fortress-hub-vnet	10.0.0.0/16	Firewall, Management, Bastion
Production	fortress-prod-vnet	10.1.0.0/16	AKS, DB, Storage, API Mgmt, PE
Staging	fortress-staging-vnet	10.2.0.0/16	AKS, DB
QA	fortress-qa-vnet	10.3.0.0/16	AKS, DB
Development	fortress-dev-vnet	10.4.0.0/16	AKS, DB
Subnet Segmentation
Subnet Name	Address Range	Purpose
aks-subnet	10.1.0.0/20	AKS node IPs (production)
db-subnet	10.1.16.0/24	Azure SQL, Cosmos DB
storage-subnet	10.1.17.0/24	Storage accounts
api-mgmt-subnet	10.1.18.0/24	API Management
private-endpoints-subnet	10.1.19.0/24	Private Endpoints
firewall-subnet	10.0.0.0/24	Azure Firewall
mgmt-subnet	10.0.1.0/24	Management services
bastion-subnet	10.0.2.0/24	Azure Bastion
Network Security Groups (NSGs)
NSG Rules – AKS Subnet
Priority	Name	Direction	Protocol	Source	Destination	Action
1000	AllowAKSInbound	Inbound	TCP	AzureLoadBalancer	*	Allow
1001	AllowAKSOutbound	Outbound	Any	*	AzureCloud	Allow
4096	DenyAllInbound	Inbound	Any	*	*	Deny
NSG Rules – Database Subnet
Priority	Name	Direction	Protocol	Source	Destination	Action
100	AllowAKSToSQL	Inbound	TCP	10.1.0.0/20	10.1.16.0/24:1433	Allow
200	DenyAllInbound	Inbound	Any	*	*	Deny
Azure Firewall
Firewall Policy
yaml
policy_name: "fortress-firewall-policy"

application_rules:
  - name: "Allow-ACR"
    source_ip_groups: ["AKS_Pods"]
    destination_ports: ["443"]
    protocols: ["https"]
    target_fqdns: ["*.azurecr.io"]
  
  - name: "Allow-OpenAI"
    source_ip_groups: ["AKS_Pods"]
    destination_ports: ["443"]
    protocols: ["https"]
    target_fqdns: ["*.openai.azure.com"]
  
  - name: "Allow-KeyVault"
    source_ip_groups: ["AKS_Pods"]
    destination_ports: ["443"]
    protocols: ["https"]
    target_fqdns: ["*.vault.azure.net"]

network_rules:
  - name: "Allow-Egress"
    source_ip_groups: ["AKS_Subnet"]
    destination_ports: ["443", "80"]
    protocols: ["TCP"]
    destination_ip_groups: ["Internet"]
Ingress & Load Balancing
Ingress Controller
Fortress uses NGINX Ingress Controller with Azure Load Balancer:

yaml
apiVersion: v1
kind: Service
metadata:
  name: ingress-nginx-controller
  namespace: ingress-nginx
  annotations:
    service.beta.kubernetes.io/azure-load-balancer-internal: "true"
spec:
  type: LoadBalancer
  loadBalancerIP: 10.1.0.100
  ports:
  - port: 443
    targetPort: 443
DNS Configuration
Record	Type	Value	Purpose
api.fortress.ai	A	10.1.0.100	API Gateway
dashboard.fortress.ai	A	10.1.0.100	Control Plane
monitoring.fortress.ai	A	10.1.0.100	Monitoring Dashboard
Private Endpoints
All PaaS services use Private Endpoints to keep traffic within the VNet:

Service	Private Endpoint Name	Private IP
Azure SQL	pe-sql-prod	10.1.19.4
Cosmos DB	pe-cosmos-prod	10.1.19.5
Key Vault	pe-kv-prod	10.1.19.6
Storage Account	pe-storage-prod	10.1.19.7
Traffic Flow
End-to-End Request Flow
Security Considerations
No Public IPs: All production resources use Private Endpoints

Azure Firewall: All egress traffic goes through Azure Firewall

Network Policies: Kubernetes Network Policies for pod-to-pod traffic

WAF: Web Application Firewall for ingress traffic

DDoS Protection: Azure DDoS Protection for public endpoints

Monitoring
Metric	Alert Threshold
Firewall Throughput	> 80%
Load Balancer Health	> 5 failed probes
DNS Resolution	> 100ms latency
Network Latency	> 50ms (eastus)
Useful Commands
bash
# Show VNet
az network vnet show --name fortress-prod-vnet --resource-group fortress-prod-rg

# Show NSG rules
az network nsg rule list --nsg-name fortress-prod-aks-nsg

# Test connectivity
az network bastion ssh --name fortress-bastion --resource-group fortress-rg
Checklist
VNet created with appropriate address space

Subnets defined for all services

NSG rules configured correctly

Azure Firewall deployed and configured

Private Endpoints created for PaaS services

Ingress controller deployed

DNS records configured

Network Policies implemented in AKS

References
AKS.md

ZERO_TRUST.md

This document is part of the Fortress Engineering Knowledge System (EKS).

text

---
