import cProfile
import pstats
from typing import Callable, Any
import os
from datetime import datetime


class Profiler:
    def __init__(self, output_dir: str = "profiles"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def profile_function(
        self,
        func: Callable,
        *args,
        **kwargs
    ) -> tuple[Any, pstats.Stats]:
        """Profile a function and return its result and stats."""
        profile = cProfile.Profile()
        result = profile.runcall(func, *args, **kwargs)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        stats_file = os.path.join(
            self.output_dir,
            f"profile_{func.__name__}_{timestamp}.stats"
        )

        stats = pstats.Stats(profile)
        stats.sort_stats('cumulative')
        stats.dump_stats(stats_file)

        return result, stats

    def analyze_stats(self, stats: pstats.Stats) -> Dict:
        """Analyze profiling statistics."""
        return {
            "total_calls": stats.total_calls,
            "total_time": stats.total_tt,
            "primitive_calls": stats.prim_calls,
            "top_functions": self._get_top_functions(stats)
        }

    def _get_top_functions(self, stats: pstats.Stats, limit: int = 10) -> List[Dict]:
        """Get the top N functions by cumulative time."""
        top_stats = []
        for func, (cc, nc, tt, ct, callers) in stats.stats.items():
            top_stats.append({
                "function": f"{func[2]}:{func[1]}",
                "calls": cc,
                "total_time": tt,
                "cumulative_time": ct
            })

        return sorted(
            top_stats,
            key=lambda x: x["cumulative_time"],
            reverse=True
        )[:limit]
