from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import numpy as np
from datetime import datetime


@dataclass
class UncertaintyMetrics:
    confidence: float
    variance: float
    sample_size: int
    timestamp: datetime


class UncertaintyHandler:
    def __init__(self, confidence_threshold: float = 0.7):
        self.confidence_threshold = confidence_threshold
        self.uncertainty_history: Dict[str, List[UncertaintyMetrics]] = {}

    def evaluate_uncertainty(
        self,
        predictions: List[float],
        context: Dict
    ) -> Tuple[float, Dict]:
        """Evaluate uncertainty in predictions."""
        if not predictions:
            return 0.0, {"error": "No predictions available"}

        metrics = UncertaintyMetrics(
            confidence=np.mean(predictions),
            variance=np.var(predictions),
            sample_size=len(predictions),
            timestamp=datetime.now()
        )

        context_id = self._get_context_id(context)
        if context_id not in self.uncertainty_history:
            self.uncertainty_history[context_id] = []
        self.uncertainty_history[context_id].append(metrics)

        uncertainty_score = self._calculate_uncertainty_score(metrics)
        return uncertainty_score, self._get_uncertainty_details(metrics)

    def _calculate_uncertainty_score(
        self,
        metrics: UncertaintyMetrics
    ) -> float:
        """Calculate overall uncertainty score."""
        confidence_weight = 0.6
        variance_weight = 0.3
        sample_weight = 0.1

        confidence_score = metrics.confidence
        variance_score = 1.0 - min(metrics.variance, 1.0)
        sample_score = min(metrics.sample_size / 10.0, 1.0)

        return (confidence_score * confidence_weight +
                variance_score * variance_weight +
                sample_score * sample_weight)

    def _get_uncertainty_details(
        self,
        metrics: UncertaintyMetrics
    ) -> Dict:
        """Get detailed uncertainty metrics."""
        return {
            "confidence": metrics.confidence,
            "variance": metrics.variance,
            "sample_size": metrics.sample_size,
            "timestamp": metrics.timestamp.isoformat(),
            "is_reliable": metrics.confidence >= self.confidence_threshold
        }

    def _get_context_id(self, context: Dict) -> str:
        """Generate a unique identifier for a context."""
        relevant_keys = sorted(
            k for k in context.keys()
            if not k.startswith('_')
        )
        return ":".join(
            f"{k}={context[k]}"
            for k in relevant_keys
        )
