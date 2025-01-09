from typing import Dict, Any, Optional
from datetime import datetime

from ..models.gpt_model import GPTModel
from ..utils.context_analyzer import ContextAnalyzer
from ..utils.cache_manager import CacheManager
from ..utils.rate_limiter import RateLimiter
from ..core.chain_of_thought import ChainOfThought
from ..core.uncertainty_handler import UncertaintyHandler


class DecisionMaker:
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4",
        cache_size: int = 1000,
        requests_per_minute: int = 60
    ):
        """Initialize the decision maker with required components."""
        self.model = GPTModel(api_key=api_key, model_name=model)
        self.context_analyzer = ContextAnalyzer()
        self.cache = CacheManager(max_size=cache_size)
        self.rate_limiter = RateLimiter(requests_per_minute=requests_per_minute)
        self.chain_of_thought = ChainOfThought()
        self.uncertainty_handler = UncertaintyHandler()

    def make_decision(
        self,
        user_id: str,
        input_data: str,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make a decision based on input and context."""
        # Check rate limit
        if not self.rate_limiter.check_limit(user_id):
            return {
                "error": "Rate limit exceeded",
                "remaining_requests": self.rate_limiter.get_remaining_requests(user_id)
            }

        # Check cache
        cache_key = self._generate_cache_key(input_data, context)
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return {**cached_result, "cached": True}

        # Analyze context
        enriched_context = self.context_analyzer.analyze(
            input_data,
            context or {}
        )

        # Generate chain of thought
        thought_id = self.chain_of_thought.add_thought(
            content=input_data,
            confidence=1.0,
            context=enriched_context
        )

        # Make decision
        try:
            result = self.model.process_input(input_data, enriched_context)

            # Evaluate uncertainty
            uncertainty_score, uncertainty_details = (
                self.uncertainty_handler.evaluate_uncertainty(
                    result.get("predictions", []),
                    enriched_context
                )
            )

            # Prepare final response
            response = {
                "decision": result.get("decision"),
                "confidence": 1.0 - uncertainty_score,
                "reasoning": result.get("reasoning", []),
                "uncertainty": uncertainty_details,
                "context": enriched_context,
                "thought_chain": self.chain_of_thought.get_chain(thought_id),
                "timestamp": datetime.now().isoformat(),
                "cached": False
            }

            # Cache result
            self.cache.set(cache_key, response)

            return response

        except Exception as e:
            return {
                "error": str(e),
                "context": enriched_context,
                "timestamp": datetime.now().isoformat()
            }

    def _generate_cache_key(
        self,
        input_data: str,
        context: Optional[Dict]
    ) -> str:
        """Generate a cache key from input and context."""
        key_parts = [input_data]
        if context:
            for k, v in sorted(context.items()):
                key_parts.append(f"{k}:{v}")
        return ":".join(key_parts)
