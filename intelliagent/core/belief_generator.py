from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Belief:
    statement: str
    confidence: float
    evidence: List[str]
    timestamp: datetime
    source: str
    metadata: Optional[Dict] = None


class BeliefGenerator:
    def __init__(self, confidence_threshold: float = 0.7):
        """Initialize the belief generator."""
        self.confidence_threshold = confidence_threshold
        self.beliefs: List[Belief] = []

    def generate_belief(
        self,
        input_data: str,
        context: Dict,
        evidence: List[str]
    ) -> Belief:
        """Generate a new belief based on input and context."""
        confidence = self._calculate_confidence(input_data, evidence)

        belief = Belief(
            statement=input_data,
            confidence=confidence,
            evidence=evidence,
            timestamp=datetime.now(),
            source="agent",
            metadata={"context": context}
        )

        if confidence >= self.confidence_threshold:
            self.beliefs.append(belief)

        return belief

    def update_belief(
        self,
        statement: str,
        new_evidence: List[str]
    ) -> Optional[Belief]:
        """Update an existing belief with new evidence."""
        existing_belief = self._find_belief(statement)
        if not existing_belief:
            return None

        # Calculate new confidence with additional evidence
        all_evidence = existing_belief.evidence + new_evidence
        new_confidence = self._calculate_confidence(statement, all_evidence)

        updated_belief = Belief(
            statement=statement,
            confidence=new_confidence,
            evidence=all_evidence,
            timestamp=datetime.now(),
            source=existing_belief.source,
            metadata=existing_belief.metadata
        )

        # Replace old belief with updated one
        self.beliefs.remove(existing_belief)
        self.beliefs.append(updated_belief)

        return updated_belief

    def get_beliefs(
        self,
        min_confidence: Optional[float] = None
    ) -> List[Belief]:
        """Get all beliefs above specified confidence threshold."""
        if min_confidence is None:
            min_confidence = self.confidence_threshold

        return [
            belief for belief in self.beliefs
            if belief.confidence >= min_confidence
        ]

    def _find_belief(self, statement: str) -> Optional[Belief]:
        """Find an existing belief by statement."""
        for belief in self.beliefs:
            if belief.statement.lower() == statement.lower():
                return belief
        return None

    def _calculate_confidence(
        self,
        statement: str,
        evidence: List[str]
    ) -> float:
        """Calculate confidence score based on evidence."""
        if not evidence:
            return 0.0

        # Simple confidence calculation
        base_confidence = 0.5
        evidence_weight = 0.1
        max_confidence = 0.95

        confidence = base_confidence + (len(evidence) * evidence_weight)
        return min(confidence, max_confidence)
