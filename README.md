# Azure Journey — AKS + CI/CD + Azure OpenAI (RAG PoC)

This repository contains a hands-on proof of concept demonstrating a complete
cloud-native deployment on Microsoft Azure, including a working
Retrieval-Augmented Generation (RAG) API.

The project shows how to build, deploy, and operate a containerized application
on Azure Kubernetes Service (AKS) with CI/CD, cost control, and Azure OpenAI
integration.

---

## What Is Implemented

- Containerized Python backend (FastAPI-style API)
- Azure Kubernetes Service (AKS)
- Public exposure via Kubernetes LoadBalancer
- CI/CD pipeline using GitHub Actions
- Azure Container Registry (ACR)
- Azure OpenAI (Chat Completions)
- Document-based Q&A (RAG)
- Azure Budget and cost monitoring

---

## Architecture Overview

Client (curl / browser)  
→ Azure LoadBalancer (Kubernetes Service)  
→ AKS Pod (Python API)  
→ Azure OpenAI (Chat / RAG)

---

## Repository Structure

```text
.
├── aks-poc/
│   ├── app.py
│   ├── Dockerfile
│   ├── deployment.yaml
│   └── service.yaml
├── docs/
│   └── source.txt
├── .github/
│   └── workflows/
│       └── deploy-aks.yml
└── README.md
```

---

## Deployed API

The application is deployed to Azure Kubernetes Service (AKS) and exposed
publicly using a Kubernetes Service of type `LoadBalancer`.

### Available Endpoints

- `GET /health`
  - Simple health check
- `POST /chat`
  - Free-form chat using Azure OpenAI
- `POST /rag`
  - Answers questions **only** using the document in `docs/source.txt`

---

## How to Get the External IP (AKS)

After deployment, retrieve the public IP address:

```bash
kubectl get svc aks-poc-svc
```

Example output:

```text
NAME           TYPE           CLUSTER-IP     EXTERNAL-IP       PORT(S)
aks-poc-svc    LoadBalancer   10.0.179.220   134.xxx.xxx.xxx  80:30225/TCP
```

The application is available at:

```text
http://<EXTERNAL-IP>
```

---

## How to Test the Application

### Health Check

```bash
curl http://<EXTERNAL-IP>/health
```

Expected response:

```json
{ "status": "ok" }
```

---

### Chat Endpoint (Azure OpenAI)

```bash
curl -X POST http://<EXTERNAL-IP>/chat \
  -H "Content-Type: application/json" \
  -d '{"text":"Write one sentence confirming Azure OpenAI works."}'
```

---

## RAG — Document-Based Q&A (WORKING EXAMPLE)

The RAG endpoint answers **only if the information exists in `docs/source.txt`**.

### Document Content

File: `docs/source.txt`

```text
Azure Kubernetes Service (AKS) is a managed Kubernetes service provided by Microsoft Azure.
It allows users to deploy, manage and scale containerized applications without managing
the underlying control plane.

AKS integrates with Azure services such as Azure Container Registry, Azure Monitor
and Azure Active Directory.
```

---

### Ask a Question Answerable From the Document

```bash
curl -X POST http://<EXTERNAL-IP>/rag \
  -H "Content-Type: application/json" \
  -d '{"question":"What is Azure Kubernetes Service (AKS)?"}'
```

Example response:

```json
{
  "answer": "Azure Kubernetes Service (AKS) is a managed Kubernetes service provided by Microsoft Azure that allows users to deploy, manage, and scale containerized applications without managing the underlying control plane.",
  "source": "docs/source.txt"
}
```

✅ Answer comes **directly from the document**  
✅ Source is explicitly returned

---

### Ask a Question NOT Covered by the Document

```bash
curl -X POST http://<EXTERNAL-IP>/rag \
  -H "Content-Type: application/json" \
  -d '{"question":"What is the weather today?"}'
```

Example response:

```json
{
  "answer": "I do not know based on the provided document.",
  "source": "docs/source.txt"
}
```

✅ No hallucination  
✅ Strict document grounding

---

## Azure OpenAI Configuration

- Service: Azure OpenAI
- Model: `gpt-4o-mini`
- Deployment name: `gpt-chat`
- Authentication: API Key
- API access via environment variables

Secrets are injected using:
- GitHub Actions
- Kubernetes Secrets

No secrets are stored in the repository.

---

## CI/CD Pipeline

Automated deployment using GitHub Actions:

1. Azure login via Service Principal
2. Docker image build
3. Push image to Azure Container Registry (ACR)
4. Fetch AKS credentials
5. Deploy to AKS
6. Rolling update with health checks

Workflow file:

```text
.github/workflows/deploy-aks.yml
```

---

## Cost Control

This project runs under an Azure subscription with an active budget and alerts.

Recommendations:
- Monitor Azure Cost Management regularly
- Delete resources when not in use:
  - AKS cluster
  - Azure Container Registry
  - Azure OpenAI resource

---

## Purpose

This project is intended as:

- a learning journey
- a portfolio proof of concept
- a demonstration of real Azure + Kubernetes + AI skills

It is **not production-ready** by design and focuses on clarity and learning.