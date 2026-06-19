"""
Alert Service — Slack + PagerDuty notifications
JD: on-call rota support, 24/7 stability
"""
import requests
import os
import logging

logger = logging.getLogger(__name__)


class AlertService:
    def __init__(self):
        self.slack_webhook = os.getenv("SLACK_WEBHOOK_URL")
        self.pagerduty_key = os.getenv("PAGERDUTY_API_KEY")

    def send_slack(self, message: str, level: str = "warning"):
        """Send alert to Slack channel"""
        if not self.slack_webhook:
            logger.warning("Slack webhook not configured")
            return
        emoji = {"info": "ℹ️", "warning": "⚠️", "critical": "🚨"}.get(level, "ℹ️")
        try:
            requests.post(
                self.slack_webhook,
                json={"text": f"{emoji} *CloudForge Alert*\n{message}"},
                timeout=5,
            )
        except Exception as e:
            logger.error(f"Slack alert failed: {e}")

    def send_pagerduty(self, summary: str, severity: str = "warning"):
        """Trigger PagerDuty on-call alert for critical issues"""
        if not self.pagerduty_key:
            return
        try:
            requests.post(
                "https://events.pagerduty.com/v2/enqueue",
                json={
                    "routing_key": self.pagerduty_key,
                    "event_action": "trigger",
                    "payload": {
                        "summary": summary,
                        "severity": severity,
                        "source": "CloudForge FinOps",
                    },
                },
                timeout=5,
            )
        except Exception as e:
            logger.error(f"PagerDuty failed: {e}")