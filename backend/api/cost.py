"""
FinOps Cost Service — AWS cost monitoring
JD: Cloud cost, AWS — unique differentiator vs other freshers
"""
from fastapi import APIRouter
from services.aws_cost import AWSCostService

router = APIRouter()


@router.get("/")
def get_cost_summary():
    """Monthly AWS cost + anomaly detection using Cost Explorer API."""
    svc = AWSCostService()
    summary = svc.get_monthly_summary()
    anomalies = svc.detect_anomalies()
    return {
        "total_monthly": summary["total"],
        "currency": "USD",
        "breakdown": summary["by_service"],
        "anomalies_detected": len(anomalies),
        "anomalies": anomalies,
        "trend": summary["trend"],
    }


@router.get("/by-service")
def cost_by_service():
    """Cost per AWS service (EC2, EKS, RDS, S3 etc.)"""
    return AWSCostService().get_cost_by_service()


@router.get("/forecast")
def cost_forecast():
    """Predicted spend for the rest of the month."""
    return AWSCostService().get_forecast()