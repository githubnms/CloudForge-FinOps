variable "env_name" {
  description = "Environment name e.g. dev-01"
  type        = string
}

variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "cidr_block" {
  description = "VPC CIDR block"
  type        = string
}