from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import json
import os
import shutil


@dataclass
class DeploymentConfig:
    model_id: str
    version: str
    environment: str
    resources: Dict
    metadata: Dict


class ModelDeployer:
    def __init__(self, deployment_dir: str = "deployments"):
        self.deployment_dir = deployment_dir
        self.active_deployments: Dict[str, DeploymentConfig] = {}
        os.makedirs(deployment_dir, exist_ok=True)

    def deploy_model(
        self,
        model_id: str,
        version: str,
        environment: str,
        resources: Optional[Dict] = None,
        metadata: Optional[Dict] = None
    ) -> str:
        """Deploy a model version to an environment."""
        deployment_id = f"{model_id}-{version}-{environment}"

        config = DeploymentConfig(
            model_id=model_id,
            version=version,
            environment=environment,
            resources=resources or {},
            metadata=metadata or {}
        )

        # Save deployment configuration
        self._save_deployment(deployment_id, config)

        # Update active deployments
        self.active_deployments[deployment_id] = config

        return deployment_id

    def rollback_deployment(
        self,
        deployment_id: str,
        target_version: str
    ) -> str:
        """Rollback a deployment to a specific version."""
        if deployment_id not in self.active_deployments:
            raise ValueError(f"Deployment {deployment_id} not found")

        current_config = self.active_deployments[deployment_id]

        # Create new deployment with target version
        new_deployment_id = self.deploy_model(
            model_id=current_config.model_id,
            version=target_version,
            environment=current_config.environment,
            resources=current_config.resources,
            metadata={
                **current_config.metadata,
                "rollback_from": current_config.version,
                "rollback_timestamp": datetime.now().isoformat()
            }
        )

        # Archive old deployment
        self._archive_deployment(deployment_id)

        return new_deployment_id

    def get_deployment_status(self, deployment_id: str) -> Dict:
        """Get status of a deployment."""
        if deployment_id not in self.active_deployments:
            raise ValueError(f"Deployment {deployment_id} not found")

        config = self.active_deployments[deployment_id]
        deployment_path = os.path.join(self.deployment_dir, deployment_id)

        return {
            "deployment_id": deployment_id,
            "model_id": config.model_id,
            "version": config.version,
            "environment": config.environment,
            "resources": config.resources,
            "metadata": config.metadata,
            "status": "active" if os.path.exists(deployment_path) else "archived"
        }

    def _save_deployment(
        self,
        deployment_id: str,
        config: DeploymentConfig
    ) -> None:
        """Save deployment configuration to disk."""
        deployment_path = os.path.join(self.deployment_dir, deployment_id)
        os.makedirs(deployment_path, exist_ok=True)

        config_path = os.path.join(deployment_path, "config.json")
        with open(config_path, 'w') as f:
            json.dump({
                "model_id": config.model_id,
                "version": config.version,
                "environment": config.environment,
                "resources": config.resources,
                "metadata": config.metadata,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)

    def _archive_deployment(self, deployment_id: str) -> None:
        """Archive a deployment."""
        deployment_path = os.path.join(self.deployment_dir, deployment_id)
        archive_path = os.path.join(
            self.deployment_dir,
            "archive",
            f"{deployment_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )

        if os.path.exists(deployment_path):
            os.makedirs(os.path.dirname(archive_path), exist_ok=True)
            shutil.move(deployment_path, archive_path)

        self.active_deployments.pop(deployment_id, None)
