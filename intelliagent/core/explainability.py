"""Explainability engine for decision making process."""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Explanation:
    """Container for decision explanation."""
    decision_id: str
    reasoning_steps: List[str]
    evidence: Dict[str, List[str]]
    confidence: float
    metadata: Dict
    timestamp: datetime


class ExplainabilityEngine:
    """Handles generation and management of explanations."""

    def __init__(self):
        """Initialize the explainability engine."""
        self.explanations: Dict[str, Explanation] = {}

    def generate_explanation(
        self,
        decision: str,
        context: Dict,
        thought_chain: List[Dict],
        confidence: float
    ) -> Explanation:
        """Generate an explanation for a decision.

        Args:
            decision: The decision made.
            context: Context information.
            thought_chain: Chain of thoughts leading to decision.
            confidence: Confidence in the decision.

        Returns:
            Explanation: Generated explanation.
        """
        # Extract reasoning steps from thought chain
        reasoning_steps = [
            thought["content"]
            for thought in thought_chain
        ]

        # Collect evidence from context and thoughts
        evidence = self._collect_evidence(context, thought_chain)

        # Create explanation
        explanation = Explanation(
            decision_id=f"exp_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            reasoning_steps=reasoning_steps,
            evidence=evidence,
            confidence=confidence,
            metadata={
                "context_size": len(context),
                "chain_length": len(thought_chain),
                "decision_type": self._infer_decision_type(decision)
            },
            timestamp=datetime.now()
        )

        # Store explanation
        self.explanations[explanation.decision_id] = explanation
        return explanation

    def get_explanation(
        self,
        decision_id: str
    ) -> Optional[Explanation]:
        """Retrieve a stored explanation.

        Args:
            decision_id: ID of the decision.

        Returns:
            Optional[Explanation]: The explanation if found.
        """
        return self.explanations.get(decision_id)

    def _collect_evidence(
        self,
        context: Dict,
        thought_chain: List[Dict]
    ) -> Dict[str, List[str]]:
        """Collect evidence from context and thought chain.

        Args:
            context: Context information.
            thought_chain: Chain of thoughts.

        Returns:
            Dict[str, List[str]]: Collected evidence.
        """
        evidence = {
            "context_based": [],
            "reasoning_based": [],
            "confidence_based": []
        }

        # Context-based evidence
        for key, value in context.items():
            if isinstance(value, (str, int, float)):
                evidence["context_based"].append(f"{key}: {value}")

        # Reasoning-based evidence
        for thought in thought_chain:
            if thought.get("confidence", 0) > 0.8:
                evidence["reasoning_based"].append(thought["content"])

        # Confidence-based evidence
        confidence_values = [
            thought.get("confidence", 0)
            for thought in thought_chain
        ]
        if confidence_values:
            avg_confidence = sum(confidence_values) / len(confidence_values)
            evidence["confidence_based"].append(
                f"Average confidence: {avg_confidence:.2f}"
            )

        return evidence

    def _infer_decision_type(self, decision: str) -> str:
        """Infer the type of decision made.

        Args:
            decision: The decision text.

        Returns:
            str: Inferred decision type.
        """
        decision_lower = decision.lower()

        if any(word in decision_lower for word in ["should", "must", "need"]):
            return "recommendation"
        elif any(word in decision_lower for word in ["is", "are", "was", "were"]):
            return "classification"
        elif any(word in decision_lower for word in ["will", "going to"]):
            return "prediction"
        else:
            return "general"
