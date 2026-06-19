"""
Deploy Service — Zero-downtime rolling deployments to EKS
JD: CI/CD, Kubernetes, SDLC, Developer Experience
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.k8s_client import K8sClient

router = APIRouter()


class DeployRequest(BaseModel):
    image: str             # Docker image e.g. "myapp:v1.2"
    service: str           # Kubernetes deployment name
    replicas: int = 2
    namespace: str = "default"


@router.post("/")
def deploy_service(req: DeployRequest):
    """
    Zero-downtime rolling deploy to EKS.
    RollingUpdate: new pods come up BEFORE old ones go down.
    """
    client = K8sClient()
    try:
        client.rolling_deploy(
            image=req.image,
            service=req.service,
            replicas=req.replicas,
            namespace=req.namespace,
        )
        return {
            "status": "deployed",
            "service": req.service,
            "image": req.image,
            "replicas": req.replicas,
            "strategy": "RollingUpdate",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{service}")
def deployment_status(service: str, namespace: str = "default"):
    """Get current rollout status for a service."""
    client = K8sClient()
    return client.get_deployment_status(service, namespace)