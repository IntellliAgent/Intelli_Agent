from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import json
import os


class CacheManager:
    def __init__(
        self,
        cache_dir: str = ".cache",
        max_size: int = 1000,
        ttl: int = 3600  # Time to live in seconds
    ):
        self.cache_dir = cache_dir
        self.max_size = max_size
        self.ttl = ttl
        self.cache: Dict[str, Dict[str, Any]] = {}

        # Create cache directory if it doesn't exist
        os.makedirs(cache_dir, exist_ok=True)
        self._load_cache()

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if key in self.cache:
            entry = self.cache[key]
            if self._is_valid(entry):
                return entry["value"]
            else:
                self._remove(key)
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache."""
        self.cache[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat(),
            "ttl": ttl or self.ttl
        }

        if len(self.cache) > self.max_size:
            self._cleanup()

        self._save_cache()

    def _is_valid(self, entry: Dict) -> bool:
        """Check if cache entry is still valid."""
        timestamp = datetime.fromisoformat(entry["timestamp"])
        age = (datetime.now() - timestamp).total_seconds()
        return age < entry["ttl"]

    def _cleanup(self) -> None:
        """Remove old entries from cache."""
        valid_entries = {
            k: v for k, v in self.cache.items()
            if self._is_valid(v)
        }

        if len(valid_entries) > self.max_size:
            # Sort by timestamp and keep only the most recent entries
            sorted_entries = sorted(
                valid_entries.items(),
                key=lambda x: x[1]["timestamp"],
                reverse=True
            )
            valid_entries = dict(sorted_entries[:self.max_size])

        self.cache = valid_entries

    def _save_cache(self) -> None:
        """Save cache to disk."""
        cache_file = os.path.join(self.cache_dir, "cache.json")
        with open(cache_file, 'w') as f:
            json.dump(self.cache, f)

    def _load_cache(self) -> None:
        """Load cache from disk."""
        cache_file = os.path.join(self.cache_dir, "cache.json")
        try:
            with open(cache_file, 'r') as f:
                self.cache = json.load(f)
            self._cleanup()
        except (FileNotFoundError, json.JSONDecodeError):
            self.cache = {}

    def _remove(self, key: str) -> None:
        """Remove entry from cache."""
        self.cache.pop(key, None)
        self._save_cache()
