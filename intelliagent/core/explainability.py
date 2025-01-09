from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Explanation:
    decision: str
    reasoning: List[str]
    factors: Dict[str, float]
    timestamp: datetime
    context: Dict


class ExplainabilityEngine:
    def __init__(self):
        self.explanations: List[Explanation] = []

    def explain_decision(
        self,
        decision: str,
        context: Dict,
        model_weights: Dict[str, float]
    ) -> Explanation:
        """Generate an explanation for a decision."""
        # Extract key factors that influenced the decision
        factors = self._extract_key_factors(context, model_weights)

        # Generate reasoning steps
        reasoning = self._generate_reasoning(decision, factors, context)

        # Create explanation
        explanation = Explanation(
            decision=decision,
            reasoning=reasoning,
            factors=factors,
            timestamp=datetime.now(),
            context=context
        )

        self.explanations.append(explanation)
        return explanation

    def _extract_key_factors(
        self,
        context: Dict,
        weights: Dict[str, float]
    ) -> Dict[str, float]:
        """Extract key factors that influenced the decision."""
        factors = {}

        for key, value in context.items():
            weight_key = f"{key}:{value}"
            if weight_key in weights:
                factors[key] = weights[weight_key]
            elif key in weights:
                factors[key] = weights[key]

        # Normalize factor weights
        total_weight = sum(factors.values())
        if total_weight > 0:
            factors = {
                k: v/total_weight
                for k, v in factors.items()
            }

        return dict(
            sorted(
                factors.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]  # Top 5 factors
        )

    def _generate_reasoning(
        self,
        decision: str,
        factors: Dict[str, float],
        context: Dict
    ) -> List[str]:
        """Generate step-by-step reasoning for the decision."""
        reasoning = []

        # Add decision statement
        reasoning.append(f"Final decision: {decision}")

        # Add factor explanations
        for factor, weight in factors.items():
            value = context.get(factor, "N/A")
            reasoning.append(
                f"Factor '{factor}' (importance: {weight:.2f}) "
                f"with value '{value}' influenced this decision."
            )

        # Add confidence statement
        total_weight = sum(factors.values())
        reasoning.append(
            f"Overall confidence in this decision: {total_weight:.2f}"
        )

        return reasoning

    def get_similar_decisions(
        self,
        context: Dict,
        limit: int = 5
    ) -> List[Explanation]:
        """Find similar past decisions based on context."""
        if not self.explanations:
            return []

        scored_explanations = [
            (self._calculate_similarity(e.context, context), e)
            for e in self.explanations
        ]

        return [
            e for _, e in sorted(
                scored_explanations,
                key=lambda x: x[0],
                reverse=True
            )[:limit]
        ]

    def _calculate_similarity(
        self,
        context1: Dict,
        context2: Dict
    ) -> float:
        """Calculate similarity score between two contexts."""
        common_keys = set(context1.keys()) & set(context2.keys())
        if not common_keys:
            return 0.0

        similarity = sum(
            1.0 if context1[k] == context2[k] else 0.0
            for k in common_keys
        )

        return similarity / len(common_keys)
