from typing import Dict, List, Optional, Union
from datetime import datetime
import numpy as np
from dataclasses import dataclass


@dataclass
class FeedbackEntry:
    feedback: str
    score: float
    context: Dict
    timestamp: datetime
    metadata: Optional[Dict] = None


class FeedbackLearner:
    def __init__(self, learning_rate: float = 0.1):
        self.learning_rate = learning_rate
        self.feedback_history: List[FeedbackEntry] = []
        self.context_weights: Dict[str, float] = {}
        self.performance_history: List[Dict] = []

    def process_feedback(
        self,
        feedback: Union[str, Dict],
        context: Dict,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """Process feedback and update learning model."""
        if isinstance(feedback, dict):
            score = feedback.get(
                'score', self._analyze_feedback(feedback['text']))
            feedback_text = feedback['text']
        else:
            score = self._analyze_feedback(feedback)
            feedback_text = feedback

        entry = FeedbackEntry(
            feedback=feedback_text,
            score=score,
            context=context,
            timestamp=datetime.now(),
            metadata=metadata
        )
        self.feedback_history.append(entry)

        # Update weights based on feedback
        self._update_weights(entry)

        # Track performance
        performance = self._evaluate_performance()
        self.performance_history.append(performance)

        return {
            "score": score,
            "performance": performance,
            "weights_updated": len(self.context_weights)
        }

    def _analyze_feedback(self, feedback: str) -> float:
        """Analyze feedback text to determine a score."""
        positive_words = {'good', 'great', 'excellent', 'perfect', 'helpful'}
        negative_words = {'bad', 'poor', 'wrong', 'unhelpful', 'incorrect'}

        words = set(feedback.lower().split())
        positive_count = len(words & positive_words)
        negative_count = len(words & negative_words)

        if positive_count == 0 and negative_count == 0:
            return 0.5

        total = positive_count + negative_count
        return positive_count / total

    def _update_weights(self, entry: FeedbackEntry) -> None:
        """Update context weights based on feedback."""
        for key, value in entry.context.items():
            if isinstance(value, (int, float, bool)):
                weight_key = f"{key}:{value}"
            else:
                weight_key = f"{key}:{type(value).__name__}"

            current_weight = self.context_weights.get(weight_key, 0.5)
            self.context_weights[weight_key] = (
                current_weight +
                self.learning_rate * (entry.score - current_weight)
            )

    def _evaluate_performance(self) -> Dict:
        """Evaluate current performance metrics."""
        recent_entries = self.feedback_history[-100:]
        if not recent_entries:
            return {"score": 0.0, "confidence": 0.0}

        scores = [entry.score for entry in recent_entries]
        return {
            "score": np.mean(scores),
            "confidence": 1.0 - np.std(scores),
            "sample_size": len(scores),
            "timestamp": datetime.now().isoformat()
        }

    def get_context_importance(self, context_key: str) -> float:
        """Get importance score for a context key."""
        relevant_weights = [
            weight for key, weight in self.context_weights.items()
            if key.startswith(f"{context_key}:")
        ]
        return np.mean(relevant_weights) if relevant_weights else 0.5
