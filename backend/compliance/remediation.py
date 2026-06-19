"""
Remediation Engine — Auto-fixes security violations
When policy engine finds FAIL, this engine fixes it without human action
"""
import boto3
import os
import logging

logger = logging.getLogger(__name__)


class RemediationEngine:
    def __init__(self):
        self.region = os.getenv("AWS_REGION", "us-east-1")

    def remediate(self, violation_id: str, rule: str = None, resource: str = None):
        """Route to the right fix function based on rule type."""
        handlers = {
            "S3_PUBLIC_ACCESS": self._fix_s3_public_access,
            "OPEN_SECURITY_GROUP": self._fix_open_security_group,
            "EBS_ENCRYPTION": self._flag_unencrypted_volume,
        }
        handler = handlers.get(rule)
        if handler and resource:
            return handler(resource)
        return {"status": "no_handler", "rule": rule}

    def _fix_s3_public_access(self, bucket_name: str) -> dict:
        """Block ALL public access on S3 bucket automatically."""
        s3 = boto3.client("s3")
        s3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                "BlockPublicAcls": True,
                "IgnorePublicAcls": True,
                "BlockPublicPolicy": True,
                "RestrictPublicBuckets": True,
            },
        )
        logger.info(f"Fixed: S3 bucket {bucket_name} -- public access blocked")
        return {"action": "blocked_public_access", "resource": bucket_name}

    def _fix_open_security_group(self, sg_id: str) -> dict:
        """Remove 0.0.0.0/0 inbound rules from security group."""
        ec2 = boto3.client("ec2", region_name=self.region)
        sg = ec2.describe_security_groups(GroupIds=[sg_id])["SecurityGroups"][0]
        for rule in sg.get("IpPermissions", []):
            open_ranges = [r for r in rule.get("IpRanges", []) if r.get("CidrIp") == "0.0.0.0/0"]
            if open_ranges:
                rule["IpRanges"] = open_ranges
                ec2.revoke_security_group_ingress(GroupId=sg_id, IpPermissions=[rule])
        logger.info(f"Fixed: Removed open rules from security group {sg_id}")
        return {"action": "removed_open_rules", "resource": sg_id}

    def _flag_unencrypted_volume(self, volume_id: str) -> dict:
        """Can't encrypt EBS in-place -- flag for manual review."""
        logger.warning(f"Unencrypted volume {volume_id} -- manual snapshot + recreate needed")
        return {"action": "flagged_for_review", "resource": volume_id}