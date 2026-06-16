# Root Terraform Configuration
# This file calls all modules and wires them together

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Remote state stored in S3
  # Create this bucket manually before running terraform init
  # Command: aws s3 mb s3://cloudforge-terraform-state --region us-east-1
  backend "s3" {
    bucket         = "cloudforge-terraform-state"
    key            = "cloudforge/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "cloudforge-state-lock"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region

  # These tags get applied to every resource automatically
  default_tags {
    tags = {
      Project     = "CloudForge-FinOps"
      Environment = var.env_name
      ManagedBy   = "Terraform"
    }
  }
}

# Step 1 — Create VPC (network foundation)
module "vpc" {
  source     = "./modules/vpc"
  env_name   = var.env_name
  aws_region = var.aws_region
  cidr_block = var.vpc_cidr
}

# Step 2 — Create EKS cluster inside the VPC
# Notice: vpc_id and subnet_ids come from vpc module outputs
module "eks" {
  source        = "./modules/eks"
  env_name      = var.env_name
  vpc_id        = module.vpc.vpc_id
  subnet_ids    = module.vpc.private_subnet_ids
  instance_type = var.instance_type
}

# Step 3 — Create S3 bucket for audit logs
module "s3" {
  source   = "./modules/s3"
  env_name = var.env_name
}