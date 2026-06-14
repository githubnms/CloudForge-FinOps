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

## Author

**[Meenakshi Sundaram]**
- BTech: [Information technology]
- LinkedIn: [[Click](https://www.linkedin.com/in/meenakshisundaram15/)]