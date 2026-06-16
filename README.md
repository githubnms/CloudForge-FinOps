# CloudForge FinOps Platform

![AWS](https://img.shields.io/badge/AWS-EKS%20%7C%20VPC%20%7C%20RDS%20%7C%20S3%20%7C%20Lambda-orange?logo=amazon-aws)
![Terraform](https://img.shields.io/badge/Terraform-Infrastructure%20as%20Code-purple?logo=terraform)
![Python](https://img.shields.io/badge/Python-FastAPI-blue?logo=python)
![Kubernetes](https://img.shields.io/badge/Kubernetes-EKS-blue?logo=kubernetes)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-black?logo=github-actions)
![Kafka](https://img.shields.io/badge/Kafka-Event%20Streaming-red?logo=apache-kafka)
![Grafana](https://img.shields.io/badge/Grafana-Observability-orange?logo=grafana)

> A self-healing, cloud-native AWS developer platform that provisions infrastructure, deploys
> services on Kubernetes, monitors health, auto-recovers failures, enforces compliance policies,
> and tracks cloud costs — built to mirror the operational model of a production bank cloud platform.

## What Is This

> CloudForge FinOps is a combined cloud developer platform and FinOps compliance engine.
> It does everything a real cloud platform team does day-to-day:

- **Provisions** complete AWS environments (VPC, EKS, RDS, S3, IAM) via Terraform in one click
- **Deploys** services to Kubernetes with zero-downtime rolling updates through a CI/CD pipeline
- **Self-heals** pod failures automatically using Kubernetes probes and Python recovery logic
- **Streams** AWS CloudTrail events through Kafka and evaluates them against compliance policies
- **Auto-remediates** violations (public S3 buckets, open security groups) using Lambda + Terraform
- **Monitors** platform health, pod status, and AWS spend via Prometheus and Grafana dashboards
- **Alerts** on-call engineers via Slack and PagerDuty when critical events occur

## Architecture

Architecture diagram is currently being finalized and will be added in a future update.

The platform is designed around a cloud-native control plane pattern with infrastructure provisioning, application deployment, observability, compliance automation, and cost governance as core capabilities.

Status: Diagram coming soon.

## Core Features

| Feature | What It Does | Tech Used |
|---|---|---|
| One-click provisioning | Creates VPC, EKS, RDS, S3, IAM via Terraform | Terraform, AWS |
| Zero-downtime deploy | Rolling update to EKS — new pod up before old goes down | Kubernetes, Docker, GitHub Actions |
| Self-healing engine | Liveness probes detect failures, pod auto-restarts, Slack notified | Kubernetes, Python |
| Compliance engine | Kafka consumes CloudTrail → OPA policy check → auto-remediation | Kafka, Python, Lambda |
| FinOps dashboard | Cost Explorer API + CloudWatch → real-time spend + anomaly alerts | boto3, Grafana, Prometheus |
| Developer portal | HTML dashboard — deploy, provision, view health with one click | HTML, FastAPI |

## Tech Stack

| Category | Technology |
|---|---|
| Cloud | AWS (EKS, VPC, RDS, S3, Lambda, ECR, CloudWatch, Cost Explorer, IAM, KMS) |
| Backend | Python 3.11, FastAPI, Pydantic |
| Infrastructure as Code | Terraform 1.6+, modular structure |
| Containers | Docker, Kubernetes (EKS), Helm |
| CI/CD | GitHub Actions (ci.yml, cd.yml, terraform.yml) |
| Event Streaming | Apache Kafka, kafka-python |
| Monitoring | Prometheus, Grafana, CloudWatch Alarms |
| Alerting | Slack Webhooks, PagerDuty Events API |
| Database | PostgreSQL (RDS), DynamoDB (state lock) |
| Security | AWS IAM least-privilege, KMS encryption, Secrets Manager |
| Testing | pytest, pytest-cov, httpx |
| Linting | flake8, black, tflint |

## Project Structure

cloudforge-finops/
│
├── frontend/                    # Developer portal UI
│   ├── index.html               # Main dashboard
│   ├── style.css                # Dark theme styling
│   └── app.js                   # FastAPI calls from browser
│
├── backend/                     # Python FastAPI platform core
│   ├── main.py                  # App entry point + router registration
│   ├── Dockerfile               # Container image
│   ├── requirements.txt         # Python dependencies
│   ├── api/
│   │   ├── provision.py         # POST /api/provision — Terraform execution
│   │   ├── deploy.py            # POST /api/deploy — EKS rolling deploy
│   │   ├── health.py            # GET /api/health — Pod + node status
│   │   ├── cost.py              # GET /api/cost — AWS Cost Explorer
│   │   └── compliance.py        # GET /api/compliance — Policy checks
│   ├── services/
│   │   ├── terraform_runner.py  # Wraps terraform CLI commands
│   │   ├── k8s_client.py        # Kubernetes Python client
│   │   ├── aws_cost.py          # Cost Explorer + anomaly detection
│   │   ├── kafka_consumer.py    # CloudTrail event streaming consumer
│   │   └── alert_service.py     # Slack + PagerDuty notifications
│   ├── compliance/
│   │   ├── policy_engine.py     # OPA-style rule evaluation engine
│   │   ├── remediation.py       # Auto-fix: S3 public access, open SGs
│   │   └── policies/            # .rego policy rule files
│   └── tests/
│       ├── test_health.py
│       └── test_compliance.py
│
├── terraform/                   # Infrastructure as Code
│   ├── main.tf                  # Root config — calls all modules
│   ├── variables.tf             # Input variables
│   ├── outputs.tf               # Cluster endpoints, bucket names
│   ├── backend.tf               # S3 remote state + DynamoDB lock
│   └── modules/
│       ├── vpc/                 # VPC, subnets, NAT gateway, IGW
│       ├── eks/                 # EKS cluster + node group + IAM roles
│       ├── rds/                 # PostgreSQL RDS in private subnet
│       ├── iam/                 # Platform IAM roles and policies
│       └── s3/                  # Encrypted audit log + app buckets
│
├── kubernetes/                  # Kubernetes manifests
│   ├── deployments/
│   │   └── backend-deploy.yaml  # RollingUpdate, liveness + readiness probes
│   ├── services/
│   │   └── backend-svc.yaml     # LoadBalancer service
│   └── configmaps/
│       └── app-config.yaml      # Environment config
│
├── monitoring/                  # Observability stack
│   ├── prometheus.yml           # Scrape config for backend + k8s pods
│   ├── grafana/
│   │   └── dashboard.json       # Cost + health Grafana dashboard
│   └── alerts/
│       └── rules.yml            # PodCrashLooping, HighCost, Compliance rules
│
├── lambda/                      # Auto-remediation functions
│   ├── remediate_iam.py         # Fix IAM root access keys
│   └── remediate_s3.py          # Block public S3 bucket access
│
├── .github/workflows/
│   ├── ci.yml                   # PR: pytest + flake8 + tflint
│   ├── cd.yml                   # Main: Docker build → ECR → EKS deploy
│   └── terraform.yml            # Infra: plan on PR, apply on main
│
├── docs/
│   ├── architecture.png         # Full architecture diagram
│   └── demo.gif                 # Screen recording of platform
│
├── docker-compose.yml           # Local dev: backend + kafka + postgres + grafana
├── Makefile                     # make run / make test / make deploy
├── .env.example                 # Environment variable template
└── .gitignore

> The repository is organized into modular domains to separate infrastructure, application services, platform operations, and observability concerns.

## What I Am Building

> CloudForge FinOps is an end-to-end cloud platform engineering project focused on combining infrastructure  automation, deployment orchestration, operational observability, compliance controls, and cost governance.

**Frontend**

- Provides a lightweight developer portal for interacting with platform capabilities including provisioning, deployment, health monitoring, and cost visibility.

**Backend**

- Acts as the platform control plane using FastAPI to expose APIs for infrastructure operations, deployment workflows, health checks, compliance execution, and cost analysis.

**Infrastructure (Terraform)**

- Defines reusable AWS infrastructure modules and enables reproducible environment provisioning through Infrastructure as Code practices.

**Kubernetes Layer**

- Manages application deployment, service exposure, configuration management, and operational resilience.

**Monitoring & Observability**

- Collects metrics, visualizes operational data, and surfaces platform health and cloud cost insights.

**Compliance Engine**

- Evaluates infrastructure activity against predefined policies and enables automated remediation workflows.

**Automation & CI/CD**

- Standardizes build, validation, infrastructure changes, and deployment pipelines to support repeatable delivery.

**Serverless Remediation**

- Executes targeted operational actions through Lambda-based remediation functions.

## Author

**[Meenakshi Sundaram]**
- BTech: [Information technology]
- LinkedIn: [[Click](https://www.linkedin.com/in/meenakshisundaram15/)]