"""Tests for health endpoints"""
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)


def test_root_returns_running():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


@patch("api.health.K8sClient")
def test_health_endpoint_structure(mock_k8s):
    mock_k8s.return_value.get_pod_summary.return_value = {
        "running": 5, "pending": 0, "failed": 0, "restarts": 2
    }
    mock_k8s.return_value.get_node_health.return_value = {"ready": 3, "total": 3}
    response = client.get("/api/health/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "pods_running" in data
    assert data["status"] == "healthy"


@patch("api.health.K8sClient")
def test_health_is_degraded_when_pods_fail(mock_k8s):
    mock_k8s.return_value.get_pod_summary.return_value = {
        "running": 3, "pending": 0, "failed": 2, "restarts": 0
    }
    mock_k8s.return_value.get_node_health.return_value = {"ready": 2, "total": 3}
    response = client.get("/api/health/")
    assert response.json()["status"] == "degraded"