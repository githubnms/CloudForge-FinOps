"""
Compliance Engine API — Policy enforcement and auto-remediation
JD: Security, compliance, AWS best practices
Most fresher projects don't have this — this is what makes you stand out
"""
from fastapi import APIRouter
from compliance.policy_engine import PolicyEngine
from compliance.remediation import RemediationEngine

router = APIRouter()


@router.get("/")
def compliance_status():
    """
    Runs all policy checks against current AWS state.
    Returns violations and whether auto-remediation was triggered.
    """
    engine = PolicyEngine()
    results = engine.run_all_checks()
    violations = [r for r in results if r["status"] == "FAIL"]
    return {
        "total_checks": len(results),
        "passed": len(results) - len(violations),
        "violations_count": len(violations),
        "violations": violations,
        "auto_remediation_enabled": True,
    }


@router.post("/remediate/{violation_id}")
def trigger_remediation(violation_id: str):
    """Manually trigger remediation for a specific violation."""
    engine = RemediationEngine()
    result = engine.remediate(violation_id)
    return {"status": "remediated", "violation_id": violation_id, "result": result}


@router.get("/audit-log")
def get_audit_log(limit: int = 50):
    """Returns audit trail from S3 — all compliance events logged here."""
    return PolicyEngine().get_audit_log(limit=limit)