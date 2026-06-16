output "audit_bucket_name" {
  description = "S3 bucket name for audit logs"
  value       = aws_s3_bucket.audit_logs.bucket
}

output "audit_bucket_arn" {
  description = "S3 bucket ARN — used for IAM policies"
  value       = aws_s3_bucket.audit_logs.arn
}