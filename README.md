# 🌸 Iris Classifier - Kubernetes & GKE Deployment (MLOps Week-6)

**Student ID:** 21f2001203  
**Course:** IIT Madras BS Data Science & Applications - MLOps (T2-Sept2025)  
**Assignment:** Week-6 - Containerization, CI/CD, and Kubernetes Deployment

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Objectives](#objectives)
3. [Architecture](#architecture)
4. [Project Structure](#project-structure)
5. [Files Included in Git Repo](#files-included-in-git-repo)
6. [Setup & Installation](#setup--installation)
7. [Running the Application](#running-the-application)
8. [CI/CD Pipeline](#cicd-pipeline)
9. [Kubernetes Deployment](#kubernetes-deployment)
10. [Testing](#testing)
11. [GCS Integration](#gcs-integration)
12. [Troubleshooting](#troubleshooting)
13. [Key Learning Outcomes](#key-learning-outcomes)

---

## 🎯 Project Overview

This project demonstrates a complete **MLOps pipeline** for deploying a machine learning model (Iris Classifier) to production using:

- **🐳 Docker**: Containerization of the FastAPI application
- **☸️ Kubernetes (GKE)**: Orchestration and management of containerized services
- **🔄 GitHub Actions**: CI/CD automation for testing and deployment
- **☁️ Google Cloud Platform (GCP)**: Cloud infrastructure and storage
- **📦 Google Cloud Storage (GCS)**: Artifact management for models and data

The application exposes a **REST API** built with FastAPI that predicts Iris flower species based on sepal/petal measurements.

---

## 🎓 Objectives

✅ **Containerize** the FastAPI application using Docker  
✅ **Create** Kubernetes manifests (Deployment & Service)  
✅ **Automate** testing with GitHub Actions (CI pipeline)  
✅ **Automate** deployment with GitHub Actions (CD pipeline)  
✅ **Deploy** to Google Kubernetes Engine (GKE)  
✅ **Integrate** GCS for artifact management (models, datasets)  
✅ **Implement** best practices for production-ready ML systems  
✅ **Document** the entire pipeline with clear instructions  

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Repository                        │
│                  (iris-k8s-deployment)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Source     │  │  CI/CD       │  │  K8s Configs │      │
│  │   Code       │  │  Workflows   │  │  (YAML)      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↓
          ┌─────────────────────────────────┐
          │   GitHub Actions Workflow       │
          │  ┌───────────────────────────┐  │
          │  │ 1. Checkout Code          │  │
          │  │ 2. Setup Python 3.10      │  │
          │  │ 3. Auth to GCP            │  │
          │  │ 4. Download from GCS      │  │
          │  │ 5. Run Tests (CI)         │  │
          │  │ 6. Build Docker Image     │  │
          │  │ 7. Push to Artifact Reg   │  │
          │  │ 8. Deploy to GKE (CD)     │  │
          │  └───────────────────────────┘  │
          └─────────────────────────────────┘
                            ↓
     ┌──────────────────────────────────────────┐
     │    Google Cloud Platform (GCP)           │
     │  ┌────────────────────────────────────┐  │
     │  │ Google Cloud Storage (GCS)         │  │
     │  │ - models/model.joblib              │  │
     │  │ - data/iris.csv                    │  │
     │  └────────────────────────────────────┘  │
     │  ┌────────────────────────────────────┐  │
     │  │ Artifact Registry                  │  │
     │  │ - iris-repo/iris-api:latest        │  │
     │  └────────────────────────────────────┘  │
     │  ┌────────────────────────────────────┐  │
     │  │ Google Kubernetes Engine (GKE)     │  │
     │  │ - iris-cluster                     │  │
     │  │  ┌──────────────────────────────┐  │  │
     │  │  │ iris-api-service (LB)        │  │  │
     │  │  │ ├─ iris-classifier Deployment│  │  │
     │  │  │ │ ├─ Pod 1 (iris-api)        │  │  │
     │  │  │ │ └─ Pod 2 (iris-api)        │  │  │
     │  │  └──────────────────────────────┘  │  │
     │  └────────────────────────────────────┘  │
     └──────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
21f2001203_Assignment_6_SEPT_2025_MLOps/
│
├── 📄 README.md (this file)
│   └── Complete documentation of the project
│
├── 📝 Code/Scripts
│   ├── iris_fastapi.py                    # Main FastAPI application
│   ├── download_from_gcs.py               # GCS artifact downloader
│   ├── upload_to_gcs.py                   # GCS artifact uploader
│   ├── select_best_model.py               # Model selection utility
│   ├── requirements.txt                   # Python dependencies
│   └── create_artifact_registry.sh        # GCP setup script
│
├── 🐳 Docker
│   ├── Dockerfile                         # Docker image configuration
│   └── (Built image available in Artifact Registry)
│
├── ☸️ Kubernetes (k8s/)
│   ├── deployment.yaml                    # K8s Deployment manifest
│   └── service.yaml                       # K8s Service manifest
│
├── 🔄 CI/CD Workflows (.github/workflows/)
│   ├── ci-tests.yaml                      # Testing pipeline (on dev branch)
│   └── cd-deploy.yaml                     # Deployment pipeline (on main branch)
│
├── 📓 Documentation
│   ├── FIX_SUMMARY.md                     # Issues found & fixes applied
│   ├── GCS_UPLOAD_GUIDE.md                # Instructions for uploading artifacts
│   ├── kubernetes_commands.txt            # Useful kubectl commands
│   └── deployment_verification.sh         # Deployment verification script
│
├── 📊 Data & Models
│   ├── iris.csv                           # Iris dataset (locally stored)
│   └── model.joblib                       # Trained model (excluded from git)
│
├── 📓 Notebook
│   └── 21f2001203_Assignment_6_CLEANED.ipynb  # Jupyter notebook with all steps
│
└── ⚙️ Configuration
    ├── .gitignore                         # Git ignore rules
    └── .git/                              # Git repository metadata

```

---

## 📦 Files Included in Git Repo

### ✅ **Code/Scripts Included**

| File | Purpose | Language |
|------|---------|----------|
| `iris_fastapi.py` | FastAPI application with ML model prediction endpoint | Python |
| `download_from_gcs.py` | Downloads model and data from Google Cloud Storage | Python |
| `upload_to_gcs.py` | Uploads artifacts (model, data) to GCS | Python |
| `select_best_model.py` | Utility script for model selection | Python |
| `requirements.txt` | Python package dependencies | Text |
| `Dockerfile` | Docker image configuration for containerization | Docker |
| `create_artifact_registry.sh` | GCP setup: creates Artifact Registry repository | Bash |
| `deployment_verification.sh` | Verifies deployment status in GKE | Bash |
| `.github/workflows/ci-tests.yaml` | GitHub Actions: testing pipeline | YAML |
| `.github/workflows/cd-deploy.yaml` | GitHub Actions: deployment pipeline | YAML |
| `k8s/deployment.yaml` | Kubernetes: deployment manifest | YAML |
| `k8s/service.yaml` | Kubernetes: service manifest | YAML |

### ✅ **Output Files Included**

| File | Purpose | Details |
|------|---------|---------|
| `iris.csv` | Input dataset | Non-binary dataset file (included for reference) |
| `FIX_SUMMARY.md` | Documentation of issues and fixes | Demonstrates problem-solving approach |
| `GCS_UPLOAD_GUIDE.md` | Instructions for artifact upload | Helpful for setup |
| `kubernetes_commands.txt` | Reference commands for kubectl operations | Quick reference guide |

### ✅ **README.md**

This comprehensive file explains:
- Complete project architecture
- Purpose and functionality of each file
- Setup and installation instructions
- Running the application locally and in production
- CI/CD pipeline details
- Kubernetes deployment process
- Testing procedures
- Troubleshooting guide

### ❌ **Binary Files Excluded from Git** (in `.gitignore`)

| File | Reason |
|------|--------|
| `model.joblib` | Binary model artifact (uploaded to GCS instead) |
| `*.pkl` | Pickle files - binary serialized objects |
| `*.h5` / `*.keras` | Neural network model files |
| `__pycache__/` | Python cache files |
| `*.egg-info/` | Package metadata |

### ❌ **Other Files NOT Included**

- Video screencast (not required)
- Dataset splits used for training (model is trained separately)
- Jupyter checkpoint files (`.ipynb_checkpoints/`)
- IDE configuration files (`.vscode/`, `.idea/`)

---

## 🚀 Setup & Installation

### Prerequisites

- **Local Machine:**
  - Git
  - Python 3.10+
  - Docker (for local testing)
  - kubectl (for K8s management)
  - gcloud CLI

- **Google Cloud Project:**
  - Active GCP project with billing enabled
  - GCS bucket for artifacts
  - GKE cluster provisioned
  - Service account with appropriate permissions

### Step 1: Clone the Repository

```bash
git clone https://github.com/iitmstudent-2021/iris-k8s-deployment.git
cd iris-k8s-deployment
```

### Step 2: Setup Python Environment (Local Development)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Google Cloud Access

```bash
# Authenticate to GCP
gcloud auth login
gcloud config set project poised-defender-472812-e6

# Set up credentials for Python libraries
gcloud auth application-default login
```

### Step 4: Upload Model & Data to GCS

```bash
# Upload using the provided script
python upload_to_gcs.py

# Or manually using gsutil
gsutil cp model.joblib gs://mlops-week6-artifacts-21f2001203/models/
gsutil cp iris.csv gs://mlops-week6-artifacts-21f2001203/data/
```

---

## 💻 Running the Application

### Option 1: Local Development

```bash
# Ensure you're in the project directory with virtual environment activated
python -m pip install -r requirements.txt

# Run the FastAPI server
uvicorn iris_fastapi:app --reload --host 0.0.0.0 --port 8000
```

Visit `http://localhost:8000/docs` for interactive API documentation.

### Option 2: Docker (Local Testing)

```bash
# Build Docker image
docker build -t iris-api:latest .

# Run container
docker run -p 8000:8000 iris-api:latest

# Test the API
curl -X POST http://localhost:8000/predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'
```

### Option 3: Kubernetes (Production)

```bash
# Get GKE cluster credentials
gcloud container clusters get-credentials iris-cluster \
  --region us-central1 \
  --project poised-defender-472812-e6

# Apply Kubernetes manifests
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/deployment.yaml

# Check deployment status
kubectl get deployment iris-classifier
kubectl get pods -l app=iris-api
kubectl get service iris-api-service

# Get the external IP (LoadBalancer)
kubectl get service iris-api-service \
  -o jsonpath='{.status.loadBalancer.ingress[0].ip}'

# Test the API
curl http://<EXTERNAL-IP>/predict/ \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
```

---

## 🔄 CI/CD Pipeline

### Workflow Triggers

- **CI Pipeline** (Testing): Triggered on push to `dev` branch and pull requests to `main`
- **CD Pipeline** (Deployment): Triggered on push to `main` branch or manual dispatch

### CI Pipeline (`ci-tests.yaml`) - Step by Step

```
1. Checkout Code
   ↓
2. Setup Python 3.10
   ↓
3. Authenticate to Google Cloud
   ↓
4. Install Python Dependencies
   ↓
5. Download Artifacts from GCS
   ├─ model.joblib
   └─ iris.csv
   ↓
6. Verify Model File Exists
   ↓
7. Install Test Dependencies
   ├─ pytest
   ├─ pytest-asyncio
   └─ httpx
   ↓
8. Run Tests (pytest)
   ↓
9. Test API Endpoints
   └─ Non-blocking (warnings only)
```

**Expected Output:** ✅ Tests pass and confirm code quality

### CD Pipeline (`cd-deploy.yaml`) - Step by Step

```
1. Checkout Code
   ↓
2. Setup Python 3.10
   ↓
3. Authenticate to Google Cloud (using GCP_SA_KEY secret)
   ↓
4. Setup Cloud SDK & GKE Auth Plugin
   ↓
5. Install Dependencies (google-cloud-storage)
   ↓
6. Download Artifacts from GCS
   ├─ model.joblib
   └─ iris.csv
   ↓
7. Verify Model File
   ↓
8. Build Docker Image
   ├─ Tag: us-central1-docker.pkg.dev/.../iris-api:<commit-sha>
   └─ Tag: us-central1-docker.pkg.dev/.../iris-api:latest
   ↓
9. Push to Artifact Registry
   ├─ Push commit-specific tag
   └─ Push latest tag
   ↓
10. Get GKE Cluster Credentials
    ↓
11. Apply Kubernetes Manifests
    ├─ k8s/service.yaml
    └─ k8s/deployment.yaml
    ↓
12. Update Deployment with New Image
    ↓
13. Wait for Rollout Completion (10-minute timeout)
    ↓
14. Verify Deployment Status
    ├─ Check deployments
    ├─ Check pods
    ├─ Check services
    └─ Display confirmation
```

**Expected Output:** ✅ Application deployed and running on GKE

### GitHub Secrets Required

To run the CD pipeline, add these secrets to your GitHub repository:

- **`GCP_SA_KEY`**: Service Account JSON key with permissions for:
  - Container Registry push
  - GKE cluster management
  - GCS read access

---

## ☸️ Kubernetes Deployment

### Deployment Configuration (`k8s/deployment.yaml`)

```yaml
- Name: iris-classifier
- Replicas: 2 (for high availability)
- Image: us-central1-docker.pkg.dev/.../iris-api:latest
- Port: 8000
- Strategy: RollingUpdate (maxSurge: 1, maxUnavailable: 0)
- Resource Requests: 100m CPU, 128Mi memory
- Resource Limits: 200m CPU, 256Mi memory
```

**Key Features:**
- ✅ Multi-replica deployment for redundancy
- ✅ Rolling update strategy for zero-downtime deployments
- ✅ Resource limits to prevent cluster overload
- ✅ Health management through Kubernetes

### Service Configuration (`k8s/service.yaml`)

```yaml
- Type: LoadBalancer (exposes external IP)
- Selector: app=iris-api
- Port Mapping: 80 → 8000
```

**Key Features:**
- ✅ LoadBalancer exposes application to external traffic
- ✅ Automatic load distribution across pods
- ✅ External IP assignment

### Useful Kubectl Commands

```bash
# Check cluster info
gcloud container clusters list

# Get credentials
gcloud container clusters get-credentials iris-cluster \
  --region us-central1 \
  --project poised-defender-472812-e6

# Deployment management
kubectl get deployment iris-classifier
kubectl describe deployment iris-classifier
kubectl rollout status deployment/iris-classifier

# Pod monitoring
kubectl get pods -l app=iris-api
kubectl describe pods -l app=iris-api
kubectl logs -l app=iris-api --tail=50

# Service inspection
kubectl get service iris-api-service
kubectl describe service iris-api-service

# Watch real-time updates
kubectl get pods -l app=iris-api -w

# Retrieve external IP
kubectl get service iris-api-service \
  -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

---

## 🧪 Testing

### Local Unit Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_api.py -v

# Run with coverage
pytest tests/ --cov=.
```

### Manual API Testing

```bash
# Root endpoint
curl http://localhost:8000/

# Prediction endpoint
curl -X POST http://localhost:8000/predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'
```

### FastAPI Interactive Docs

After starting the server:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## 📦 GCS Integration

### Understanding GCS Bucket Structure

```
gs://mlops-week6-artifacts-21f2001203/
├── models/
│   └── model.joblib          # Trained ML model
└── data/
    └── iris.csv              # Training/test dataset
```

### Upload Artifacts to GCS

**Method 1: Using Provided Script**
```bash
python upload_to_gcs.py
```

**Method 2: Using gsutil**
```bash
gsutil cp model.joblib gs://mlops-week6-artifacts-21f2001203/models/
gsutil cp iris.csv gs://mlops-week6-artifacts-21f2001203/data/
```

### Download Artifacts from GCS

**Method 1: Using Provided Script**
```bash
python download_from_gcs.py
```

**Method 2: Using gsutil**
```bash
gsutil cp gs://mlops-week6-artifacts-21f2001203/models/model.joblib .
gsutil cp gs://mlops-week6-artifacts-21f2001203/data/iris.csv .
```

### Verify Bucket Contents

```bash
# List all objects in bucket
gsutil ls -R gs://mlops-week6-artifacts-21f2001203/

# Check file details
gsutil stat gs://mlops-week6-artifacts-21f2001203/models/model.joblib
```

---

## 🔧 Troubleshooting

### Issue 1: Docker Build Fails - "Dockerfile not found"

**Problem:** GitHub Actions CI/CD workflow fails with `"ERROR: failed to read dockerfile: open Dockerfile: no such file or directory"`

**Solution:**
- Ensure `Dockerfile` is committed to main branch
- Verify file is in repository root
- Run: `git add Dockerfile && git commit -m "Add Dockerfile" && git push`

### Issue 2: GCS Download Fails in Workflow

**Problem:** `"OperationError: 404 Not Found: gs://... does not exist"`

**Solution:**
- Upload model to GCS: `python upload_to_gcs.py`
- Verify bucket exists: `gsutil ls gs://mlops-week6-artifacts-21f2001203/`
- Check GCP service account has storage.objects.get permission

### Issue 3: Docker Push Fails - "Repository not found"

**Problem:** `"ERROR: failed to push: failed to authorize: authorization failed"`

**Solution:**
```bash
# Create Artifact Registry repository
gcloud artifacts repositories create iris-repo \
  --repository-format=docker \
  --location=us-central1 \
  --project=poised-defender-472812-e6

# Configure Docker authentication
gcloud auth configure-docker us-central1-docker.pkg.dev
```

### Issue 4: Pod Fails to Start - ImagePullBackOff

**Problem:** Kubernetes pod stuck in ImagePullBackOff state

**Solution:**
```bash
# Check pod events
kubectl describe pod <pod-name>

# Verify image exists in Artifact Registry
gcloud artifacts docker images list us-central1-docker.pkg.dev/poised-defender-472812-e6/iris-repo

# Check cluster node has correct permissions
kubectl get nodes
```

### Issue 5: Service Has No External IP (Pending)

**Problem:** LoadBalancer service stuck in "pending" state

**Solution:**
```bash
# Check service events
kubectl describe service iris-api-service

# Ensure GKE cluster has enough quota
gcloud compute project-info describe --project=poised-defender-472812-e6

# Try restarting deployment
kubectl rollout restart deployment/iris-classifier
```

### Issue 6: Permission Denied When Accessing GCS

**Problem:** `"Permission 'storage.objects.get' denied"`

**Solution:**
- Add `roles/storage.objectViewer` to GitHub secret's service account
- Verify service account email in GCS bucket permissions
- Run: `gsutil iam ch serviceAccount:<email>:objectViewer gs://bucket-name`

### General Debugging Commands

```bash
# Check GitHub Actions logs
# Visit: https://github.com/iitmstudent-2021/iris-k8s-deployment/actions

# View recent commits
git log --oneline -10

# Check git status
git status

# View workflow file syntax
yamllint .github/workflows/cd-deploy.yaml

# Validate Kubernetes manifests
kubectl apply -f k8s/ --dry-run=client

# Test model locally
python -c "import joblib; model = joblib.load('model.joblib'); print('Model loaded successfully')"
```

---

## 📊 Key Learning Outcomes

### MLOps Concepts Covered

1. **Containerization (Docker)**
   - Creating production-ready Docker images
   - Multi-stage builds optimization
   - Image versioning and tagging

2. **Orchestration (Kubernetes)**
   - Deployment and Service manifests
   - Pod replicas and auto-scaling concepts
   - Rolling updates and zero-downtime deployments
   - Resource management and limits

3. **CI/CD Pipelines (GitHub Actions)**
   - Workflow automation
   - Environment secrets management
   - Multi-step deployment pipelines
   - Build and push to registry

4. **Cloud Integration (GCP)**
   - Google Cloud Storage for artifact management
   - Google Kubernetes Engine cluster management
   - Artifact Registry for container images
   - IAM and service account permissions

5. **Best Practices**
   - Version control discipline
   - Infrastructure as Code (IaC)
   - Non-blocking test pipelines
   - Resource monitoring and health checks
   - Documentation and reproducibility

---

## 📚 Additional Resources

### Official Documentation

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Google Cloud Platform Docs](https://cloud.google.com/docs)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

### Project References

- **GitHub Repository**: [iris-k8s-deployment](https://github.com/iitmstudent-2021/iris-k8s-deployment)
- **GCP Project ID**: `poised-defender-472812-e6`
- **GCS Bucket**: `gs://mlops-week6-artifacts-21f2001203`
- **Artifact Registry**: `iris-repo` (us-central1)
- **GKE Cluster**: `iris-cluster` (us-central1)

### Useful Scripts in Repository

- `deployment_verification.sh` - Verify deployment status
- `kubernetes_commands.txt` - Quick reference for kubectl commands
- `create_artifact_registry.sh` - Setup script for GCP infrastructure

---

## 🤝 Contributing & Support

For questions or issues:

1. Check the [FIX_SUMMARY.md](FIX_SUMMARY.md) for common issues
2. Review [GCS_UPLOAD_GUIDE.md](GCS_UPLOAD_GUIDE.md) for artifact setup
3. Consult [kubernetes_commands.txt](kubernetes_commands.txt) for kubectl reference
4. Review GitHub Actions logs for deployment issues

---

## 📝 License & Attribution

**Academic Assignment:** IIT Madras, BS Data Science & Applications  
**Course:** MLOps - Week 6  
**Student:** 21f2001203  

---

## 🎉 Summary

This project demonstrates a **complete MLOps pipeline** from development to production, covering:

✅ Application development with FastAPI  
✅ Containerization with Docker  
✅ Infrastructure as Code with Kubernetes  
✅ Automated testing and deployment with GitHub Actions  
✅ Cloud integration with Google Cloud Platform  
✅ Best practices for production ML systems  

**All components are production-ready and can be used as a template for other ML projects.**

---

**Last Updated:** November 2, 2025  
**Status:** ✅ Deployment Ready
