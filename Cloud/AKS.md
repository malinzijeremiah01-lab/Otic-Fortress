# Azure Kubernetes Service (AKS) Standards

**Owner:**Esiana Emmanuel: Cloud Infrastructure & DevOps Team  
**Version:** 1.0.0  
**Last Updated:** 2026-07-01  
**Audience:** Platform Engineers, DevOps Engineers, Developers  

---

## Purpose

This document defines the architecture, configuration, and operational standards for Azure Kubernetes Service (AKS) clusters powering the Fortress AI Cybersecurity Platform. It ensures that all Kubernetes deployments are secure, scalable, reliable, and follow industry best practices.

---

## Scope

This document covers:

- AKS cluster architecture and design
- Node pools and sizing
- Workload deployment patterns (Deployments, StatefulSets, DaemonSets)
- Services, Ingress, and networking
- Configuration management (ConfigMaps, Secrets)
- Autoscaling (HPA, VPA, Cluster Autoscaler)
- Rolling updates and canary deployments
- Security and RBAC
- Monitoring and logging
- Production best practices

---

## Overview

### Why AKS for Fortress?

AKS is the container orchestration platform for all Fortress microservices:

| Requirement | AKS Capability |
|-------------|----------------|
| **Microservices Architecture** | Native support for containerised workloads |
| **AI Workloads** | GPU node pools for AI inference |
| **Scalability** | Horizontal Pod Autoscaler, Cluster Autoscaler |
| **High Availability** | Multi-zone cluster, rolling updates, pod disruption budgets |
| **Security** | Azure AD integration, RBAC, pod identity, network policies |
| **Cost Optimisation** | Node autoscaling, spot instances for non-production |
| **Observability** | Azure Monitor, Application Insights, Container Insights |

---

## Architecture

### AKS Cluster Architecture

```mermaid
graph TB
    subgraph "AKS Cluster"
        subgraph "System Node Pool"
            SYS_NODES[System Nodes]
            DNS[CoreDNS]
            CSI[CSI Drivers]
            METRICS[Metrics Server]
            TUNNEL[Tunnel Pod]
        end

        subgraph "User Node Pool"
            USER_NODES[User Nodes]
            subgraph "Fortress Workloads"
                API[API Gateway Pods]
                CONTROL[Control Plane Pods]
                DATA[Data Plane Pods]
                AI[AI Shadow Engine Pods]
                POLICY[Policy Engine Pods]
                EVENT[Event Processor Pods]
                AUDIT[Audit Service Pods]
                NOTIFY[Notification Service Pods]
            end
        end

        subgraph "Ingress Layer"
            INGRESS[Ingress Controller]
            NLB[Network Load Balancer]
            WAF[WAF Policy]
        end
    end

    subgraph "Azure Services"
        ACR[Azure Container Registry]
        KV[Key Vault]
        SQL[Azure SQL]
        COSMOS[Cosmos DB]
        EH[Event Hubs]
    end

    subgraph "Monitoring"
        MON[Azure Monitor]
        INS[Application Insights]
        LOG[Log Analytics]
    end

    API --> INGRESS
    CONTROL --> SQL
    CONTROL --> KV
    DATA --> COSMOS
    EVENT --> EH
    AI --> OPENAI[Azure OpenAI]
    ALL_PODS --> MON
    ALL_PODS --> INS
    ACR --> API
    ACR --> CONTROL
Components
Node Pools
AKS clusters use two node pools:

System Node Pool
Configuration	Value
Name	systempool
VM Size	Standard_D4s_v3 (4 vCPU, 16GB RAM)
Node Count	2 (min) / 5 (max)
Taint	CriticalAddonsOnly=true:NoSchedule
Purpose	Cluster system components (CoreDNS, CSI, Metrics Server)
User Node Pool
Configuration	Value
Name	userpool
VM Size	Standard_D8s_v3 (8 vCPU, 32GB RAM)
Node Count	3 (min) / 20 (max)
Purpose	All Fortress microservices
GPU Node Pool (for AI Workloads)
Configuration	Value
Name	gpupool
VM Size	Standard_NC6s_v3 (6 vCPU, 112GB RAM, NVIDIA Tesla V100)
Node Count	0 (min) / 5 (max)
Purpose	AI inference, AI Shadow processing
Workload Types
Workload	Deployment Type	Replicas (Prod)	Resource Requests
API Gateway	Deployment	3	1 CPU / 2GB
Control Plane	Deployment	3	1 CPU / 2GB
Data Plane	Deployment	3	2 CPU / 4GB
AI Shadow Engine	Deployment	2	4 CPU / 8GB (GPU optional)
Policy Engine	Deployment	2	1 CPU / 2GB
Event Processor	Deployment	2	2 CPU / 4GB
Audit Service	Deployment	2	1 CPU / 2GB
Notification Service	Deployment	2	0.5 CPU / 1GB
Workflow
Fortress Deployment Workflow
Standards
Deployment YAML Example
yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fortress-api-gateway
  namespace: fortress-api
  labels:
    app: fortress-api-gateway
    environment: production
    version: 1.2.3
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: fortress-api-gateway
  template:
    metadata:
      labels:
        app: fortress-api-gateway
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
    spec:
      containers:
      - name: api-gateway
        image: fortress.azurecr.io/fortress-api:1.2.3
        imagePullPolicy: Always
        ports:
        - containerPort: 8080
        resources:
          requests:
            cpu: "1000m"
            memory: "2Gi"
          limits:
            cpu: "2000m"
            memory: "4Gi"
        env:
        - name: ASPNETCORE_ENVIRONMENT
          value: "Production"
        - name: CONNECTION_STRING
          valueFrom:
            secretKeyRef:
              name: fortress-secrets
              key: sql-connection-string
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 10
      nodeSelector:
        nodepool-type: user
      tolerations:
      - key: "CriticalAddonsOnly"
        operator: "Exists"
        effect: "NoSchedule"
Service Example
yaml
apiVersion: v1
kind: Service
metadata:
  name: fortress-api-gateway
  namespace: fortress-api
  annotations:
    service.beta.kubernetes.io/azure-load-balancer-internal: "true"
spec:
  type: ClusterIP
  ports:
  - port: 8080
    targetPort: 8080
  selector:
    app: fortress-api-gateway
Ingress Example
yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: fortress-api-ingress
  namespace: fortress-api
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - api.fortress.ai
    secretName: fortress-tls-cert
  rules:
  - host: api.fortress.ai
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: fortress-api-gateway
            port:
              number: 8080
Best Practices
Resource Management
Always set requests and limits to prevent resource starvation

Use HPA for workloads with variable load

Use Cluster Autoscaler to handle node scaling

Prefer multiple replicas for high availability

Security
Use Azure AD Pod Identity or Workload Identity

Restrict RBAC permissions to least privilege

Enable Azure Policy for AKS

Use Network Policies to restrict pod-to-pod traffic

Scan images before deployment

Availability
Use Pod Disruption Budgets for critical workloads

Configure readiness and liveness probes

Deploy across availability zones

Enable Node Auto-Repair

Observability
Enable Container Insights for logging and metrics

Integrate with Application Insights for application performance

Configure Prometheus metrics for custom monitoring

Security Considerations
Security Layer	Implementation
Authentication	Entra ID integration, Azure RBAC
Network	Azure CNI, Network Policies, Private Cluster
Secrets	Key Vault CSI Driver
Image Security	ACR with Defender scanning, image signing
Compliance	Azure Policy, CIS benchmark compliance
Runtime Security	Defender for Containers, Falcon (CrowdStrike)
Monitoring
Key Metrics
Metric	Source	Alert Threshold
CPU Usage	Container Insights	> 80% for 10 min
Memory Usage	Container Insights	> 80% for 10 min
Pod Restarts	Kubernetes Events	> 5 in 5 min
Node Health	Azure Monitor	Node not ready
API Server	Control Plane Metrics	> 100ms latency
Dashboards
AKS Health Dashboard – Node and pod health

Application Performance Dashboard – Request rates, errors, latency

Cost Dashboard – Resource utilisation by namespace

Troubleshooting
Common Issues
Issue	Diagnosis	Solution
Pod stuck in Pending	Insufficient resources	Scale node pool, increase quotas
ImagePullBackOff	Image not found or auth failure	Check image tag, ACR credentials
CrashLoopBackOff	Application error	Check logs, liveness/readiness probes
Node NotReady	Node failure or upgrade	Check node logs, restart node
Useful Commands
bash
# Get pods
kubectl get pods -n fortress-api

# View logs
kubectl logs -n fortress-api pod-name

# Describe pod
kubectl describe pod -n fortress-api pod-name

# Get events
kubectl get events -n fortress-api --sort-by='.lastTimestamp'

# Check nodes
kubectl get nodes

# View resource usage
kubectl top pods -n fortress-api
kubectl top nodes
Checklist
AKS cluster created with system and user node pools

Node autoscaling configured

HPA configured for all workloads

Pod Disruption Budgets defined

Network Policies implemented

Azure Policy for AKS assigned

Container Insights enabled

Application Insights integrated

RBAC roles configured correctly

Managed Identity configured for AKS

ACR integration configured

Key Vault CSI Driver enabled

References
AZURE.md

DOCKER.md

CI_CD.md

SECRETS.md

This document is part of the Fortress Engineering Knowledge System (EKS) and is maintained by the Cloud Infrastructure & DevOps Team.

text

---
