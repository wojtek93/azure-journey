# AKS Proof of Concept

This PoC demonstrates containerized application deployment
to Azure Kubernetes Service (AKS).

## Kubernetes Deployment (AKS PoC)

- Application deployed on Azure Kubernetes Service (AKS)
- Container images stored in Azure Container Registry (ACR)
- Deployment with 2 replicas for high availability
- Rolling updates enabled (zero-downtime)
- Service exposed via LoadBalancer

### Tested scenarios
- Scaling replicas
- Rolling update (v1 → v3)
- Rollback handling
- Pod self-healing
