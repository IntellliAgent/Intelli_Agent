"""Performance profiling system for IntelliAgent."""

import time
import cProfile
import pstats
from typing import Dict, Any, Callable, Optional
from functools import wraps
from datetime import datetime


class PerformanceProfiler:
    def __init__(self):
        """Initialize the performance profiler."""
        self.profiles: Dict[str, Dict[str, Any]] = {}
        self.current_profile: Optional[cProfile.Profile] = None

    def start_profiling(self, name: str) -> None:
        """Start profiling a section of code.

        Args:
            name: Name of the profile section.
        """
        if self.current_profile:
            raise RuntimeError("Profiling already in progress")

        self.current_profile = cProfile.Profile()
        self.current_profile.enable()
        self.profiles[name] = {
            "start_time": datetime.now(),
            "stats": None
        }

    def stop_profiling(self) -> Dict[str, Any]:
        """Stop current profiling session.

        Returns:
            Dict[str, Any]: Profiling results.
        """
        if not self.current_profile:
            raise RuntimeError("No profiling in progress")

        self.current_profile.disable()
        stats = pstats.Stats(self.current_profile)

        for name, profile in self.profiles.items():
            if profile["stats"] is None:
                profile["stats"] = stats
                profile["end_time"] = datetime.now()
                profile["duration"] = (
                    profile["end_time"] - profile["start_time"]
                ).total_seconds()
                return self._format_stats(profile)

        return {}

    def profile(self, func: Callable) -> Callable:
        """Decorator for profiling functions.

        Args:
            func: Function to profile.

        Returns:
            Callable: Wrapped function.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            profile_name = f"{func.__name__}_{time.time()}"
            self.start_profiling(profile_name)
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                self.stop_profiling()
        return wrapper

    def get_profile(self, name: str) -> Optional[Dict[str, Any]]:
        """Get profiling results by name.

        Args:
            name: Name of the profile to retrieve.

        Returns:
            Optional[Dict[str, Any]]: Profile results if found.
        """
        profile = self.profiles.get(name)
        if not profile or not profile["stats"]:
            return None
        return self._format_stats(profile)

    def _format_stats(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Format profiling statistics.

        Args:
            profile: Raw profile data.

        Returns:
            Dict[str, Any]: Formatted statistics.
        """
        stats = profile["stats"]
        return {
            "duration": profile["duration"],
            "function_calls": stats.total_calls,
            "primitive_calls": stats.prim_calls,
            "total_time": stats.total_tt,
            "timestamp": profile["start_time"].isoformat()
        }
