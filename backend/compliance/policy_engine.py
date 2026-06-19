"""
Policy Engine — Evaluates AWS events and state against compliance rules
JD: Security, compliance, AWS best practices
"""
import boto3
import json
import uuid
import os
from datetime import datetime


class PolicyEngine:
    def __init__(self):
        self.s3 = boto3.client("s3", region_name=os.getenv("AWS_REGION", "us-east-1"))
        self.audit_bucket = os.getenv("AUDIT_BUCKET", "cloudforge-audit-logs")

    def run_all_checks(self) -> list:
        """Run all compliance checks. Returns list of PASS/FAIL results."""
        results = []
        results += self._check_s3_public_access()
        results += self._check_iam_root_usage()
        results += self._check_unencrypted_volumes()
        results += self._check_open_security_groups()
        return results

    def evaluate_event(self, event: dict) -> dict:
        """Check a single CloudTrail event against rules. Called by Kafka consumer."""
        event_name = event.get("eventName", "")

        if event_name == "PutBucketAcl":
            acl = event.get("requestParameters", {}).get("AccessControlPolicy", {})
            if "public" in str(acl).lower():
                return self._violation("S3_PUBLIC_ACCESS", event.get("requestParameters", {}))

        if event_name == "ConsoleLogin" and event.get("userIdentity", {}).get("type") == "Root":
            return self._violation("IAM_ROOT_LOGIN", event.get("userIdentity", {}))

        return {"status": "PASS", "event": event_name}

    def _violation(self, rule: str, resource: dict) -> dict:
        violation_id = str(uuid.uuid4())
        result = {
            "status": "FAIL",
            "rule": rule,
            "resource": resource,
            "violation_id": violation_id,
            "timestamp": datetime.utcnow().isoformat(),
        }
        self._write_audit_log(result)
        return result

    def _check_s3_public_access(self) -> list:
        results = []
        try:
            s3 = boto3.client("s3")
            buckets = s3.list_buckets().get("Buckets", [])
            for bucket in buckets:
                try:
                    acl = s3.get_bucket_acl(Bucket=bucket["Name"])
                    is_public = any("AllUsers" in str(g) for g in acl.get("Grants", []))
                    results.append({
                        "status": "FAIL" if is_public else "PASS",
                        "rule": "S3_PUBLIC_ACCESS",
                        "resource": bucket["Name"],
                        "severity": "HIGH",
                    })
                except Exception:
                    pass
        except Exception:
            pass
        return results

    def _check_iam_root_usage(self) -> list:
        try:
            iam = boto3.client("iam")
            summary = iam.get_account_summary()
            has_root_keys = summary.get("SummaryMap", {}).get("AccountAccessKeysPresent", 0)
            return [{
                "status": "FAIL" if has_root_keys > 0 else "PASS",
                "rule": "IAM_ROOT_ACCESS_KEYS",
                "resource": "root-account",
                "severity": "CRITICAL",
            }]
        except Exception:
            return []

    def _check_unencrypted_volumes(self) -> list:
        try:
            ec2 = boto3.client("ec2", region_name=os.getenv("AWS_REGION", "us-east-1"))
            volumes = ec2.describe_volumes().get("Volumes", [])
            return [
                {
                    "status": "FAIL" if not v.get("Encrypted") else "PASS",
                    "rule": "EBS_ENCRYPTION",
                    "resource": v["VolumeId"],
                    "severity": "MEDIUM",
                }
                for v in volumes
            ]
        except Exception:
            return []

    def _check_open_security_groups(self) -> list:
        try:
            ec2 = boto3.client("ec2", region_name=os.getenv("AWS_REGION", "us-east-1"))
            sgs = ec2.describe_security_groups().get("SecurityGroups", [])
            results = []
            for sg in sgs:
                for rule in sg.get("IpPermissions", []):
                    if any(r.get("CidrIp") == "0.0.0.0/0" for r in rule.get("IpRanges", [])):
                        results.append({
                            "status": "FAIL",
                            "rule": "OPEN_SECURITY_GROUP",
                            "resource": sg["GroupId"],
                            "severity": "HIGH",
                        })
            return results
        except Exception:
            return []

    def get_audit_log(self, limit=50) -> list:
        try:
            objs = self.s3.list_objects_v2(Bucket=self.audit_bucket, MaxKeys=limit)
            return [
                json.loads(self.s3.get_object(Bucket=self.audit_bucket, Key=o["Key"])["Body"].read())
                for o in objs.get("Contents", [])
            ]
        except Exception:
            return []

    def _write_audit_log(self, record: dict):
        key = f"audit/{record['timestamp']}-{record['violation_id']}.json"
        try:
            self.s3.put_object(Bucket=self.audit_bucket, Key=key, Body=json.dumps(record))
        except Exception:
            pass