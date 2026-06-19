"""
Kubernetes Client — Manages EKS cluster operations
"""
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException


class K8sClient:
    def __init__(self):
        try:
            config.load_incluster_config()   # when running inside EKS pod
        except Exception:
            config.load_kube_config()        # when running locally
        self.apps_v1 = client.AppsV1Api()
        self.core_v1 = client.CoreV1Api()

    def rolling_deploy(self, image, service, replicas, namespace):
        """Update image — triggers zero-downtime rolling update automatically"""
        try:
            d = self.apps_v1.read_namespaced_deployment(service, namespace)
            d.spec.replicas = replicas
            d.spec.template.spec.containers[0].image = image
            self.apps_v1.patch_namespaced_deployment(service, namespace, d)
        except ApiException as e:
            raise RuntimeError(f"K8s deploy failed: {e.reason}")

    def get_pod_summary(self) -> dict:
        pods = self.core_v1.list_pod_for_all_namespaces()
        s = {"running": 0, "pending": 0, "failed": 0, "restarts": 0}
        for pod in pods.items:
            phase = pod.status.phase or "Unknown"
            if phase == "Running":
                s["running"] += 1
            elif phase == "Pending":
                s["pending"] += 1
            elif phase in ("Failed", "Unknown"):
                s["failed"] += 1
            if pod.status.container_statuses:
                for cs in pod.status.container_statuses:
                    s["restarts"] += cs.restart_count
        return s

    def get_node_health(self) -> dict:
        nodes = self.core_v1.list_node()
        ready = sum(
            1 for n in nodes.items for c in n.status.conditions
            if c.type == "Ready" and c.status == "True"
        )
        return {"ready": ready, "total": len(nodes.items)}

    def list_pods(self, namespace) -> list:
        pods = self.core_v1.list_namespaced_pod(namespace)
        return [{"name": p.metadata.name, "status": p.status.phase} for p in pods.items]

    def delete_pod(self, pod_name, namespace):
        """Delete pod to trigger self-healing restart by Kubernetes"""
        self.core_v1.delete_namespaced_pod(pod_name, namespace)

    def get_deployment_status(self, service, namespace) -> dict:
        d = self.apps_v1.read_namespaced_deployment(service, namespace)
        return {
            "service": service,
            "desired": d.spec.replicas,
            "ready": d.status.ready_replicas or 0,
        }