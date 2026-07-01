# CI/CD Pipeline Architecture

**Owner:**Esiana Emmanuel: Cloud Infrastructure & DevOps Team  
**Version:** 1.0.0  
**Last Updated:** 2026-07-01  
**Audience:** DevOps Engineers, Developers, Platform Engineers  

---

## Purpose

This document defines the CI/CD pipeline architecture for the Fortress AI Cybersecurity Platform. It covers build, test, security scanning, container packaging, and deployment automation.

---

## Scope

This document covers:

- CI/CD concepts and principles
- Pipeline stages (Build, Test, Scan, Package, Deploy)
- GitHub Actions integration
- Secrets management
- Deployment approvals

---

## Overview

### Why CI/CD?

CI/CD enables Fortress to:

- **Release faster** – Automate build and deployment
- **Reduce errors** – Consistent, repeatable process
- **Improve quality** – Automated testing and scanning
- **Increase confidence** – Rollback and approval gates

---

## Architecture

```mermaid
graph LR
    subgraph "CI Pipeline"
        CODE[Code Push]
        BUILD[Build]
        TEST[Test]
        SCAN[Security Scan]
        PACKAGE[Package Container]
        PUSH[Push to ACR]
    end

    subgraph "CD Pipeline"
        DEV[Deploy Dev]
        QA[Deploy QA]
        STG[Deploy Staging]
        APPROVAL[Approval Gate]
        PROD[Deploy Production]
    end

    subgraph "Monitoring"
        MON[Post-Deploy Monitoring]
        ALERT[Alert on Failure]
    end

    CODE --> BUILD
    BUILD --> TEST
    TEST --> SCAN
    SCAN --> PACKAGE
    PACKAGE --> PUSH
    PUSH --> DEV
    DEV --> QA
    QA --> STG
    STG --> APPROVAL
    APPROVAL --> PROD
    PROD --> MON
    MON --> ALERT
Pipeline Stages
Stage 1: Build
yaml
- name: Build Docker Image
  uses: docker/build-push-action@v5
  with:
    context: .
    push: false
    tags: ${{ env.IMAGE_NAME }}:latest
Stage 2: Test
yaml
- name: Run Unit Tests
  run: |
    docker run --rm ${{ env.IMAGE_NAME }}:latest pytest

- name: Run Integration Tests
  run: |
    docker-compose -f docker-compose.test.yml up --abort-on-container-exit
Stage 3: Security Scan
yaml
- name: Scan for Vulnerabilities
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ${{ env.IMAGE_NAME }}:latest
    format: 'table'
    exit-code: '1'
    severity: 'CRITICAL,HIGH'
Stage 4: Package
yaml
- name: Tag and Push
  run: |
    docker tag ${{ env.IMAGE_NAME }}:latest ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ env.TAG }}
    docker push ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ env.TAG }}
Stage 5: Deploy
yaml
- name: Deploy to Kubernetes
  uses: azure/k8s-deploy@v4
  with:
    manifests: ./deploy/manifests/
    images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ env.TAG }}
GitHub Actions Workflow
Complete workflow file:

yaml
name: Fortress CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: fortress.azurecr.io
  IMAGE_NAME: fortress-api

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Docker
        uses: docker/setup-buildx-action@v3
      - name: Build
        run: docker build -t $IMAGE_NAME:latest .
      - name: Test
        run: docker run --rm $IMAGE_NAME:latest pytest
      - name: Scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: $IMAGE_NAME:latest
          severity: HIGH,CRITICAL
      - name: Login to ACR
        uses: azure/docker-login@v1
        with:
          login-server: ${{ env.REGISTRY }}
          username: ${{ secrets.ACR_USERNAME }}
          password: ${{ secrets.ACR_PASSWORD }}
      - name: Push
        run: |
          docker tag $IMAGE_NAME:latest $REGISTRY/$IMAGE_NAME:latest
          docker push $REGISTRY/$IMAGE_NAME:latest

  cd:
    needs: ci
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - name: Login to Azure
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      - name: Deploy to AKS
        uses: azure/k8s-deploy@v4
        with:
          manifests: ./deploy/manifests/
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
Secrets Management
Secret	Purpose	Source
ACR_USERNAME	ACR authentication	Azure
ACR_PASSWORD	ACR authentication	Azure
AZURE_CREDENTIALS	Azure login	Service Principal
GH_PAT	GitHub token	GitHub
Deployment Approvals
Environment	Approval Required	Approver
Development	No	-
QA	No	-
Staging	No	-
Production	Yes	Engineering Manager
Rollback Strategy
yaml
rollback:
  - name: Revert to previous version
    run: |
      kubectl set image deployment/fortress-api \
        fortress-api=$REGISTRY/$IMAGE_NAME:${{ github.event.inputs.rollback_tag }}
      kubectl rollout status deployment/fortress-api
Monitoring
Metric	Alert Threshold
Build Failure	Any failure
Deployment Failure	Any failure
Long Build Time	> 10 minutes
Checklist
CI pipeline configured

CD pipeline configured

Security scanning enabled

Deployment approvals configured

Rollback procedures documented

References
GITHUB_ACTIONS.md

DEPLOYMENT.md

This document is part of the Fortress Engineering Knowledge System (EKS).

text

---