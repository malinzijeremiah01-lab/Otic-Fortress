# Backup & Recovery Procedures

**Owner:**Esiana Emmanuel: Cloud Infrastructure & DevOps Team  
**Version:** 1.0.0  
**Last Updated:** 2026-07-01  
**Audience:** SREs, DevOps Engineers, Platform Engineers  

---

## Purpose

This document defines the backup strategy, schedules, retention policies, and recovery procedures for all Fortress platform data. It ensures data durability and business continuity in case of accidental deletion, corruption, or regional failure.

---

## Scope

This document covers:

- Backup strategy for Azure SQL, Cosmos DB, Blob Storage
- Backup schedules and retention policies
- Recovery procedures for each data type
- Backup validation and testing
- Automation and monitoring

---

## Overview

### Why Backups?

Fortress stores critical data including:

- **Governance policies** – Enterprise AI rules
- **Audit records** – Compliance evidence
- **AI telemetry** – Operational analytics
- **Configuration** – Tenant and user settings

Losing this data could result in compliance violations, operational downtime, and customer impact.

---

## Architecture

```mermaid
graph TB
    subgraph "Production (East US)"
        SQL1[Azure SQL Primary]
        COSMOS1[Cosmos DB Primary]
        BLOB1[Blob Storage Primary]
    end

    subgraph "DR Region (West US)"
        SQL2[Azure SQL Geo-Replica]
        COSMOS2[Cosmos DB Geo-Replica]
        BLOB2[Blob Storage RA-GRS]
    end

    subgraph "Backup Storage"
        BACKUP1[Azure SQL Backup - 35 days]
        BACKUP2[Cosmos Backup - 30 days]
        BACKUP3[Blob Archive - 7 years]
    end

    SQL1 -->|Geo-Replication| SQL2
    COSMOS1 -->|Geo-Replication| COSMOS2
    BLOB1 -->|RA-GRS| BLOB2
    
    SQL1 -->|Daily Full Backup| BACKUP1
    COSMOS1 -->|Continuous Backup| BACKUP2
    BLOB1 -->|Lifecycle Policy| BACKUP3
Backup Schedules
Azure SQL Database
Backup Type	Frequency	Retention	Location
Full Backup	Daily	35 days	Geo-redundant
Differential	12 hours	35 days	Geo-redundant
Transaction Log	5 minutes	35 days	Geo-redundant
Long-Term Retention	Weekly	10 years	Archive storage
Cosmos DB
Backup Type	Frequency	Retention	Location
Continuous Backup	Real-time	30 days	Geo-redundant
Point-in-Time Restore	Up to 30 days	30 days	Geo-redundant
Blob Storage
Data Type	Backup Method	Frequency	Retention
Audit Evidence	Immutable Storage	N/A	7 years
AI Training Data	Cross-region replication	Daily	30 days
Exports/Reports	Backup to DR	Daily	90 days
Backup Configurations
Azure SQL – Long-Term Retention
sql
-- Set LTR policy via Azure CLI
az sql db ltr-policy set \
  --resource-group fortress-prod-rg \
  --server fortress-prod-eastus-sql-001 \
  --name fortress-prod-db \
  --weekly-retention "P10Y" \
  --monthly-retention "P10Y" \
  --yearly-retention "P10Y"
Cosmos DB – Continuous Backup
bash
# Enable continuous backup
az cosmosdb update \
  --resource-group fortress-prod-rg \
  --name fortress-prod-eastus-cosmos-001 \
  --backup-policy-type Continuous
Blob Storage – Soft Delete
bash
# Enable soft delete
az storage blob service-properties delete-policy update \
  --account-name fortressprodeastusstore001 \
  --enable true \
  --days-retained 7
Recovery Procedures
SQL Database Restore
bash
# Restore to a point in time
az sql db restore \
  --resource-group fortress-prod-rg \
  --server fortress-prod-eastus-sql-001 \
  --dest-resource-group fortress-prod-rg \
  --dest-server fortress-prod-eastus-sql-001 \
  --dest-db fortress-prod-db-restore \
  --deleted-time "2026-07-01T10:00:00"
Cosmos DB Restore
bash
# Restore to a point in time
az cosmosdb restore \
  --resource-group fortress-prod-rg \
  --account-name fortress-prod-eastus-cosmos-001 \
  --source-database-name fortress-db \
  --restore-timestamp "2026-07-01T10:00:00"
Blob Storage Restore
bash
# Restore blob from soft delete
az storage blob restore \
  --account-name fortressprodeastusstore001 \
  --container-name audit-evidence \
  --name file.json \
  --time "2026-07-01T10:00:00"
Backup Validation
Weekly Backup Validation Script
powershell
# Validate SQL backups
$databases = Get-AzSqlDatabase -ResourceGroupName "fortress-prod-rg" `
    -ServerName "fortress-prod-eastus-sql-001"

foreach ($db in $databases) {
    $backups = Get-AzSqlDatabaseRestorePoint -ResourceGroupName "fortress-prod-rg" `
        -ServerName "fortress-prod-eastus-sql-001" `
        -DatabaseName $db.DatabaseName
    
    if ($backups.Count -eq 0) {
        Write-Warning "No backups found for $($db.DatabaseName)"
    }
    
    # Test restore to validation environment
    Restore-AzSqlDatabase -FromPointInTimeBackup `
        -ResourceGroupName "fortress-validate-rg" `
        -ServerName "fortress-validate-sql-001" `
        -DatabaseName "$($db.DatabaseName)-restore-test" `
        -RestorePointInTime (Get-Date).AddHours(-6)
}
Monitoring
Metric	Alert Threshold
Backup Status	Any backup failure
Backup Age	> 24 hours since last backup
Restoration Time	> 1 hour
Troubleshooting
Issue	Solution
Backup failure	Check storage capacity, network connectivity
Restore timeout	Check resource capacity, use larger tier
Corrupted backup	Use an earlier restore point
Checklist
SQL automated backups enabled

Cosmos continuous backup enabled

Blob soft delete enabled

Long-term retention configured for SQL

Backup validation script created

Recovery procedures documented and tested

Backup monitoring alerts configured

References
DISASTER_RECOVERY.md

MONITORING.md

This document is part of the Fortress Engineering Knowledge System (EKS).

text

---
