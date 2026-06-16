variable "env_name" {
  description = "Environment name e.g. dev-01"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID from VPC module output"
  type        = string
}

variable "subnet_ids" {
  description = "Private subnet IDs from VPC module output"
  type        = list(string)
}

variable "instance_type" {
  description = "EC2 instance type for worker nodes"
  type        = string
}