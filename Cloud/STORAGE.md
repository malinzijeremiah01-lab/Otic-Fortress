# Storage Architecture & Standards

**Owner:**Esiana Emmanuel: Cloud Infrastructure & DevOps Team  
**Version:** 1.0.0  
**Last Updated:** 2026-07-01  
**Audience:** Cloud Architects, DevOps Engineers, Data Engineers  

---

## Purpose

This document defines the storage architecture, access patterns, and management standards for the Fortress AI Cybersecurity Platform. It covers Azure Storage Accounts, Blob Storage, File Storage, and Queue Storage for AI data, audit logs, and operational data.

---

## Scope

This document covers:

- Storage account types and SKUs
- Blob Storage for audit evidence, exports, and AI training data
- File Storage for shared configuration and logs
- Queue Storage for asynchronous processing
- Access control and security
- Backup and lifecycle policies

---

## Overview

### Why Azure Storage?

Azure Storage provides scalable, durable, and secure storage for Fortress:

| Requirement | Azure Storage Capability |
|-------------|---------------------------|
| **Audit Evidence** | Immutable Blob Storage |
| **AI Training Data** | Data Lake Storage Gen2 |
| **Shared Configuration** | Azure Files (NFS/SMB) |
| **Asynchronous Tasks** | Queue Storage |
| **Cost Optimisation** | Lifecycle policies, tiering |

---

## Architecture

```mermaid
graph TB
    subgraph "Storage Accounts"
        SA1[fortressprodeastusstore001]
        SA2[fortressprodwestusstore001]
    end

    subgraph "Blob Storage"
        BLOB1[audit-evidence - Immutable]
        BLOB2[ai-training-data - ADLS Gen2]
        BLOB3[exports-reports]
        BLOB4[logs-archive]
    end

    subgraph "File Storage"
        FILE1[shared-config]
        FILE2[prometheus-data]
    end

    subgraph "Queue Storage"
        QUEUE1[notification-queue]
        QUEUE2[event-processing-queue]
    end

    SA1 --> BLOB1
    SA1 --> BLOB2
    SA1 --> BLOB3
    SA1 --> BLOB4
    SA1 --> FILE1
    SA1 --> QUEUE1
    
    SA2 --> BLOB1
    SA2 --> BLOB2
Components
Storage Account Types
Environment	SKU	Replication	Tier
Production	Standard_LRS	LRS (Primary)	Hot/Cool
Production DR	Standard_GRS	GRS (Secondary)	Hot/Cool
Backup	Standard_ZRS	ZRS	Hot/Cool
Archive	Standard_LRS	LRS	Archive
Storage Account Naming
text
{project}{env}{region}store{number}
Examples:

fortressprodeastusstore001

fortressstagingeastusstore001

Blob Storage
Container Structure
text
storage-account/
├── audit-evidence/
│   ├── yyyy/mm/dd/
│   │   └── audit-{tenant}-{date}-{uuid}.json
├── ai-training-data/
│   ├── raw/
│   │   └── {dataset}/{version}/
│   ├── processed/
│   │   └── {dataset}/{version}/
│   └── labels/
│       └── {dataset}/{version}/
├── exports/
│   ├── reports/
│   │   └── {report-type}/{date}/
│   └── compliance/
│       └── {framework}/{date}/
└── logs-archive/
    └── {service}/{yyyy}/{mm}/
Immutable Blob Storage
Audit evidence requires immutability:

json
{
  "policy": {
    "ruleName": "audit-immutability",
    "type": "TimeBasedRetention",
    "retentionDays": 2555,  // 7 years
    "allowProtectedAppendWrites": true
  }
}
Lifecycle Policies
json
{
  "rules": [
    {
      "name": "archive-audit-logs",
      "enabled": true,
      "filters": {
        "prefixMatch": ["audit-evidence/"],
        "blobTypes": ["blockBlob"]
      },
      "actions": {
        "baseBlob": {
          "tierToCool": {
            "daysAfterModificationGreaterThan": 30
          },
          "tierToArchive": {
            "daysAfterModificationGreaterThan": 90
          },
          "delete": {
            "daysAfterModificationGreaterThan": 2555
          }
        }
      }
    }
  ]
}
File Storage (Azure Files)
Shares
Share Name	Purpose	Access
fortress-config	Shared configuration files	NFS
fortress-logs	Application logs	SMB
prometheus-data	Prometheus metrics storage	NFS
Mount Example
yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: fortress-config-pvc
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: azurefile-csi
  resources:
    requests:
      storage: 10Gi
Queue Storage
Queues
Queue Name	Purpose
notification-queue	Notification service work items
event-processing-queue	Event Processor work items
audit-ingest-queue	Audit record ingestion
ai-shadow-queue	AI Shadow processing tasks
Access Control
Authentication Methods
Method	Use Case
Managed Identity	AKS pod access to storage
SAS Tokens	Time-limited access
Storage Account Key	CI/CD pipelines (avoid if possible)
Managed Identity Example
yaml
apiVersion: v1
kind: Pod
metadata:
  name: fortress-audit
  annotations:
    azure.workload.identity/client-id: "xxx"
spec:
  serviceAccountName: workload-identity-sa
  containers:
  - name: audit
    image: fortress-audit:latest
    env:
    - name: STORAGE_ACCOUNT
      value: "fortressprodeastusstore001"
Backup Strategy
Data Type	Backup Method	Frequency	Retention
Audit Evidence	Immutable Storage (no backup needed)	N/A	7 years
AI Training Data	Cross-region replication	Daily	30 days
Exports/Reports	Backup to DR region	Daily	90 days
Configuration	Git repository	On change	Indefinite
Cost Optimization
Strategy	Implementation
Tiering	Hot → Cool → Archive based on access patterns
Lifecycle Policies	Automate tier transitions
Reserved Capacity	Purchase reserved capacity for predictable usage
Delete Orphaned Data	Weekly cleanup of temporary files
Monitoring
Metric	Alert Threshold
Storage Used	> 80%
Transactions	> 1M/hour
Failed Requests	> 5%
Latency	> 100ms
Troubleshooting
Issue	Solution
Authorization error	Check Managed Identity, RBAC
Slow throughput	Check tier, network latency
Storage full	Run lifecycle policy, delete old data
Useful Commands
bash
# List storage accounts
az storage account list --resource-group fortress-prod-rg

# Show container
az storage container list --account-name fortressprodeastusstore001

# Copy blob
az storage blob copy start \
  --source-account-name source \
  --source-container container \
  --source-blob blob \
  --destination-account-name destination \
  --destination-container container \
  --destination-blob blob
Checklist
Storage account created with correct SKU

Immutability policy enabled for audit evidence

Lifecycle policies configured

Managed Identity assigned

Private Endpoint configured

Backup strategy defined

Monitoring alerts configured

References
BACKUP.md

MONITORING.md

This document is part of the Fortress Engineering Knowledge System (EKS).

text

---