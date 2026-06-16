# VPC Module — Your private network inside AWS
# Creates: VPC, 2 public subnets, 2 private subnets, NAT gateway, Internet Gateway, Route tables

resource "aws_vpc" "main" {
  cidr_block           = var.cidr_block
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "${var.env_name}-vpc"
  }
}

# Internet Gateway — allows public subnets to reach internet
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.env_name}-igw"
  }
}

# Public subnets — faces internet, used for load balancers
# count = 2 means this creates 2 subnets automatically
resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(var.cidr_block, 4, count.index)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name                     = "${var.env_name}-public-${count.index + 1}"
    "kubernetes.io/role/elb" = "1"
  }
}

# Private subnets — internal only, EKS nodes and RDS live here
resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.cidr_block, 4, count.index + 4)
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name                              = "${var.env_name}-private-${count.index + 1}"
    "kubernetes.io/role/internal-elb" = "1"
  }
}

# Elastic IP for NAT gateway — NAT needs a fixed public IP
resource "aws_eip" "nat" {
  domain = "vpc"
}

# NAT Gateway — lets private subnet reach internet for updates
# Lives in public subnet but serves private subnet
resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public[0].id

  tags = {
    Name = "${var.env_name}-nat"
  }

  # NAT gateway needs IGW to exist first
  depends_on = [aws_internet_gateway.igw]
}

# Route table for public subnets — sends all traffic to internet via IGW
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "${var.env_name}-public-rt"
  }
}

# Route table for private subnets — sends all traffic to internet via NAT
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat.id
  }

  tags = {
    Name = "${var.env_name}-private-rt"
  }
}

# Connect public subnets to public route table
resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# Connect private subnets to private route table
resource "aws_route_table_association" "private" {
  count          = 2
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private.id
}

# Get list of available AZs in the region automatically
data "aws_availability_zones" "available" {
  state = "available"
}