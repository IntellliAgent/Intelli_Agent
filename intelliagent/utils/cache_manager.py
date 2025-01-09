from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from collections import OrderedDict


class CacheManager:
    def __init__(
        self,
        max_size: int = 1000,
        ttl: int = 3600  # Time to live in seconds
    ):
        """Initialize the cache manager."""
        self.max_size = max_size
        self.ttl = ttl
        self.cache: OrderedDict = OrderedDict()
        self.timestamps: Dict[str, datetime] = {}

    def get(self, key: str) -> Optional[Any]:
        """Get a value from cache."""
        if key not in self.cache:
            return None

        # Check if expired
        if self._is_expired(key):
            self._remove(key)
            return None

        # Move to end (most recently used)
        value = self.cache.pop(key)
        self.cache[key] = value
        return value

    def set(self, key: str, value: Any) -> None:
        """Set a value in cache."""
        # Remove if exists
        if key in self.cache:
            self._remove(key)

        # Remove oldest if at max size
        if len(self.cache) >= self.max_size:
            oldest_key = next(iter(self.cache))
            self._remove(oldest_key)

        # Add new value
        self.cache[key] = value
        self.timestamps[key] = datetime.now()

    def clear(self) -> None:
        """Clear the cache."""
        self.cache.clear()
        self.timestamps.clear()

    def _is_expired(self, key: str) -> bool:
        """Check if a cache entry is expired."""
        timestamp = self.timestamps.get(key)
        if not timestamp:
            return True

        return (datetime.now() - timestamp) > timedelta(seconds=self.ttl)

    def _remove(self, key: str) -> None:
        """Remove an entry from cache."""
        self.cache.pop(key, None)
        self.timestamps.pop(key, None)
