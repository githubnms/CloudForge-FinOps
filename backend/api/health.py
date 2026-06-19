"""
Health Service — Platform health monitoring
JD: Stability, 24/7 operation, Kubernetes operations
"""
from fastapi import APIRouter
from services.k8s_client import K8sClient

router = APIRouter()


@router.get("/")
def platform_health():
    """
    Returns health of entire platform:
    - EKS cluster status
    - Pod counts (running / pending / failed)
    - Node health
    - Recent restarts (self-healing events)
    """
    client = K8sClient()
    pods = client.get_pod_summary()
    nodes = client.get_node_health()

    return {
        "status": "healthy" if pods["failed"] == 0 else "degraded",
        "eks_clusters": 1,
        "pods_running": pods["running"],
        "pods_pending": pods["pending"],
        "pods_failed": pods["failed"],
        "nodes_ready": nodes["ready"],
        "nodes_total": nodes["total"],
        "recent_restarts": pods.get("restarts", 0),
    }


@router.get("/pods")
def pod_list(namespace: str = "default"):
    """List all pods with their current status."""
    client = K8sClient()
    return client.list_pods(namespace)


@router.post("/heal/{pod_name}")
def trigger_heal(pod_name: str, namespace: str = "default"):
    """
    Manually trigger self-healing for a specific pod.
    Deletes pod so Kubernetes automatically recreates it.
    """
    client = K8sClient()
    client.delete_pod(pod_name, namespace)
    return {"status": "healing", "pod": pod_name, "action": "pod_deleted_for_restart"}