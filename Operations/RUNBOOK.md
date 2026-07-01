# Operational Runbook

**Owner:**Esiana Emmanuel: Cloud Infrastructure & DevOps Team  
**Version:** 1.0.0  
**Last Updated:** 2026-07-01  
**Audience:** SREs, DevOps Engineers, On-call Engineers  

---

## Purpose

This document provides operational procedures for managing the Fortress AI Cybersecurity Platform in production.

---

## Scope

This document covers:

- Deployment procedures
- Service restart
- Scaling
- Image updates
- Emergency response

---

## Deployment Procedures

### Standard Deployment

```bash
# 1. Apply manifests
kubectl apply -f ./deploy/manifests/

# 2. Verify rollout
kubectl rollout status deployment/fortress-api -n fortress-api

# 3. Check pods
kubectl get pods -n fortress-api

# 4. Monitor logs
kubectl logs -f deployment/fortress-api -n fortress-api
Canary Deployment
bash
# 1. Deploy new version (10% traffic)
kubectl set image deployment/fortress-api fortress-api=fortress.azurecr.io/fortress-api:v1.2.3

# 2. Monitor for 30 minutes
# 3. Increase to 50% traffic
kubectl patch virtualservice fortress-api -n fortress-api -p '{"spec":{"http":[{"route":[{"destination":{"host":"fortress-api","subset":"v123"},"weight":50},{"destination":{"host":"fortress-api","subset":"stable"},"weight":50}]}]}}'

# 4. Monitor for 30 minutes
# 5. Increase to 100% traffic
kubectl patch virtualservice fortress-api -n fortress-api -p '{"spec":{"http":[{"route":[{"destination":{"host":"fortress-api","subset":"v123"},"weight":100}]}]}}'
Restarting Services
Restart Single Pod
bash
# Delete pod (will restart)
kubectl delete pod -n fortress-api fortress-api-xxxxx

# Restart deployment
kubectl rollout restart deployment/fortress-api -n fortress-api
Restart All Services
bash
kubectl rollout restart deployment -n fortress-api
kubectl rollout restart deployment -n fortress-control
kubectl rollout restart deployment -n fortress-data
kubectl rollout restart deployment -n fortress-ai
Scaling
Horizontal Scaling
bash
# Scale deployment
kubectl scale deployment/fortress-api --replicas=5 -n fortress-api

# Auto-scaling (HPA)
kubectl autoscale deployment/fortress-api --cpu-percent=80 --min=3 --max=10 -n fortress-api
Cluster Scaling
bash
# Scale AKS cluster
az aks scale \
  --resource-group fortress-prod-rg \
  --name fortress-prod-aks \
  --node-count 5
Updating Images
Update Service Image
bash
# Set new image
kubectl set image deployment/fortress-api fortress-api=fortress.azurecr.io/fortress-api:v1.2.4

# Monitor rollout
kubectl rollout status deployment/fortress-api -n fortress-api
Rollback Image
bash
# Undo to previous revision
kubectl rollout undo deployment/fortress-api -n fortress-api

# Rollback to specific revision
kubectl rollout undo deployment/fortress-api --to-revision=2 -n fortress-api
Emergency Response
Emergency Contacts
Contact	Role	Phone
Primary On-call	DevOps Engineer	+1-XXX-XXX-XXXX
Secondary On-call	SRE Engineer	+1-XXX-XXX-XXXX
Incident Commander	Engineering Manager	+1-XXX-XXX-XXXX
Emergency Actions
Scenario	Action
Pod crash	View logs, restart pod
Service unavailable	Check ingress, load balancer
Database failure	Failover to replica
Security breach	Isolate service, notify security
Daily Health Check
Morning Checklist
bash
# 1. Check node health
kubectl get nodes

# 2. Check pod health
kubectl get pods -n fortress-api
kubectl get pods -n fortress-control

# 3. Check service availability
curl -f https://api.fortress.ai/health

# 4. Check database
az sql db show --resource-group fortress-prod-rg --server fortress-prod-sql --name fortress-prod

# 5. Check Key Vault
az keyvault show --name fortress-prod-kv

# 6. Check storage
az storage account show --name fortressprodeastusstore001

# 7. Review metrics
az monitor metrics list --resource fortress-prod-aks --metric node_cpu_usage
Troubleshooting Commands
bash
# Get logs
kubectl logs -n fortress-api <pod-name>

# Describe pod
kubectl describe pod -n fortress-api <pod-name>

# Get events
kubectl get events -n fortress-api --sort-by='.lastTimestamp'

# Check resources
kubectl top pods -n fortress-api
kubectl top nodes

# Exec into container
kubectl exec -it -n fortress-api <pod-name> -- /bin/bash
Checklist
Deployment procedures documented

Restart procedures tested

Scaling procedures tested

Image update procedures tested

Emergency contacts listed

References
INCIDENT_RESPONSE.md

MONITORING_GUIDE.md

This document is part of the Fortress Engineering Knowledge System (EKS).

text