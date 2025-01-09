from typing import Dict
from datetime import datetime, timedelta
import threading
import time


class RateLimiter:
    def __init__(
        self,
        requests_per_minute: int = 60,
        burst_limit: int = 10
    ):
        self.rate_limit = requests_per_minute
        self.burst_limit = burst_limit
        self.requests: Dict[str, list] = {}
        self.lock = threading.Lock()

    def check_limit(self, user_id: str) -> bool:
        """Check if request is within rate limits."""
        with self.lock:
            now = datetime.now()
            self._cleanup_old_requests(user_id, now)

            if user_id not in self.requests:
                self.requests[user_id] = []

            # Check burst limit
            if len(self.requests[user_id]) >= self.burst_limit:
                return False

            # Check rate limit
            minute_ago = now - timedelta(minutes=1)
            recent_requests = [
                req for req in self.requests[user_id]
                if req > minute_ago
            ]

            if len(recent_requests) >= self.rate_limit:
                return False

            self.requests[user_id].append(now)
            return True

    def _cleanup_old_requests(self, user_id: str, now: datetime) -> None:
        """Remove requests older than 1 minute."""
        if user_id in self.requests:
            minute_ago = now - timedelta(minutes=1)
            self.requests[user_id] = [
                req for req in self.requests[user_id]
                if req > minute_ago
            ]

    def get_remaining_requests(self, user_id: str) -> int:
        """Get number of remaining requests for the current minute."""
        with self.lock:
            now = datetime.now()
            self._cleanup_old_requests(user_id, now)

            if user_id not in self.requests:
                return self.rate_limit

            minute_ago = now - timedelta(minutes=1)
            recent_requests = [
                req for req in self.requests[user_id]
                if req > minute_ago
            ]

            return max(0, self.rate_limit - len(recent_requests))
