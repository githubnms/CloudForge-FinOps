"""Tests for compliance engine"""
from compliance.policy_engine import PolicyEngine
from unittest.mock import patch


def test_s3_public_event_is_violation():
    engine = PolicyEngine()
    event = {
        "eventName": "PutBucketAcl",
        "requestParameters": {"AccessControlPolicy": {"public-read": True}},
    }
    with patch.object(engine, "_write_audit_log"):
        result = engine.evaluate_event(event)
    assert result["status"] == "FAIL"
    assert result["rule"] == "S3_PUBLIC_ACCESS"


def test_normal_event_passes():
    engine = PolicyEngine()
    event = {"eventName": "GetObject", "requestParameters": {}}
    result = engine.evaluate_event(event)
    assert result["status"] == "PASS"


def test_root_login_is_violation():
    engine = PolicyEngine()
    event = {
        "eventName": "ConsoleLogin",
        "userIdentity": {"type": "Root"},
    }
    with patch.object(engine, "_write_audit_log"):
        result = engine.evaluate_event(event)
    assert result["status"] == "FAIL"
    assert result["rule"] == "IAM_ROOT_LOGIN"