output "cluster_name" {
  description = "EKS cluster name — used by kubectl and CD pipeline"
  value       = aws_eks_cluster.main.name
}

output "cluster_endpoint" {
  description = "EKS API server endpoint"
  value       = aws_eks_cluster.main.endpoint
}

output "cluster_ca" {
  description = "Cluster certificate authority data"
  value       = aws_eks_cluster.main.certificate_authority[0].data
}