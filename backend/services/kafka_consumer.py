"""
Kafka Consumer — Reads CloudTrail events, runs compliance checks
JD: event streaming, connectivity between AWS accounts
"""
from kafka import KafkaConsumer
from compliance.policy_engine import PolicyEngine
from compliance.remediation import RemediationEngine
from services.alert_service import AlertService
import json
import os
import logging

logger = logging.getLogger(__name__)


def start_consumer():
    """
    Listens to Kafka topic for CloudTrail events.
    Flow: event received -> policy check -> violation? -> auto-remediate -> Slack alert
    """
    consumer = KafkaConsumer(
        os.getenv("KAFKA_TOPIC_CLOUDTRAIL", "cloudtrail-events"),
        bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
        auto_offset_reset="latest",
        enable_auto_commit=True,
        group_id="cloudforge-compliance",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )
    policy = PolicyEngine()
    remediation = RemediationEngine()
    alert = AlertService()

    logger.info("Kafka consumer started -- listening for CloudTrail events")

    for message in consumer:
        event = message.value
        try:
            result = policy.evaluate_event(event)
            if result["status"] == "FAIL":
                logger.warning(f"Violation: {result['rule']} on {result['resource']}")
                remediation.remediate(result["violation_id"])
                alert.send_slack(
                    f"Auto-remediated: {result['rule']} on {result['resource']}",
                    level="critical",
                )
        except Exception as e:
            logger.error(f"Error processing event: {e}")