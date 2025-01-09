#!/usr/bin/env python3
"""Benchmark script for IntelliAgent."""

import time
import statistics
from typing import List, Dict
import argparse
import json
from datetime import datetime

from intelliagent import DecisionMaker
from intelliagent.utils import DataProcessor


def run_benchmark(
    iterations: int,
    test_cases: List[str],
    api_key: str
) -> Dict:
    """Run benchmark tests."""
    agent = DecisionMaker(api_key=api_key)

    latencies = []
    results = []

    start_time = time.time()

    for _ in range(iterations):
        for case in test_cases:
            case_start = time.time()
            result = agent.make_decision("benchmark_user", case)
            latency = time.time() - case_start

            latencies.append(latency)
            results.append({
                "case": case,
                "latency": latency,
                "result": result
            })

    total_time = time.time() - start_time

    return {
        "timestamp": datetime.now().isoformat(),
        "iterations": iterations,
        "total_time": total_time,
        "avg_latency": statistics.mean(latencies),
        "median_latency": statistics.median(latencies),
        "p95_latency": statistics.quantiles(latencies, n=20)[-1],
        "min_latency": min(latencies),
        "max_latency": max(latencies),
        "results": results
    }


def main():
    parser = argparse.ArgumentParser(description="Run IntelliAgent benchmarks")
    parser.add_argument("--iterations", type=int, default=100)
    parser.add_argument("--output", type=str, default="benchmark_results.json")
    parser.add_argument("--api-key", type=str, required=True)
    args = parser.parse_args()

    test_cases = [
        "What's the weather like today?",
        "Should I invest in tech stocks?",
        "Recommend a good restaurant.",
    ]

    print(f"Running benchmark with {args.iterations} iterations...")
    results = run_benchmark(args.iterations, test_cases, args.api_key)

    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to {args.output}")
    print(f"Average latency: {results['avg_latency']:.3f}s")
    print(f"P95 latency: {results['p95_latency']:.3f}s")


if __name__ == "__main__":
    main()
