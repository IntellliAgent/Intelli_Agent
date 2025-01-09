from typing import Dict, List
import time
import statistics
from ..core import DecisionMaker


class PerformanceBenchmark:
    def __init__(self, agent: DecisionMaker):
        self.agent = agent
        self.results: List[Dict] = []

    def run_latency_test(
        self,
        test_cases: List[str],
        iterations: int = 100
    ) -> Dict:
        """Run latency benchmark tests."""
        latencies = []

        for _ in range(iterations):
            for case in test_cases:
                start_time = time.time()
                self.agent.make_decision("benchmark_user", case)
                latency = time.time() - start_time
                latencies.append(latency)

        return {
            "avg_latency": statistics.mean(latencies),
            "median_latency": statistics.median(latencies),
            "p95_latency": statistics.quantiles(latencies, n=20)[-1],
            "min_latency": min(latencies),
            "max_latency": max(latencies)
        }
