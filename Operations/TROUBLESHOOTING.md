# Troubleshooting Guide

**Owner:**Esiana Emmanuel: Cloud Infrastructure & DevOps Team  
**Version:** 1.0.0  
**Last Updated:** 2026-07-01  
**Audience:** SREs, DevOps Engineers, Developers  

---

## Purpose

This document provides troubleshooting procedures for common issues with the Fortress AI Cybersecurity Platform.

---

## Scope

This document covers:

- Common issues and diagnosis
- Solutions and workarounds
- Useful Azure CLI commands
- Useful kubectl commands
- Useful Docker commands

---

## Common Issues

### Issue 1: Pod Stuck in Pending

**Symptom:** `kubectl get pods` shows `Pending` status for more than 5 minutes.

**Diagnosis:**
```bash
kubectl describe pod -n fortress-api <pod-name>
Possible Causes & Solutions:

Cause	Solution
Insufficient resources	Scale node pool or reduce requests
Node taint	Add toleration to pod spec
PersistentVolumeClaim not bound	Check PVC status, create if needed
Issue 2: ImagePullBackOff
Symptom: kubectl get pods shows ImagePullBackOff or ErrImagePull.

Diagnosis:

bash
kubectl describe pod -n fortress-api <pod-name>
Solutions:

bash
# Check image exists
az acr repository show-tags --name fortressprodeastusacr001 --repository fortress-api

# Test pull manually
docker pull fortress.azurecr.io/fortress-api:latest

# Check ACR authentication
az acr login --name fortressprodeastusacr001
Issue 3: CrashLoopBackOff
Symptom: Pod crashes repeatedly.

Diagnosis:

bash
# View logs
kubectl logs -n fortress-api <pod-name>

# Previous container logs
kubectl logs -n fortress-api <pod-name> --previous
Solutions:

bash
# Restart pod
kubectl delete pod -n fortress-api <pod-name>

# Check resource limits
kubectl describe pod -n fortress-api <pod-name>
Issue 4: Service Unavailable
Symptom: 503 errors, connection refused.

Diagnosis:

bash
# Check service endpoints
kubectl get endpoints -n fortress-api

# Check ingress
kubectl get ingress -n fortress-api

# Test internal connectivity
kubectl run -it --rm debug --image=busybox -- /bin/sh
wget -O- http://fortress-api:8080/health
Issue 5: Database Connection Failure
Symptom: Application errors about database connectivity.

Diagnosis:

bash
# Check SQL status
az sql db show --resource-group fortress-prod-rg --server fortress-prod-sql --name fortress-prod

# Check firewall rules
az sql server firewall-rule list --resource-group fortress-prod-rg --server fortress-prod-sql
Solutions:

bash
# Allow AKS subnet
az sql server firewall-rule create \
  --resource-group fortress-prod-rg \
  --server fortress-prod-sql \
  --name allow-aks \
  --start-ip-address 10.1.0.0 \
  --end-ip-address 10.1.15.255

# Test connection from pod
kubectl run -it --rm debug --image=postgres:15 -- /bin/sh
psql -h fortress-prod-sql.postgres.database.azure.com -U fortress -d fortress
Useful Azure CLI Commands
Resource Management
bash
# List resources
az resource list --resource-group fortress-prod-rg

# Show resource
az resource show --resource-group fortress-prod-rg --name fortress-prod-aks --resource-type Microsoft.ContainerService/managedClusters

# Tag resources
az resource tag --tags Environment=Production --ids $(az resource list -g fortress-prod-rg --query "[].id" -o tsv)
AKS Commands
bash
# Get cluster credentials
az aks get-credentials --resource-group fortress-prod-rg --name fortress-prod-aks

# Show cluster
az aks show --resource-group fortress-prod-rg --name fortress-prod-aks

# Scale cluster
az aks scale --resource-group fortress-prod-rg --name fortress-prod-aks --node-count 5
Database Commands
bash
# Show databases
az sql db list --resource-group fortress-prod-rg --server fortress-prod-sql

# Show backups
az sql db list-restore-points --resource-group fortress-prod-rg --server fortress-prod-sql --name fortress-prod

# Restore database
az sql db restore --resource-group fortress-prod-rg --server fortress-prod-sql --dest-resource-group fortress-prod-rg --dest-server fortress-prod-sql --dest-db fortress-prod-restore --deleted-time "2026-07-01T10:00:00"
Storage Commands
bash
# List storage accounts
az storage account list --resource-group fortress-prod-rg

# Show container
az storage container list --account-name fortressprodeastusstore001

# Copy blob
az storage blob copy start --source-account-name source --source-container container --source-blob blob --destination-account-name destination --destination-container container --destination-blob blob
Useful kubectl Commands
Pod Management
bash
# List pods
kubectl get pods -n fortress-api

# Describe pod
kubectl describe pod -n fortress-api <pod-name>

# Get logs
kubectl logs -n fortress-api <pod-name>

# Tail logs
kubectl logs -f -n fortress-api <pod-name>

# Previous logs
kubectl logs -n fortress-api <pod-name> --previous

# Exec into pod
kubectl exec -it -n fortress-api <pod-name> -- /bin/bash

# Delete pod
kubectl delete pod -n fortress-api <pod-name>
Deployment Management
bash
# List deployments
kubectl get deployments -n fortress-api

# Describe deployment
kubectl describe deployment -n fortress-api fortress-api

# Rollout status
kubectl rollout status deployment -n fortress-api fortress-api

# Rollout history
kubectl rollout history deployment -n fortress-api fortress-api

# Rollback
kubectl rollout undo deployment -n fortress-api fortress-api

# Scale
kubectl scale deployment -n fortress-api fortress-api --replicas=5
Service & Ingress
bash
# List services
kubectl get svc -n fortress-api

# Describe service
kubectl describe svc -n fortress-api fortress-api

# List ingress
kubectl get ingress -n fortress-api
Events & Debugging
bash
# Get events
kubectl get events -n fortress-api --sort-by='.lastTimestamp'

# Top nodes
kubectl top nodes

# Top pods
kubectl top pods -n fortress-api
Useful Docker Commands
Image Management
bash
# List images
docker images

# Remove image
docker rmi fortress-api:latest

# Build image
docker build -t fortress-api:latest .

# Tag image
docker tag fortress-api:latest fortress.azurecr.io/fortress-api:latest

# Push image
docker push fortress.azurecr.io/fortress-api:latest
Container Management
bash
# List containers
docker ps -a

# Stop container
docker stop <container-id>

# Remove container
docker rm <container-id>

# Exec into container
docker exec -it <container-id> /bin/bash

# View logs
docker logs -f <container-id>

# Inspect container
docker inspect <container-id>
System Commands
bash
# Docker info
docker info

# System prune
docker system prune -af

# Show disk usage
docker system df
Debugging Checklist
Check pod status (kubectl get pods)

View pod logs (kubectl logs)

Describe pod (kubectl describe pod)

Check service status (kubectl get svc)

Check ingress (kubectl get ingress)

Check node status (kubectl get nodes)

Check Azure resources (az resource list)

Check database connectivity

Check Key Vault access

