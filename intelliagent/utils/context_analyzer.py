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
        self.sentiment_keywords = {
            'positive': ['good', 'great', 'excellent', 'happy', 'profit', 'gain'],
            'negative': ['bad', 'poor', 'terrible', 'unhappy', 'loss', 'decline'],
            'neutral': ['okay', 'normal', 'standard', 'regular', 'usual']
        }

    def analyze_input(self, input_data: str) -> Dict[str, Any]:
        """Analyze input data to extract relevant context."""
        return {
            "entities": self._extract_entities(input_data),
            "sentiment": self._analyze_sentiment(input_data),
            "key_points": self._extract_key_points(input_data),
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "length": len(input_data),
                "complexity": self._calculate_complexity(input_data)
            }
        }

    def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract entities from text using patterns."""
        entities = defaultdict(list)

        for entity_type, pattern in self.entity_patterns.items():
            matches = re.finditer(pattern, text)
            entities[entity_type].extend([m.group() for m in matches])

        return dict(entities)

    def _analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze text sentiment based on keyword matching."""
        text = text.lower()
        scores = {
            'positive': 0.0,
            'negative': 0.0,
            'neutral': 0.0
        }

        words = text.split()
        total_matches = 0

        for sentiment, keywords in self.sentiment_keywords.items():
            matches = sum(1 for word in words if word in keywords)
            scores[sentiment] = matches
            total_matches += matches

        # Normalize scores
        if total_matches > 0:
            for sentiment in scores:
                scores[sentiment] /= total_matches
        else:
            scores['neutral'] = 1.0

        return scores

    def _extract_key_points(self, text: str) -> List[str]:
        """Extract key points from text."""
        sentences = re.split(r'[.!?]+', text)
        key_points = []

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Identify sentences with important indicators
            indicators = ['must', 'should',
                          'important', 'key', 'critical', 'need']
            if any(indicator in sentence.lower() for indicator in indicators):
                key_points.append(sentence)

        return key_points

    def _calculate_complexity(self, text: str) -> float:
        """Calculate text complexity score."""
        words = text.split()
        if not words:
            return 0.0

        avg_word_length = sum(len(word) for word in words) / len(words)
        sentence_count = len(re.split(r'[.!?]+', text))

        return (avg_word_length * 0.5) + (len(words) / max(sentence_count, 1) * 0.5)

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
