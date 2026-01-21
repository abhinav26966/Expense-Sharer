# Daily Expense Sharing Application

[![CI Pipeline](https://github.com/abhinavnagar2696/Expense-Sharer/actions/workflows/ci.yml/badge.svg)](https://github.com/abhinavnagar2696/Expense-Sharer/actions/workflows/ci.yml)
[![CD Pipeline](https://github.com/abhinavnagar2696/Expense-Sharer/actions/workflows/cd.yml/badge.svg)](https://github.com/abhinavnagar2696/Expense-Sharer/actions/workflows/cd.yml)

A production-ready expense sharing application built with Flask, featuring a complete CI/CD pipeline implementing DevSecOps best practices.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [CI/CD Pipeline](#cicd-pipeline)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [Security](#security)
- [Deployment](#deployment)
- [Project Structure](#project-structure)

---

## Overview

The Daily Expense Sharing App simplifies splitting expenses among friends, colleagues, or family. Whether it's a weekend getaway, dinner with friends, or shared utilities—this app handles fair expense distribution through multiple splitting methods.

## Features

### Application Features
- **User Management** - Create and manage users with email, name, and mobile number
- **Expense Tracking** - Record and track expenses with detailed descriptions
- **Multiple Split Methods**:
  - **Equal Split**: Divide amount equally among participants
  - **Exact Split**: Specify exact amounts for each participant
  - **Percentage Split**: Allocate based on percentages (must sum to 100%)
- **Balance Sheet** - Generate detailed breakdown of individual and group expenses
- **Data Validation** - Smart validation ensuring consistency

### DevOps Features
- Automated CI/CD pipeline with GitHub Actions
- Container security scanning (Trivy)
- Static Application Security Testing (CodeQL)
- Software Composition Analysis (Safety, Bandit)
- Kubernetes deployment with auto-scaling
- Dynamic Application Security Testing (OWASP ZAP)

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3.11, Flask 3.0 |
| Database | SQLite (SQLAlchemy ORM) |
| Web Server | Gunicorn |
| Containerization | Docker |
| Orchestration | Kubernetes |
| CI/CD | GitHub Actions |
| Security Scanning | CodeQL, Trivy, Bandit, Safety |

---

## CI/CD Pipeline

### Pipeline Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   COMMIT    │────▶│  CI PIPELINE │────▶│ CD PIPELINE │
└─────────────┘     └─────────────┘     └─────────────┘
                           │                    │
                    ┌──────┴──────┐      ┌──────┴──────┐
                    ▼             ▼      ▼             ▼
               ┌────────┐   ┌────────┐ ┌────────┐ ┌────────┐
               │  Lint  │   │  SAST  │ │ Deploy │ │  DAST  │
               └────────┘   └────────┘ └────────┘ └────────┘
                    │             │          │          │
               ┌────────┐   ┌────────┐ ┌────────┐ ┌────────┐
               │  Test  │   │  SCA   │ │ Verify │ │Rollback│
               └────────┘   └────────┘ └────────┘ └────────┘
                    │             │
               ┌────────┐   ┌────────┐
               │ Build  │   │  Scan  │
               └────────┘   └────────┘
                    │             │
               ┌────────┐   ┌────────┐
               │Runtime │   │  Push  │
               │  Test  │   │        │
               └────────┘   └────────┘
```

### CI Pipeline Stages

| Stage | Tool | Purpose | Why It Matters |
|-------|------|---------|----------------|
| **Linting** | Flake8 | Code style enforcement | Prevents technical debt, ensures maintainability |
| **SAST** | CodeQL | Static security analysis | Detects OWASP Top 10 vulnerabilities in code |
| **SCA** | Safety, Bandit | Dependency scanning | Identifies supply chain risks |
| **Unit Tests** | Pytest | Functionality validation | Prevents regressions, validates business logic |
| **Docker Build** | Docker | Containerization | Consistent deployment artifact |
| **Image Scan** | Trivy | Container vulnerability scan | Prevents vulnerable images from shipping |
| **Runtime Test** | Smoke tests | Container validation | Ensures image is runnable |
| **Registry Push** | DockerHub | Image publishing | Enables downstream deployment |

### CD Pipeline Stages

| Stage | Purpose | Why It Matters |
|-------|---------|----------------|
| **Deploy** | Apply K8s manifests | Automated, consistent deployments |
| **Verify** | Validate deployment | Early detection of deployment issues |
| **DAST** | Runtime security testing | Finds vulnerabilities in running app |
| **Rollback** | Recovery mechanism | Minimizes downtime on failures |

---

## Getting Started

### Prerequisites

- Python 3.11+
- Docker
- Git

### Running Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/abhinavnagar2696/Expense-Sharer.git
   cd Expense-Sharer
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Access the app**
   ```
   http://localhost:5000
   ```

### Running with Docker

```bash
# Build the image
docker build -t expense-sharer .

# Run the container
docker run -d -p 5000:5000 \
  -e SECRET_KEY=your-secret-key \
  -e FLASK_ENV=production \
  expense-sharer
```

### Running Tests

```bash
# Run all tests with coverage
pytest tests/ -v --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/test_app.py -v
```

---

## API Documentation

### User Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/` | Create a new user |
| GET | `/users/<id>` | Get user by ID |
| GET | `/users/` | List all users |
| GET | `/users/<id>/expenses` | Get user's expenses |

### Expense Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/expenses` | Create new expense |
| GET | `/expenses` | List all expenses |
| GET | `/balance-sheet` | Get balance sheet |

### Example Requests

**Create User**
```bash
curl -X POST http://localhost:5000/users/ \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "name": "John Doe", "mobile": "1234567890"}'
```

**Add Expense (Equal Split)**
```bash
curl -X POST http://localhost:5000/expenses \
  -H "Content-Type: application/json" \
  -d '{
    "payer_id": 1,
    "amount": 300,
    "description": "Dinner",
    "split_method": "equal",
    "participants": [1, 2, 3]
  }'
```

---

## Security

### Security Measures Implemented

1. **Static Analysis (SAST)**
   - CodeQL for security vulnerability detection
   - Bandit for Python-specific security issues

2. **Dependency Scanning (SCA)**
   - Safety for known vulnerability detection
   - Automated on every PR/push

3. **Container Security**
   - Trivy vulnerability scanner
   - Non-root container execution
   - Minimal base image (Python slim)

4. **Runtime Security (DAST)**
   - OWASP ZAP baseline scanning
   - Custom security tests

5. **Infrastructure Security**
   - Kubernetes RBAC
   - Network policies
   - Secret management via GitHub Secrets

### Secrets Configuration

Configure the following GitHub Secrets for the pipeline:

| Secret Name | Purpose |
|-------------|---------|
| `DOCKERHUB_USERNAME` | DockerHub registry username |
| `DOCKERHUB_TOKEN` | DockerHub access token |
| `KUBE_CONFIG` | Base64-encoded kubeconfig |
| `APP_SECRET_KEY` | Application secret key |

**How to set secrets:**
```bash
# Encode kubeconfig
cat ~/.kube/config | base64 | pbcopy  # macOS
cat ~/.kube/config | base64 -w 0      # Linux

# Then paste in GitHub: Settings > Secrets and variables > Actions
```

---

## Deployment

### Kubernetes Deployment

```bash
# Apply all manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/hpa.yaml

# Check status
kubectl get all -n expense-sharer
```

### Local Kubernetes (Minikube/Kind)

```bash
# Start cluster
minikube start

# Enable ingress
minikube addons enable ingress

# Build image in minikube
eval $(minikube docker-env)
docker build -t expense-sharer:latest .

# Deploy
kubectl apply -f k8s/
```

---

## Project Structure

```
expense-sharer/
├── .github/
│   └── workflows/
│       ├── ci.yml           # CI pipeline
│       └── cd.yml           # CD pipeline
├── app/
│   ├── __init__.py          # Application factory
│   ├── models.py            # Database models
│   ├── routes.py            # API endpoints
│   └── utils.py             # Utility functions
├── k8s/
│   ├── namespace.yaml       # Kubernetes namespace
│   ├── configmap.yaml       # Configuration
│   ├── secret.yaml          # Secrets (example)
│   ├── deployment.yaml      # Deployment spec
│   ├── service.yaml         # Service definition
│   ├── ingress.yaml         # Ingress rules
│   └── hpa.yaml             # Horizontal Pod Autoscaler
├── tests/
│   ├── __init__.py
│   └── test_app.py          # Unit tests
├── .env.example             # Environment template
├── config.py                # Configuration classes
├── Dockerfile               # Container definition
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── README.md                # This file
```

---

## Expense Calculation Examples

### Equal Split
- **Scenario**: Dinner with 3 friends, total bill ₹3000
- **Result**: Each person owes ₹1000

### Exact Split
- **Scenario**: Shopping with 2 friends, total ₹4299
- **Result**: Friend 1 owes ₹799, Friend 2 owes ₹2000, You owe ₹1500

### Percentage Split
- **Scenario**: Party expenses ₹10,000
- **Result**: You (50%) = ₹5000, Friend 1 (30%) = ₹3000, Friend 2 (20%) = ₹2000

---

## Future Enhancements

- [ ] User Authentication & Authorization
- [ ] Enhanced Error Handling
- [ ] Performance Optimization for large datasets
- [ ] Integration Tests
- [ ] Prometheus metrics endpoint
- [ ] Helm chart for Kubernetes deployment

---

## License

This project is part of the Scaler DevOps Assessment.

## Author

**Abhinav Nagar**  
Scaler Student ID: [Your Student ID]
