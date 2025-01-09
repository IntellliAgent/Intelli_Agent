from typing import Dict, List, Any
from datetime import datetime
import re
from collections import defaultdict


class ContextAnalyzer:
    def __init__(self):
        self.context_cache = {}
        self.entity_patterns = {
            'email': r'[\w\.-]+@[\w\.-]+\.\w+',
            'phone': r'\+?1?\d{9,15}',
            'money': r'\$\d+(?:\.\d{2})?',
            'percentage': r'\d+(?:\.\d+)?%',
            'date': r'\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}',
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

    def merge_contexts(self, old_context: Dict, new_context: Dict) -> Dict:
        """Merge old and new contexts intelligently."""
        merged = old_context.copy()

        for key, value in new_context.items():
            if key not in merged:
                merged[key] = value
            elif isinstance(value, dict) and isinstance(merged[key], dict):
                merged[key] = self.merge_contexts(merged[key], value)
            elif isinstance(value, list) and isinstance(merged[key], list):
                merged[key] = list(set(merged[key] + value))
            else:
                merged[key] = value

        return merged

    def get_relevant_history(
        self,
        user_id: str,
        current_context: Dict,
        max_items: int = 5
    ) -> List[Dict]:
        """Get relevant historical context for the current situation."""
        if user_id not in self.context_cache:
            return []

        history = self.context_cache[user_id]
        scored_history = []

        for hist_item in history:
            relevance_score = self._calculate_relevance(
                hist_item,
                current_context
            )
            scored_history.append((relevance_score, hist_item))

        # Sort by relevance and return top items
        scored_history.sort(reverse=True, key=lambda x: x[0])
        return [item for _, item in scored_history[:max_items]]

    def _calculate_relevance(
        self,
        historical_item: Dict,
        current_context: Dict
    ) -> float:
        """Calculate relevance score between historical item and current context."""
        score = 0.0

        # Check entity overlap
        hist_entities = set(str(e)
                            for e in historical_item.get('entities', []))
        curr_entities = set(str(e)
                            for e in current_context.get('entities', []))
        entity_overlap = len(hist_entities & curr_entities)
        score += entity_overlap * 0.3

        # Check sentiment similarity
        hist_sentiment = historical_item.get('sentiment', {})
        curr_sentiment = current_context.get('sentiment', {})
        sentiment_diff = sum(
            abs(hist_sentiment.get(k, 0) - curr_sentiment.get(k, 0))
            for k in set(hist_sentiment) | set(curr_sentiment)
        )
        score += (1 - sentiment_diff) * 0.2

        # Check recency (if timestamp available)
        if 'timestamp' in historical_item:
            hist_time = datetime.fromisoformat(historical_item['timestamp'])
            time_diff = (datetime.now() - hist_time).total_seconds()
            recency_score = 1.0 / (1.0 + time_diff / 86400)  # Decay over days
            score += recency_score * 0.5

        return score
