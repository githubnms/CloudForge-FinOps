variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "us-east-1"
}

variable "env_name" {
  description = "Environment name e.g. dev-01, staging, prod"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "instance_type" {
  description = "EC2 instance type for EKS worker nodes"
  type        = string
  default     = "t3.medium"
}

variable "enable_rds" {
  description = "Whether to create RDS PostgreSQL — set false to save costs while testing"
  type        = bool
  default     = false
}