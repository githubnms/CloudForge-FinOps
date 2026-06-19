"""
Provision Service — Creates AWS infra via Terraform
JD: Infrastructure as Code, AWS, Terraform
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.terraform_runner import TerraformRunner

router = APIRouter()


class ProvisionRequest(BaseModel):
    name: str                    # e.g. "dev-01"
    region: str                  # e.g. "us-east-1"
    instance_type: str = "t3.medium"
    enable_rds: bool = False


class ProvisionResponse(BaseModel):
    status: str
    environment: str
    resources_created: list[str]
    message: str


@router.post("/", response_model=ProvisionResponse)
def provision_environment(req: ProvisionRequest):
    """
    One-click environment creation.
    Creates: VPC + EKS cluster + S3 bucket + IAM roles via Terraform.
    """
    runner = TerraformRunner()
    try:
        result = runner.apply(
            env_name=req.name,
            region=req.region,
            instance_type=req.instance_type,
            enable_rds=req.enable_rds,
        )
        return ProvisionResponse(
            status="success",
            environment=req.name,
            resources_created=result.get("resources", []),
            message=f"Environment {req.name} provisioned in {req.region}",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{env_name}")
def destroy_environment(env_name: str):
    """Tear down all resources for a given environment."""
    runner = TerraformRunner()
    runner.destroy(env_name=env_name)
    return {"status": "destroyed", "environment": env_name}