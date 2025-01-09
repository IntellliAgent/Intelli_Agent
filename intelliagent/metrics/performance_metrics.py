from typing import Dict
from datetime import datetime
import json
import os


class MetricsCollector:
    def __init__(self, metrics_dir: str = "metrics"):
        self.metrics_dir = metrics_dir
        os.makedirs(metrics_dir, exist_ok=True)
        self.current_metrics: Dict = self._initialize_metrics()

    def _initialize_metrics(self) -> Dict:
        """Initialize metrics structure."""
        return {
            "requests": 0,
            "errors": 0,
            "latencies": [],
            "cache_hits": 0,
            "cache_misses": 0,
            "model_usage": {},
            "domain_stats": {},
            "timestamp": datetime.now().isoformat()
        }

    def record_request(
        self,
        latency: float,
        model: str,
        domain: str,
        cache_hit: bool,
        error: bool = False
    ) -> None:
        """Record metrics for a request."""
        self.current_metrics["requests"] += 1
        self.current_metrics["latencies"].append(latency)

        if error:
            self.current_metrics["errors"] += 1

        if cache_hit:
            self.current_metrics["cache_hits"] += 1
        else:
            self.current_metrics["cache_misses"] += 1

        # Update model usage
        self.current_metrics["model_usage"][model] = (
            self.current_metrics["model_usage"].get(model, 0) + 1
        )

        # Update domain stats
        if domain not in self.current_metrics["domain_stats"]:
            self.current_metrics["domain_stats"][domain] = {
                "requests": 0,
                "errors": 0
            }
        self.current_metrics["domain_stats"][domain]["requests"] += 1
        if error:
            self.current_metrics["domain_stats"][domain]["errors"] += 1

    def save_metrics(self) -> None:
        """Save current metrics to disk."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"metrics_{timestamp}.json"
        filepath = os.path.join(self.metrics_dir, filename)

        with open(filepath, 'w') as f:
            json.dump(self.current_metrics, f, indent=2)
