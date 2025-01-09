"""Chain of thought reasoning implementation."""

from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import uuid


@dataclass
class Thought:
    """Represents a single thought in the chain."""
    id: str
    content: str
    confidence: float
    context: Dict
    timestamp: datetime
    previous_thought_id: Optional[str] = None


class ChainOfThought:
    """Manages chains of thoughts for reasoning."""

    def __init__(self):
        """Initialize the chain of thought manager."""
        self.thoughts: List[Thought] = []

    def add_thought(
        self,
        content: str,
        confidence: float,
        context: Dict,
        previous_thought_id: Optional[str] = None
    ) -> str:
        """Add a new thought to the chain.

        Args:
            content: The thought content.
            confidence: Confidence score for the thought.
            context: Context information.
            previous_thought_id: ID of the previous thought if any.

        Returns:
            str: ID of the new thought.
        """
        thought_id = f"thought_{uuid.uuid4().hex[:8]}"
        thought = Thought(
            id=thought_id,
            content=content,
            confidence=confidence,
            context=context,
            timestamp=datetime.now(),
            previous_thought_id=previous_thought_id
        )
        self.thoughts.append(thought)
        return thought_id

    def get_chain(self, thought_id: Optional[str] = None) -> List[Thought]:
        """Get the chain of thoughts leading to a specific thought.

        Args:
            thought_id: ID of the target thought.

        Returns:
            List[Thought]: Chain of thoughts.
        """
        if not thought_id:
            return self.thoughts

        chain = []
        current_id = thought_id

        while current_id:
            thought = self._find_thought(current_id)
            if not thought:
                break

            chain.insert(0, thought)
            current_id = thought.previous_thought_id

        return chain

    def analyze_chain(self, thought_chain: List[Thought]) -> Dict:
        """Analyze a chain of thoughts.

        Args:
            thought_chain: List of thoughts to analyze.

        Returns:
            Dict: Analysis results.
        """
        if not thought_chain:
            return {
                "length": 0,
                "average_confidence": 0.0,
                "context_evolution": {}
            }

        # Calculate metrics
        confidences = [t.confidence for t in thought_chain]
        avg_confidence = sum(confidences) / len(confidences)

        # Analyze context evolution
        context_evolution = {}
        for i, thought in enumerate(thought_chain[:-1]):
            next_thought = thought_chain[i + 1]
            changes = self._compare_contexts(thought.context, next_thought.context)
            if changes:
                context_evolution[f"step_{i+1}"] = changes

        return {
            "length": len(thought_chain),
            "average_confidence": avg_confidence,
            "context_evolution": context_evolution
        }

    def _find_thought(self, thought_id: str) -> Optional[Thought]:
        """Find a thought by its ID.

        Args:
            thought_id: ID of the thought to find.

        Returns:
            Optional[Thought]: The found thought or None.
        """
        for thought in self.thoughts:
            if thought.id == thought_id:
                return thought
        return None

    def _compare_contexts(self, context1: Dict, context2: Dict) -> Dict:
        """Compare two contexts and find differences.

        Args:
            context1: First context.
            context2: Second context.

        Returns:
            Dict: Dictionary of changes.
        """
        changes = {}
        all_keys = set(context1.keys()) | set(context2.keys())

        for key in all_keys:
            if key not in context1:
                changes[key] = {"added": context2[key]}
            elif key not in context2:
                changes[key] = {"removed": context1[key]}
            elif context1[key] != context2[key]:
                changes[key] = {
                    "from": context1[key],
                    "to": context2[key]
                }

        return changes
