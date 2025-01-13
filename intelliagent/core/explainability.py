"""Enhanced explainability engine with advanced analysis features."""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import math


@dataclass
class ContextFactor:
    """Represents a context factor and its influence."""
    name: str
    value: any
    influence_score: float
    confidence: float
    category: str = "general"


@dataclass
class Explanation:
    """Enhanced container for decision explanation."""
    decision_id: str
    reasoning_steps: List[str]
    evidence: Dict[str, List[str]]
    confidence: float
    metadata: Dict
    timestamp: datetime
    context_influence: Dict[str, ContextFactor]
    key_factors: List[str]  # New: Track most influential factors


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

        # Analyze context influence
        context_influence = self._analyze_context_influence(context)

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
            timestamp=datetime.now(),
            context_influence=context_influence
        )

        # Store explanation
        self.explanations[explanation.decision_id] = explanation
        return explanation

    def visualize_explanation(self, decision_id: str, format: str = 'json') -> str:
        """Enhanced visualization with multiple format options.

        Args:
            decision_id: ID of the decision.
            format: Output format ('json' or 'text').

        Returns:
            str: Formatted visualization of the explanation.
        """
        explanation = self.get_explanation(decision_id)
        if not explanation:
            return "Explanation not found."

        if format == 'json':
            return self._generate_json_visualization(explanation)
        else:
            return self._generate_text_visualization(explanation)

    def _analyze_context_influence(self, context: Dict) -> Dict[str, ContextFactor]:
        """Enhanced context influence analysis.

        Args:
            context: Context information.

        Returns:
            Dict[str, ContextFactor]: Detailed influence analysis for each factor.
        """
        influence_factors = {}
        total_weight = 0

        # Calculate initial weights based on value types and content
        for key, value in context.items():
            weight = self._calculate_factor_weight(key, value)
            total_weight += weight

            # Determine factor category
            category = self._categorize_factor(key, value)

            # Calculate confidence based on value type and content
            confidence = self._calculate_factor_confidence(value)

            influence_factors[key] = ContextFactor(
                name=key,
                value=value,
                influence_score=weight,
                confidence=confidence,
                category=category
            )

        # Normalize influence scores
        if total_weight > 0:
            for factor in influence_factors.values():
                factor.influence_score /= total_weight

        return influence_factors

    def _calculate_factor_weight(self, key: str, value: any) -> float:
        """Calculate weight for a context factor."""
        base_weight = 1.0

        # Adjust weight based on value type
        if isinstance(value, (int, float)):
            base_weight *= 1.2  # Numerical values slightly more important
        elif isinstance(value, bool):
            base_weight *= 1.1  # Boolean values slightly more important
        elif isinstance(value, dict):
            base_weight *= 1.3  # Structured data more important

        # Adjust weight based on key naming
        important_keywords = {'priority', 'critical', 'essential', 'key', 'main'}
        if any(keyword in key.lower() for keyword in important_keywords):
            base_weight *= 1.5

        return base_weight

    def _calculate_factor_confidence(self, value: any) -> float:
        """Calculate confidence score for a factor value."""
        if value is None:
            return 0.0

        if isinstance(value, (int, float)):
            return 1.0  # High confidence in numerical values
        elif isinstance(value, bool):
            return 1.0  # High confidence in boolean values
        elif isinstance(value, str):
            if not value.strip():
                return 0.0
            return min(1.0, len(value.strip()) / 100)  # Length-based confidence
        elif isinstance(value, dict):
            return min(1.0, len(value) / 5)  # Structure-based confidence
        elif isinstance(value, (list, tuple)):
            return min(1.0, len(value) / 10)  # Size-based confidence

        return 0.5  # Default confidence for other types

    def _categorize_factor(self, key: str, value: any) -> str:
        """Categorize context factors."""
        key_lower = key.lower()

        # Time-related factors
        if any(word in key_lower for word in ['time', 'date', 'duration', 'period']):
            return 'temporal'

        # Numerical factors
        if isinstance(value, (int, float)):
            return 'numerical'

        # Status/state factors
        if any(word in key_lower for word in ['status', 'state', 'condition']):
            return 'state'

        # User-related factors
        if any(word in key_lower for word in ['user', 'person', 'client']):
            return 'user'

        return 'general'

    def _generate_text_visualization(self, explanation: Explanation) -> str:
        """Generate text-based visualization."""
        lines = [
            f"Decision Explanation (ID: {explanation.decision_id})",
            f"Timestamp: {explanation.timestamp.isoformat()}",
            "\nReasoning Steps:",
        ]

        for i, step in enumerate(explanation.reasoning_steps, 1):
            lines.append(f"{i}. {step}")

        lines.extend([
            "\nKey Factors:",
            *[f"- {factor}: {explanation.context_influence[factor].influence_score:.2f}"
              for factor in explanation.key_factors],
            "\nConfidence Score:",
            f"{explanation.confidence:.2%}"
        ])

        return "\n".join(lines)

    def _generate_json_visualization(self, explanation: Explanation) -> str:
        """Generate JSON visualization."""
        return json.dumps({
            "decision": {
                "id": explanation.decision_id,
                "timestamp": explanation.timestamp.isoformat(),
                "confidence": explanation.confidence
            },
            "reasoning": {
                "steps": explanation.reasoning_steps,
                "evidence": explanation.evidence
            },
            "context": {
                "factors": {
                    name: {
                        "value": factor.value,
                        "influence": factor.influence_score,
                        "confidence": factor.confidence,
                        "category": factor.category
                    }
                    for name, factor in explanation.context_influence.items()
                },
                "key_factors": explanation.key_factors
            },
            "metadata": explanation.metadata
        }, indent=2)

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

    def compare_explanations(
        self,
        explanation_id1: str,
        explanation_id2: str
    ) -> Dict:
        """Compare two explanations and highlight differences.

        Args:
            explanation_id1: First explanation ID
            explanation_id2: Second explanation ID

        Returns:
            Dict: Comparison results
        """
        exp1 = self.get_explanation(explanation_id1)
        exp2 = self.get_explanation(explanation_id2)

        if not exp1 or not exp2:
            raise ValueError("One or both explanations not found")

        return {
            "confidence_diff": exp2.confidence - exp1.confidence,
            "context_changes": self._compare_context_factors(
                exp1.context_influence,
                exp2.context_influence
            ),
            "reasoning_changes": self._compare_reasoning_steps(
                exp1.reasoning_steps,
                exp2.reasoning_steps
            ),
            "metadata_changes": self._compare_metadata(
                exp1.metadata,
                exp2.metadata
            ),
            "timestamp_diff": (exp2.timestamp - exp1.timestamp).total_seconds()
        }

    def summarize_explanation(
        self,
        explanation_id: str,
        format: str = 'short'
    ) -> str:
        """Generate a concise summary of the explanation.

        Args:
            explanation_id: Explanation ID
            format: Summary format ('short', 'medium', 'long')

        Returns:
            str: Summarized explanation
        """
        explanation = self.get_explanation(explanation_id)
        if not explanation:
            return "Explanation not found"

        if format == 'short':
            return self._generate_short_summary(explanation)
        elif format == 'medium':
            return self._generate_medium_summary(explanation)
        else:
            return self._generate_long_summary(explanation)

    def get_historical_analysis(
        self,
        time_window: Optional[int] = None
    ) -> Dict:
        """Analyze historical decisions and their explanations.

        Args:
            time_window: Time window in seconds (None for all history)

        Returns:
            Dict: Historical analysis results
        """
        explanations = self._filter_explanations_by_time(time_window)

        return {
            "total_decisions": len(explanations),
            "average_confidence": self._calculate_average_confidence(explanations),
            "common_factors": self._identify_common_factors(explanations),
            "confidence_trend": self._analyze_confidence_trend(explanations),
            "category_distribution": self._analyze_category_distribution(explanations)
        }

    def _compare_context_factors(
        self,
        factors1: Dict[str, ContextFactor],
        factors2: Dict[str, ContextFactor]
    ) -> Dict:
        """Compare context factors between two explanations."""
        changes = {
            "added": [],
            "removed": [],
            "modified": [],
            "unchanged": []
        }

        all_keys = set(factors1.keys()) | set(factors2.keys())

        for key in all_keys:
            if key not in factors1:
                changes["added"].append({
                    "factor": key,
                    "new_value": factors2[key]
                })
            elif key not in factors2:
                changes["removed"].append({
                    "factor": key,
                    "old_value": factors1[key]
                })
            elif factors1[key] != factors2[key]:
                changes["modified"].append({
                    "factor": key,
                    "old_value": factors1[key],
                    "new_value": factors2[key],
                    "influence_change": factors2[key].influence_score - factors1[key].influence_score
                })
            else:
                changes["unchanged"].append(key)

        return changes

    def _generate_short_summary(self, explanation: Explanation) -> str:
        """Generate a short summary of the explanation."""
        key_factors = sorted(
            explanation.context_influence.items(),
            key=lambda x: x[1].influence_score,
            reverse=True
        )[:3]

        return (
            f"Decision made with {explanation.confidence:.1%} confidence. "
            f"Key factors: {
                ', '.join(f'{k} ({v.influence_score:.2f})' for k, v in key_factors)}. "
            f"Based on {len(explanation.reasoning_steps)} reasoning steps."
        )

    def _filter_explanations_by_time(
        self,
        time_window: Optional[int]
    ) -> List[Explanation]:
        """Filter explanations by time window."""
        if time_window is None:
            return list(self.explanations.values())

        cutoff_time = datetime.now() - timedelta(seconds=time_window)
        return [
            exp for exp in self.explanations.values()
            if exp.timestamp >= cutoff_time
        ]

    def _analyze_confidence_trend(
        self,
        explanations: List[Explanation]
    ) -> Dict:
        """Analyze confidence trends over time."""
        if not explanations:
            return {"trend": "no_data"}

        sorted_exps = sorted(explanations, key=lambda x: x.timestamp)
        confidences = [exp.confidence for exp in sorted_exps]

        return {
            "start": confidences[0],
            "end": confidences[-1],
            "min": min(confidences),
            "max": max(confidences),
            "trend": "increasing" if confidences[-1] > confidences[0] else "decreasing"
        }

    def _generate_medium_summary(self, explanation: Explanation) -> str:
        """Generate a medium-length summary of the explanation."""
        key_factors = sorted(
            explanation.context_influence.items(),
            key=lambda x: x[1].influence_score,
            reverse=True
        )

        # Format reasoning steps
        reasoning = "\n".join(
            f"- {step}" for step in explanation.reasoning_steps
        )

        # Format key factors with categories
        factors = "\n".join(
            f"- {k} ({v.category}): {v.influence_score:.2f} "
            f"(confidence: {v.confidence:.2f})"
            for k, v in key_factors
        )

        return (
            f"Decision Analysis\n"
            f"================\n"
            f"Confidence: {explanation.confidence:.1%}\n"
            f"Type: {explanation.metadata['decision_type']}\n\n"
            f"Key Factors:\n{factors}\n\n"
            f"Reasoning Steps:\n{reasoning}\n\n"
            f"Made at: {explanation.timestamp.isoformat()}"
        )

    def _generate_long_summary(self, explanation: Explanation) -> str:
        """Generate a detailed summary of the explanation."""
        # Start with medium summary
        summary = self._generate_medium_summary(explanation)

        # Add evidence analysis
        evidence_analysis = "\n".join(
            f"{category}:\n" + "\n".join(f"- {item}" for item in items)
            for category, items in explanation.evidence.items()
        )

        # Add context influence analysis by category
        categories = {}
        for factor in explanation.context_influence.values():
            if factor.category not in categories:
                categories[factor.category] = []
            categories[factor.category].append(factor)

        category_analysis = "\n".join(
            f"{category}:\n" + "\n".join(
                f"- {factor.name}: {factor.influence_score:.2f}"
                for factor in factors
            )
            for category, factors in categories.items()
        )

        return (
            f"{summary}\n\n"
            f"Evidence Analysis\n"
            f"================\n"
            f"{evidence_analysis}\n\n"
            f"Context Categories\n"
            f"=================\n"
            f"{category_analysis}"
        )

    def _identify_common_factors(self, explanations: List[Explanation]) -> Dict:
        """Identify common factors across explanations."""
        factor_counts = {}
        factor_influences = {}
        total_explanations = len(explanations)

        for exp in explanations:
            for factor_name, factor in exp.context_influence.items():
                if factor_name not in factor_counts:
                    factor_counts[factor_name] = 0
                    factor_influences[factor_name] = []
                factor_counts[factor_name] += 1
                factor_influences[factor_name].append(factor.influence_score)

        return {
            name: {
                "frequency": count / total_explanations,
                "avg_influence": sum(factor_influences[name]) / len(factor_influences[name]),
                "occurrences": count
            }
            for name, count in factor_counts.items()
            if count > 1  # Only include factors that appear multiple times
        }

    def _analyze_category_distribution(self, explanations: List[Explanation]) -> Dict:
        """Analyze the distribution of context factor categories."""
        category_counts = {}
        category_influences = {}

        for exp in explanations:
            for factor in exp.context_influence.values():
                if factor.category not in category_counts:
                    category_counts[factor.category] = 0
                    category_influences[factor.category] = []
                category_counts[factor.category] += 1
                category_influences[factor.category].append(factor.influence_score)

        total_factors = sum(category_counts.values())
        return {
            category: {
                "percentage": count / total_factors * 100,
                "count": count,
                "avg_influence": sum(category_influences[category]) / len(category_influences[category])
            }
            for category, count in category_counts.items()
        }

    def _calculate_average_confidence(self, explanations: List[Explanation]) -> float:
        """Calculate average confidence across explanations."""
        if not explanations:
            return 0.0
        return sum(exp.confidence for exp in explanations) / len(explanations)

    def _compare_reasoning_steps(
        self,
        steps1: List[str],
        steps2: List[str]
    ) -> Dict:
        """Compare reasoning steps between explanations."""
        return {
            "added": [step for step in steps2 if step not in steps1],
            "removed": [step for step in steps1 if step not in steps2],
            "common": [step for step in steps1 if step in steps2]
        }

    def _compare_metadata(self, metadata1: Dict, metadata2: Dict) -> Dict:
        """Compare metadata between explanations."""
        changes = {}
        all_keys = set(metadata1.keys()) | set(metadata2.keys())

        for key in all_keys:
            if key not in metadata1:
                changes[key] = {"added": metadata2[key]}
            elif key not in metadata2:
                changes[key] = {"removed": metadata1[key]}
            elif metadata1[key] != metadata2[key]:
                changes[key] = {
                    "from": metadata1[key],
                    "to": metadata2[key]
                }

        return changes
