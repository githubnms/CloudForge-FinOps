"""
Terraform Runner — Executes Terraform CLI commands from Python
Wraps terraform init / apply / destroy
"""
import subprocess

class TerraformRunner:
    def __init__(self, working_dir: str = "../terraform"):
        self.working_dir = working_dir

    def _run(self, *args) -> dict:
        cmd = ["terraform"] + list(args)
        result = subprocess.run(
            cmd, cwd=self.working_dir, capture_output=True, text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"Terraform error: {result.stderr}")
        return {"stdout": result.stdout}

    def init(self):
        return self._run("init", "-no-color")

    def apply(self, env_name, region, instance_type, enable_rds):
        self.init()
        result = self._run(
            "apply", "-auto-approve",
            f"-var=env_name={env_name}",
            f"-var=aws_region={region}",
            f"-var=instance_type={instance_type}",
            f"-var=enable_rds={'true' if enable_rds else 'false'}",
            "-no-color",
        )
        resources = [
            line.strip() for line in result["stdout"].split("\n")
            if "created" in line.lower()
        ]
        return {"resources": resources}

    def destroy(self, env_name):
        return self._run(
            "destroy", "-auto-approve",
            f"-var=env_name={env_name}",
            "-no-color",
        )