The CI/CD pipeline is implemented as a GitHub Actions workflow located in
.github/workflows/deploy-aks.yml

Deployment to AKS is automated using a GitHub Actions CI/CD pipeline
defined in the pipelines directory.

The main pipeline builds a Docker image from the application source code,
pushes it to Azure Container Registry (ACR), and deploys it to Azure
Kubernetes Service (AKS).

Pipeline flow:
- Triggered on push to main branch
- Logs in to Azure using a service principal
- Builds and pushes Docker image to ACR
- Retrieves AKS credentials
- Updates the image in an existing Kubernetes Deployment
- Performs a rolling update without downtime

This setup demonstrates a simple but complete CI/CD workflow for containerized
applications running on AKS.
