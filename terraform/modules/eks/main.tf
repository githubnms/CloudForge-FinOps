# EKS Module — AWS managed Kubernetes cluster
# Creates: EKS control plane, worker node group, IAM roles for both

# EKS Cluster — AWS manages the control plane for you
resource "aws_eks_cluster" "main" {
  name     = "${var.env_name}-cluster"
  role_arn = aws_iam_role.eks_cluster.arn
  version  = "1.29"

  vpc_config {
    subnet_ids              = var.subnet_ids
    endpoint_private_access = true
    endpoint_public_access  = true
  }

  # Cluster can only be created after IAM role is ready
  depends_on = [aws_iam_role_policy_attachment.eks_cluster_policy]

  tags = {
    Name = "${var.env_name}-cluster"
  }
}

# Node Group — EC2 machines where your pods actually run
resource "aws_eks_node_group" "workers" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "${var.env_name}-workers"
  node_role_arn   = aws_iam_role.eks_nodes.arn
  subnet_ids      = var.subnet_ids

  scaling_config {
    desired_size = 2 # how many nodes to run normally
    max_size     = 4 # max nodes when scaling up
    min_size     = 1 # minimum nodes always running
  }

  instance_types = [var.instance_type]

  # Nodes need all 3 IAM policies attached before they can start
  depends_on = [
    aws_iam_role_policy_attachment.eks_worker_node,
    aws_iam_role_policy_attachment.eks_cni,
    aws_iam_role_policy_attachment.ecr_readonly,
  ]

  tags = {
    Name = "${var.env_name}-workers"
  }
}

# =============================================
# IAM Role for EKS Control Plane
# This lets EKS itself talk to AWS services
# =============================================

resource "aws_iam_role" "eks_cluster" {
  name = "${var.env_name}-eks-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "eks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks_cluster.name
}

# =============================================
# IAM Role for Worker Nodes
# This lets EC2 machines join the EKS cluster
# =============================================

resource "aws_iam_role" "eks_nodes" {
  name = "${var.env_name}-eks-nodes-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

# Worker nodes need these 3 policies to function properly
resource "aws_iam_role_policy_attachment" "eks_worker_node" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.eks_nodes.name
}

resource "aws_iam_role_policy_attachment" "eks_cni" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.eks_nodes.name
}

# ECR readonly — lets nodes pull Docker images from your ECR registry
resource "aws_iam_role_policy_attachment" "ecr_readonly" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.eks_nodes.name
}