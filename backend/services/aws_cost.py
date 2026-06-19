"""
AWS Cost Service — Fetches spend data from Cost Explorer API
"""
import boto3
from datetime import datetime, timedelta
import os


class AWSCostService:
    def __init__(self):
        self.client = boto3.client("ce", region_name=os.getenv("AWS_REGION", "us-east-1"))

    def _date_range(self, days_back=30):
        end = datetime.utcnow().date()
        start = end - timedelta(days=days_back)
        return str(start), str(end)

    def get_monthly_summary(self) -> dict:
        start, end = self._date_range(30)
        response = self.client.get_cost_and_usage(
            TimePeriod={"Start": start, "End": end},
            Granularity="MONTHLY",
            Metrics=["BlendedCost"],
        )
        total = sum(
            float(r["Total"]["BlendedCost"]["Amount"]) for r in response["ResultsByTime"]
        )
        return {
            "total": round(total, 2),
            "by_service": self.get_cost_by_service(),
            "trend": "increasing" if total > 100 else "stable",
        }

    def get_cost_by_service(self) -> list:
        start, end = self._date_range(30)
        response = self.client.get_cost_and_usage(
            TimePeriod={"Start": start, "End": end},
            Granularity="MONTHLY",
            Metrics=["BlendedCost"],
            GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
        )
        services = []
        for result in response["ResultsByTime"]:
            for g in result["Groups"]:
                services.append({
                    "service": g["Keys"][0],
                    "cost": round(float(g["Metrics"]["BlendedCost"]["Amount"]), 2),
                })
        return sorted(services, key=lambda x: x["cost"], reverse=True)

    def detect_anomalies(self) -> list:
        try:
            r = self.client.get_anomalies(
                DateInterval={"StartDate": "2024-01-01", "EndDate": "2024-12-31"}
            )
            return [
                {
                    "service": a.get("RootCauses", [{}])[0].get("Service", "unknown"),
                    "impact": a.get("Impact", {}).get("TotalImpact", 0),
                }
                for a in r.get("Anomalies", [])
            ]
        except Exception:
            return []

    def get_forecast(self) -> dict:
        start = str(datetime.utcnow().date())
        end = str((datetime.utcnow() + timedelta(days=30)).date())
        r = self.client.get_cost_forecast(
            TimePeriod={"Start": start, "End": end},
            Metric="BLENDED_COST",
            Granularity="MONTHLY",
        )
        return {"forecast_amount": round(float(r["Total"]["Amount"]), 2), "currency": "USD"}