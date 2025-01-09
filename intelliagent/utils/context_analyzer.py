from typing import Dict, Optional
from datetime import datetime


class ContextAnalyzer:
    def __init__(self):
        """Initialize the context analyzer."""
        self.context_history: Dict[str, list] = {}

    def analyze(
        self,
        input_data: str,
        context: Dict,
        user_id: Optional[str] = None
    ) -> Dict:
        """Analyze input and context to provide enriched context."""
        # Track context history if user_id provided
        if user_id:
            self._track_context(user_id, context)

        # Extract key information from input
        extracted_info = self._extract_info(input_data)

        # Merge with provided context
        enriched_context = {
            **context,
            **extracted_info,
            "timestamp": datetime.now().isoformat(),
            "input_length": len(input_data),
            "context_keys": list(context.keys())
        }

        return enriched_context

    def _extract_info(self, input_data: str) -> Dict:
        """Extract key information from input text."""
        # Simple extraction for now
        words = input_data.lower().split()
        return {
            "word_count": len(words),
            "has_question": "?" in input_data,
            "sentiment": self._analyze_sentiment(words)
        }

    def _analyze_sentiment(self, words: list) -> str:
        """Basic sentiment analysis."""
        positive_words = {"good", "great", "excellent", "amazing", "wonderful"}
        negative_words = {"bad", "poor", "terrible", "awful", "horrible"}

        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)

        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        return "neutral"

    def _track_context(self, user_id: str, context: Dict) -> None:
        """Track context history for a user."""
        if user_id not in self.context_history:
            self.context_history[user_id] = []

        self.context_history[user_id].append({
            "context": context,
            "timestamp": datetime.now().isoformat()
        })

        # Keep only last 10 contexts
        self.context_history[user_id] = self.context_history[user_id][-10:]
