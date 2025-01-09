"""Rate limiter implementation for API request management."""

from typing import Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict


class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        """Initialize the rate limiter.

        Args:
            requests_per_minute: Maximum number of requests allowed per minute.
        """
        self.requests_per_minute = requests_per_minute
        self.request_history: Dict[str, list] = defaultdict(list)

    def check_limit(self, user_id: str) -> bool:
        """Check if user has exceeded their rate limit.

        Args:
            user_id: Unique identifier for the user.

        Returns:
            bool: True if request is allowed, False if limit exceeded.
        """
        now = datetime.now()
        self._cleanup_history(user_id, now)

        if len(self.request_history[user_id]) >= self.requests_per_minute:
            return False

        self.request_history[user_id].append(now)
        return True

    def get_remaining_requests(self, user_id: str) -> int:
        """Get number of remaining requests for user.

        Args:
            user_id: Unique identifier for the user.

        Returns:
            int: Number of remaining requests allowed.
        """
        now = datetime.now()
        self._cleanup_history(user_id, now)

        return max(0, self.requests_per_minute - len(self.request_history[user_id]))

    def _cleanup_history(self, user_id: str, current_time: datetime) -> None:
        """Remove requests older than 1 minute from history.

        Args:
            user_id: Unique identifier for the user.
            current_time: Current timestamp for comparison.
        """
        cutoff_time = current_time - timedelta(minutes=1)
        self.request_history[user_id] = [
            timestamp for timestamp in self.request_history[user_id]
            if timestamp > cutoff_time
        ]
