from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Thought:
    content: str
    confidence: float
    timestamp: datetime
    context: Dict
    previous_thought_id: Optional[str] = None


class ChainOfThought:
    def __init__(self):
        self.thoughts: List[Thought] = []
        self.current_chain: List[str] = []

    def add_thought(
        self,
        content: str,
        confidence: float,
        context: Dict,
        previous_thought_id: Optional[str] = None
    ) -> str:
        """Add a new thought to the chain."""
        thought = Thought(
            content=content,
            confidence=confidence,
            timestamp=datetime.now(),
            context=context,
            previous_thought_id=previous_thought_id
        )

        thought_id = f"thought_{len(self.thoughts)}"
        self.thoughts.append(thought)

        if previous_thought_id:
            self._update_chain(thought_id, previous_thought_id)
        else:
            self.current_chain = [thought_id]

        return thought_id

    def _update_chain(self, new_thought_id: str, previous_id: str) -> None:
        """Update the current chain of thoughts."""
        if previous_id in self.current_chain:
            idx = self.current_chain.index(previous_id)
            self.current_chain = self.current_chain[:idx +
                                                    1] + [new_thought_id]
        else:
            self.current_chain = [new_thought_id]

    def get_chain(self, thought_id: Optional[str] = None) -> List[Thought]:
        """Get the chain of thoughts leading to a specific thought."""
        if not thought_id:
            return [self.thoughts[int(tid.split('_')[1])]
                    for tid in self.current_chain]

        chain = []
        current_id = thought_id

        while current_id:
            thought = self.thoughts[int(current_id.split('_')[1])]
            chain.insert(0, thought)
            current_id = thought.previous_thought_id

        return chain

    def analyze_chain(self, chain: List[Thought]) -> Dict:
        """Analyze a chain of thoughts."""
        return {
            "length": len(chain),
            "average_confidence": sum(t.confidence for t in chain) / len(chain),
            "time_span": (chain[-1].timestamp - chain[0].timestamp).total_seconds(),
            "context_evolution": self._analyze_context_evolution(chain)
        }

    def _analyze_context_evolution(self, chain: List[Thought]) -> Dict:
        """Analyze how context evolved through the chain."""
        if not chain:
            return {}

        context_changes = {}
        base_context = chain[0].context

        for thought in chain[1:]:
            changes = {}
            for key, value in thought.context.items():
                if key not in base_context or base_context[key] != value:
                    changes[key] = {
                        "from": base_context.get(key, None),
                        "to": value
                    }
            if changes:
                context_changes[thought.timestamp.isoformat()] = changes

        return context_changes
