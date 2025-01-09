"""Uncertainty handling and quantification system."""

from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class UncertaintyMetrics:
    """Metrics for uncertainty quantification."""
    confidence_score: float
    entropy: float
    variance: float
    prediction_spread: float


class UncertaintyHandler:
    """Handles uncertainty in decision making."""

    def __init__(self, confidence_threshold: float = 0.7):
        """Initialize the uncertainty handler.

        Args:
            confidence_threshold: Minimum confidence threshold.
        """
        self.confidence_threshold = confidence_threshold

    def evaluate_uncertainty(
        self,
        predictions: List[float],
        context: Dict
    ) -> Tuple[float, Dict]:
        """Evaluate uncertainty in predictions.

        Args:
            predictions: List of prediction probabilities.
            context: Context information.

        Returns:
            Tuple[float, Dict]: Uncertainty score and details.
        """
        if not predictions:
            return 1.0, {"error": "No predictions available"}

        metrics = self._calculate_metrics(predictions)
        uncertainty_score = self._compute_uncertainty_score(metrics)

        return uncertainty_score, {
            "metrics": {
                "confidence": metrics.confidence_score,
                "entropy": metrics.entropy,
                "variance": metrics.variance,
                "prediction_spread": metrics.prediction_spread
            },
            "context_factors": self._analyze_context_uncertainty(context),
            "threshold": self.confidence_threshold
        }

    def _calculate_metrics(self, predictions: List[float]) -> UncertaintyMetrics:
        """Calculate uncertainty metrics.

        Args:
            predictions: List of prediction probabilities.

        Returns:
            UncertaintyMetrics: Calculated metrics.
        """
        import numpy as np

        # Convert to numpy array for calculations
        preds = np.array(predictions)

        return UncertaintyMetrics(
            confidence_score=float(np.mean(preds)),
            entropy=float(-np.sum(preds * np.log2(preds + 1e-10))),
            variance=float(np.var(preds)),
            prediction_spread=float(np.max(preds) - np.min(preds))
        )

    def _compute_uncertainty_score(self, metrics: UncertaintyMetrics) -> float:
        """Compute final uncertainty score.

        Args:
            metrics: Calculated uncertainty metrics.

        Returns:
            float: Final uncertainty score.
        """
        # Weighted combination of metrics
        weights = {
            "confidence": 0.4,
            "entropy": 0.2,
            "variance": 0.2,
            "spread": 0.2
        }

        score = (
            weights["confidence"] * (1 - metrics.confidence_score) +
            weights["entropy"] * min(1.0, metrics.entropy) +
            weights["variance"] * min(1.0, metrics.variance * 2) +
            weights["spread"] * metrics.prediction_spread
        )

        return min(1.0, max(0.0, score))

    def _analyze_context_uncertainty(self, context: Dict) -> Dict:
        """Analyze uncertainty factors in context.

        Args:
            context: Context information.

        Returns:
            Dict: Context uncertainty analysis.
        """
        factors = {}

        # Check for missing or incomplete information
        if not context:
            factors["missing_context"] = 1.0
            return factors

        # Analyze specific uncertainty factors
        if "confidence" in context:
            factors["explicit_confidence"] = 1 - context["confidence"]

        if "timestamp" in context:
            # Add time-based uncertainty
            from datetime import datetime
            try:
                time_diff = datetime.now() - datetime.fromisoformat(
                    context["timestamp"]
                )
                factors["temporal_uncertainty"] = min(
                    1.0,
                    time_diff.total_seconds() / (24 * 3600)
                )  # Max 1 day
            except (ValueError, TypeError):
                factors["invalid_timestamp"] = 1.0

        return factors
