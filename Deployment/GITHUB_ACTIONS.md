# GitHub Actions Workflow Standards

**Owner:**Esiana Emmanuel: Cloud Infrastructure & DevOps Team  
**Version:** 1.0.0  
**Last Updated:** 2026-07-01  
**Audience:** DevOps Engineers, Developers, Platform Engineers  

---

## Purpose

This document defines the standards for GitHub Actions workflows used to build, test, scan, and deploy the Fortress AI Cybersecurity Platform.

---

## Scope

This document covers:

- Workflow syntax and structure
- Jobs, steps, and runners
- Secrets and variables
- Matrix builds
- Reusable workflows
- Sample production workflow

---

## Overview

### Why GitHub Actions?

- **Native integration** with GitHub repositories
- **Flexible runners** – Linux, Windows, macOS, self-hosted
- **Large ecosystem** of pre-built actions
- **Cost-effective** – Free for open source

---

## Workflow Structure

```yaml
name: Fortress CI

on:
  push:
    branches: [main, develop]
  pull_request:
    types: [opened, synchronize]

env:
  REGISTRY: fortress.azurecr.io

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run build
        run: make build

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Run tests
        run: make test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy
        run: make deploy
Reusable Workflows
Build Workflow (reusable)
yaml
# .github/workflows/reusable-build.yml
name: Reusable Build

on:
  workflow_call:
    inputs:
      service:
        required: true
        type: string
    secrets:
      ACR_USERNAME:
        required: true
      ACR_PASSWORD:
        required: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build ${{ inputs.service }}
        run: |
          docker build -t ${{ inputs.service }} ./services/${{ inputs.service }}
Using Reusable Workflow
yaml
# .github/workflows/fortress-api.yml
name: Build Fortress API

on:
  push:
    paths:
      - 'services/api/**'

jobs:
  build:
    uses: ./.github/workflows/reusable-build.yml
    with:
      service: api
    secrets:
      ACR_USERNAME: ${{ secrets.ACR_USERNAME }}
      ACR_PASSWORD: ${{ secrets.ACR_PASSWORD }}
Matrix Builds
yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11']
        os: [ubuntu-latest, windows-latest]
    steps:
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Run tests
        run: pytest
Secrets & Variables
Secrets
yaml
secrets:
  ACR_USERNAME:
    description: 'ACR username'
    required: true
  ACR_PASSWORD:
    description: 'ACR password'
    required: true
Environment Variables
yaml
env:
  REGISTRY: fortress.azurecr.io
  IMAGE_NAME: fortress-api
  ENVIRONMENT: production
Sample Production Workflow
yaml
name: Fortress Production Deployment

on:
  push:
    branches: [main]
    paths:
      - 'services/api/**'

env:
  REGISTRY: fortress.azurecr.io
  IMAGE_NAME: fortress-api
  K8S_NAMESPACE: fortress-api

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: azure/docker-login@v1
        with:
          login-server: ${{ env.REGISTRY }}
          username: ${{ secrets.ACR_USERNAME }}
          password: ${{ secrets.ACR_PASSWORD }}
      - name: Build and Push
        uses: docker/build-push-action@v5
        with:
          context: ./services/api
          push: true
          tags: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest

  deploy-production:
    needs: build-and-push
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      - name: Deploy to AKS
        uses: azure/k8s-deploy@v4
        with:
          manifests: ./deploy/manifests/
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          namespace: ${{ env.K8S_NAMESPACE }}
          strategy: canary
Best Practices
1. Use Matrix for Testing
yaml
strategy:
  matrix:
    version: [3.10, 3.11, 3.12]
2. Cache Dependencies
yaml
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
3. Set Resource Limits
yaml
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 20
4. Use Environment Protection
yaml
environment:
  name: production
  url: https://api.fortress.ai
Monitoring
Metric	Alert Threshold
Workflow Failure	Any failure
Workflow Duration	> 20 minutes
Checklist
Workflow defined for each service

Secrets configured in GitHub

Reusable workflows for common steps

Matrix testing for multiple versions

Environment protection for production

References
CI_CD.md

DEPLOYMENT.md

This document is part of the Fortress Engineering Knowledge System (EKS).

text