# S3 Module — Encrypted audit log bucket
# Compliance violations get logged here
# Versioning enabled so logs are never lost

resource "aws_s3_bucket" "audit_logs" {
  bucket = "${var.env_name}-cloudforge-audit-logs"

  tags = {
    Name    = "${var.env_name}-audit-logs"
    Purpose = "Compliance audit trail"
  }
}

# Enable versioning — every log version is kept forever
resource "aws_s3_bucket_versioning" "audit_logs" {
  bucket = aws_s3_bucket.audit_logs.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Encrypt all objects at rest using AES256
resource "aws_s3_bucket_server_side_encryption_configuration" "audit_logs" {
  bucket = aws_s3_bucket.audit_logs.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Block ALL public access — audit logs must never be public
resource "aws_s3_bucket_public_access_block" "audit_logs" {
  bucket = aws_s3_bucket.audit_logs.id

  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}