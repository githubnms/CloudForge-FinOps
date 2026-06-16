output "vpc_id" {
  description = "VPC ID — used by EKS and RDS modules"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "Public subnet IDs — for load balancers"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "Private subnet IDs — for EKS nodes and RDS"
  value       = aws_subnet.private[*].id
}