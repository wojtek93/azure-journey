# AKS Proof of Concept

This project is a simple Proof of Concept showing how a containerized web application
can be built, stored and deployed on Azure Kubernetes Service (AKS).

## Goal

The goal of this PoC is to demonstrate:
- Dockerized application
- Azure Container Registry (ACR) as a private image registry
- Deployment to Azure Kubernetes Service (AKS)
- Rolling updates and replicas in Kubernetes

## Architecture

User -> Azure LoadBalancer -> AKS Service -> Pods (Nginx container)

## Components

- Docker: Nginx-based container image
- Azure Container Registry (ACR): stores container images
- Azure Kubernetes Service (AKS): runs the application
- Kubernetes Deployment: manages replicas and updates
- Kubernetes Service (LoadBalancer): exposes the application publicly

## How it works

1. Application is built as a Docker image
2. Image is pushed to Azure Container Registry (ACR)
3. AKS pulls the image from ACR
4. Kubernetes Deployment ensures the desired number of replicas is running
5. Service of type LoadBalancer exposes the application via a public IP

## Kubernetes configuration

- Deployment with 2 replicas
- Rolling updates enabled
- Self-healing pods
- Service type: LoadBalancer

## Tested scenarios

- Scaling replicas
- Rolling update (v1 -> v3)
- Pod self-healing
- Rollback to previous version

## Tech stack

- Azure Kubernetes Service (AKS)
- Azure Container Registry (ACR)
- Docker
- Kubernetes
