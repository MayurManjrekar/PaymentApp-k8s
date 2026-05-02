# Payment Application – Kubernetes Deployment

## Overview

This repository contains a microservices-based payment application deployed on a local Kubernetes cluster. The application consists of two services:

* **Payment Gateway** – entry point for client requests
* **Payment Processor** – internal service responsible for processing payments

The system is designed with a focus on **security, reliability, scalability, and operational readiness**, aligning with production-grade DevOps practices.

---

## Infrastructure Setup

The application is deployed on:

* **Docker Desktop (Mac)** with Kubernetes enabled
* Local Kubernetes cluster (single-node)
* Helm used for application packaging and deployment

This setup simulates a real Kubernetes environment while enabling local development and testing.

---

## Architecture

```
Client
  |
Ingress (NGINX)
  |
Payment Gateway (Service)
  |
Payment Processor (Service)
```

---

## Repository Structure

```
.
├── K8
│   ├── ingress.yaml
│   ├── namespace.yaml
│   ├── network.yaml
│   ├── payment-gateway (Helm Chart)
│   └── payment-processor (Helm Chart)
├── src
│   ├── payment-gateway
│   └── payment-processor
└── README.md
```

---

# Clarity

## Design Principles

* Separation of concerns between application code and infrastructure
* Helm-based modular deployment for reusability
* Consistent naming and labeling conventions
* Environment isolated using Kubernetes namespace (`payment`)

## Deployment Approach

* Namespace created for logical isolation
* Each service deployed using independent Helm charts
* Infrastructure components (Ingress, NetworkPolicy) managed centrally

---

# Security

## 1. Network Policies

Strict network isolation is enforced using the following policies:

### Default Deny Policy

* Blocks all ingress and egress traffic by default
* Ensures zero-trust baseline

### Internal Communication Policy

* Allows communication only between pods within the `payment` namespace
* Prevents cross-namespace access

### Ingress Access Policy

* Allows only the ingress controller to communicate with the payment gateway
* Restricts external access to a single controlled entry point

## 2. Container Security

### Non-root Execution

Dockerfile updated to run containers as a non-root user:

* Reduces privilege escalation risks
* Aligns with container security best practices

### Dockerfile Optimization

* Uses `python:3.9-slim` base image
* Combines RUN commands to reduce image layers
* Minimizes attack surface and image size

Example improvements:

* Fewer layers
* Reduced image size
* Improved security posture

### Kubernetes Security Context

* Enforces non-root execution at runtime
* Prevents privilege escalation

---

## 3. Configuration Management

* Configurations externalized using ConfigMaps
* Sensitive data can be migrated to Kubernetes Secrets for production

---

## 4. Ingress Security

* Single entry point via NGINX Ingress
* Traffic routed only to the gateway service
* Internal services are not exposed externally

---

# Operability

## Logging

* Application logs available via:

  ```
  kubectl logs <pod> -n payment
  ```

## Health Checks

* Liveness and readiness probes configured
* Ensures:

  * Faulty pods are restarted
  * Traffic is only routed to healthy pods

## Troubleshooting Guide

If issues occur:

1. Check pod status:

   ```
   kubectl get pods -n payment
   ```

2. Inspect logs:

   ```
   kubectl logs <pod> -n payment
   ```

3. Describe pod:

   ```
   kubectl describe pod <pod> -n payment
   ```

4. Verify ingress:

   ```
   kubectl describe ingress payment-ingress -n payment
   ```

5. Check services:

   ```
   kubectl get svc -n payment
   ```

---

# Reliability

## 1. Horizontal Pod Autoscaler (HPA)

* Automatically scales pods based on CPU utilization
* Ensures application can handle varying load

## 2. Pod Disruption Budget (PDB)

* Ensures minimum availability during voluntary disruptions
* Prevents all pods from going down during maintenance

## 3. Multi-replica Deployment

* Multiple pod replicas ensure high availability
* Eliminates single point of failure

## 4. Health Probes

* Liveness probe: detects failed containers
* Readiness probe: ensures only healthy pods receive traffic

---

# Scalability

* HPA dynamically adjusts pod count
* Stateless service design enables horizontal scaling
* Helm allows easy scaling via configuration changes

---

# Engineering Quality

## Helm Charts

* Separate charts for each service
* Reusable and configurable templates
* Supports incremental releases and upgrades

### Benefits

* Version-controlled deployments
* Easy rollback
* Parameterized configurations via `values.yaml`

---

# Ingress Implementation

* NGINX Ingress Controller used
* Routes external traffic to `payment-gateway`
* Path-based routing configured
* Only gateway service exposed externally

---

# Validation Steps

## Deploy Application

```
kubectl apply -f K8/namespace.yaml

helm install payment-processor ./K8/payment-processor -n payment
helm install payment-gateway ./K8/payment-gateway -n payment

kubectl apply -f K8/ingress.yaml
kubectl apply -f K8/network.yaml
```

## Test Application

```
curl -X POST http://localhost/pay \
-H "Content-Type: application/json" \
-d '{"amount":100}'
```

Expected response:

```
{"status":"processed"}
```

---

**Note:** Future Enhancements
* Enforce HTTPS by adding SSL/TLS certificates at the Ingress level
* RBAC can be enforced on the cluster to manage access & permissions
* Use Kubernetes Secrets for sensitive data instead of ConfigMaps
* Implement container image scanning (Trivy, Snyk) and use hardened base images
* Enhance observability with Node Exporter or a service mesh (Istio)
* Configure custom alerts for failures, restarts, and resource spikes
* Automate build, scan, and deployment using GitHub Actions
