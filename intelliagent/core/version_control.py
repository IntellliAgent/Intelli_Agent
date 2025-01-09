from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import json
import os
import hashlib


@dataclass
class ModelVersion:
    version_id: str
    timestamp: datetime
    weights: Dict[str, float]
    performance_metrics: Dict
    metadata: Dict
    parent_version: Optional[str] = None


class VersionController:
    def __init__(self, storage_dir: str = "model_versions"):
        self.storage_dir = storage_dir
        self.versions: Dict[str, ModelVersion] = {}
        self.current_version: Optional[str] = None
        os.makedirs(storage_dir, exist_ok=True)
        self._load_versions()

    def create_version(
        self,
        weights: Dict[str, float],
        performance_metrics: Dict,
        metadata: Dict
    ) -> str:
        """Create a new model version."""
        # Generate version ID
        version_id = self._generate_version_id(weights)

        # Create version object
        version = ModelVersion(
            version_id=version_id,
            timestamp=datetime.now(),
            weights=weights,
            performance_metrics=performance_metrics,
            metadata=metadata,
            parent_version=self.current_version
        )

        # Save version
        self.versions[version_id] = version
        self._save_version(version)
        self.current_version = version_id

        return version_id

    def rollback(self, version_id: str) -> ModelVersion:
        """Rollback to a specific version."""
        if version_id not in self.versions:
            raise ValueError(f"Version {version_id} not found")

        self.current_version = version_id
        return self.versions[version_id]

    def get_version_history(self) -> List[Dict]:
        """Get the version history with performance metrics."""
        history = []
        current_id = self.current_version

        while current_id:
            version = self.versions[current_id]
            history.append({
                "version_id": version.version_id,
                "timestamp": version.timestamp.isoformat(),
                "performance": version.performance_metrics,
                "metadata": version.metadata
            })
            current_id = version.parent_version

        return history

    def compare_versions(
        self,
        version_id1: str,
        version_id2: str
    ) -> Dict:
        """Compare two versions."""
        if version_id1 not in self.versions:
            raise ValueError(f"Version {version_id1} not found")
        if version_id2 not in self.versions:
            raise ValueError(f"Version {version_id2} not found")

        v1 = self.versions[version_id1]
        v2 = self.versions[version_id2]

        # Compare weights
        weight_changes = {}
        all_keys = set(v1.weights.keys()) | set(v2.weights.keys())

        for key in all_keys:
            w1 = v1.weights.get(key, 0.0)
            w2 = v2.weights.get(key, 0.0)
            if w1 != w2:
                weight_changes[key] = {
                    "from": w1,
                    "to": w2,
                    "diff": w2 - w1
                }

        # Compare performance
        perf_changes = {}
        all_metrics = set(v1.performance_metrics.keys()) | set(
            v2.performance_metrics.keys()
        )

        for metric in all_metrics:
            p1 = v1.performance_metrics.get(metric, 0.0)
            p2 = v2.performance_metrics.get(metric, 0.0)
            if p1 != p2:
                perf_changes[metric] = {
                    "from": p1,
                    "to": p2,
                    "diff": p2 - p1
                }

        return {
            "weight_changes": weight_changes,
            "performance_changes": perf_changes,
            "time_difference": (
                v2.timestamp - v1.timestamp
            ).total_seconds(),
            "metadata_changes": {
                k: {"from": v1.metadata.get(k), "to": v2.metadata.get(k)}
                for k in set(v1.metadata.keys()) | set(v2.metadata.keys())
                if v1.metadata.get(k) != v2.metadata.get(k)
            }
        }

    def _generate_version_id(self, weights: Dict[str, float]) -> str:
        """Generate a unique version ID based on weights."""
        weights_str = json.dumps(weights, sort_keys=True)
        timestamp = datetime.now().isoformat()
        content = f"{weights_str}:{timestamp}"
        return hashlib.sha256(content.encode()).hexdigest()[:8]

    def _save_version(self, version: ModelVersion) -> None:
        """Save a version to disk."""
        filename = f"version_{version.version_id}.json"
        filepath = os.path.join(self.storage_dir, filename)

        with open(filepath, 'w') as f:
            json.dump({
                "version_id": version.version_id,
                "timestamp": version.timestamp.isoformat(),
                "weights": version.weights,
                "performance_metrics": version.performance_metrics,
                "metadata": version.metadata,
                "parent_version": version.parent_version
            }, f, indent=2)

    def _load_versions(self) -> None:
        """Load versions from disk."""
        for filename in os.listdir(self.storage_dir):
            if filename.startswith("version_") and filename.endswith(".json"):
                filepath = os.path.join(self.storage_dir, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    version = ModelVersion(
                        version_id=data["version_id"],
                        timestamp=datetime.fromisoformat(data["timestamp"]),
                        weights=data["weights"],
                        performance_metrics=data["performance_metrics"],
                        metadata=data["metadata"],
                        parent_version=data["parent_version"]
                    )
                    self.versions[version.version_id] = version
                    if not self.current_version:
                        self.current_version = version.version_id
