# Azure Journey – AKS + Azure OpenAI PoC

This repository contains a learning / proof-of-concept project demonstrating how to deploy
a containerized backend application to Azure Kubernetes Service (AKS) and integrate it with
Azure OpenAI.

The project focuses on practical understanding of Azure, Kubernetes, CI/CD and AI services.
It is not intended to be production-ready.

---

## Architecture

Client (browser / curl)
→ Azure LoadBalancer (AKS Service)
→ AKS Pod (containerized backend)
→ Azure OpenAI (gpt-4o-mini)

---

## Deployed API

The application is deployed to AKS and exposed publicly using a Kubernetes Service
of type LoadBalancer.

---

## Finding the External IP (AKS)

To retrieve the public IP address of the application:

kubectl get svc

Look for the service with TYPE = LoadBalancer and copy the value from the EXTERNAL-IP column.

Example:
NAME           TYPE           CLUSTER-IP     EXTERNAL-IP      PORT(S)
aks-poc-svc    LoadBalancer   10.0.145.123   20.82.xxx.xxx   80:31234/TCP

The application is available at:
http://<EXTERNAL-IP>

---

### Health check

Endpoint:
GET /health

Example:
curl http://<EXTERNAL-IP>/health

---

### Chat endpoint (Azure OpenAI)

Endpoint:
POST /chat

Example:
curl -X POST http://<EXTERNAL-IP>/chat \
-H "Content-Type: application/json" \
-d '{"text":"Napisz jedno zdanie po polsku, że Azure OpenAI działa."}'

Example response:
{
  "answer": "Azure OpenAI działa poprawnie i umożliwia przetwarzanie języka naturalnego."
}

---

## Azure OpenAI Integration

Service: Azure OpenAI  
Model: gpt-4o-mini  
Deployment name: gpt-chat  
Authentication: API Key  
Configuration: environment variables  

The backend application communicates directly with the Azure OpenAI endpoint.
Secrets are not stored in the repository.

---

## CI/CD

The project uses GitHub Actions for automated deployment to AKS.

The pipeline:
- builds the container image
- authenticates to Azure using a Service Principal
- pushes the image to Azure Container Registry (ACR)
- deploys the application to AKS

Workflow definitions are located in the .github/workflows directory.

---

## Cost Control

An Azure Budget is configured to prevent unexpected costs.

Monthly budget: 50 USD  
Alerts at: 50%, 80%, 100%  
The budget applies to all services in the subscription, including Azure OpenAI.

---

## Disclaimer

This project is for learning and experimentation purposes only.
It omits production concerns such as authentication, authorization,
rate limiting and persistent storage.

---

## Next Steps

- Document ingestion
- Retrieval-Augmented Generation (RAG)
- Vector database integration
- API authentication
