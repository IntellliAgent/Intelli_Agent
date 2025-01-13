"""Benchmarking utilities for IntelliAgent."""

import time
import functools
from typing import Any, Callable, Dict, Optional
from dataclasses import dataclass
import statistics
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)


@dataclass
class BenchmarkResult:
    """Results from a benchmark run."""

    name: str
    execution_time: float
    memory_usage: Optional[float] = None
    cpu_usage: Optional[float] = None
    additional_metrics: Dict[str, Any] = None

    def __str__(self) -> str:
        """Format benchmark result as string."""
        result = [
            f"Benchmark: {self.name}",
            f"Execution Time: {self.execution_time:.4f}s"
        ]
        if self.memory_usage:
            result.append(f"Memory Usage: {self.memory_usage:.2f}MB")
        if self.cpu_usage:
            result.append(f"CPU Usage: {self.cpu_usage:.1f}%")
        if self.additional_metrics:
            for key, value in self.additional_metrics.items():
                result.append(f"{key}: {value}")
        return "\n".join(result)


def benchmark(
    name: Optional[str] = None,
    iterations: int = 1,
    warmup: int = 0
) -> Callable:
    """Decorator for benchmarking functions.

    Args:
        name: Name of the benchmark
        iterations: Number of iterations to run
        warmup: Number of warmup iterations

    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> BenchmarkResult:
            # Run warmup iterations
            for _ in range(warmup):
                func(*args, **kwargs)

            # Run benchmark iterations
            times = []
            for _ in range(iterations):
                start = time.perf_counter()
                result = func(*args, **kwargs)
                end = time.perf_counter()
                times.append(end - start)

            # Calculate statistics
            avg_time = statistics.mean(times)
            benchmark_name = name or func.__name__

            # Create benchmark result
            benchmark_result = BenchmarkResult(
                name=benchmark_name,
                execution_time=avg_time
            )

            logger.info(str(benchmark_result))
            return result
        return wrapper
    return decorator


@contextmanager
def timer(name: str = "Operation"):
    """Context manager for timing code blocks.

    Args:
        name: Name of the operation being timed
    """
    start = time.perf_counter()
    yield
    end = time.perf_counter()
    duration = end - start
    logger.info(f"{name} took {duration:.4f} seconds")


class PerformanceMonitor:
    """Monitor and collect performance metrics."""

    def __init__(self):
        """Initialize the performance monitor."""
        self.metrics: Dict[str, list] = {
            'execution_time': [],
            'memory_usage': [],
            'cpu_usage': []
        }

    def record_metric(
        self,
        metric_name: str,
        value: float
    ) -> None:
        """Record a performance metric.

        Args:
            metric_name: Name of the metric
            value: Value to record
        """
        if metric_name not in self.metrics:
            self.metrics[metric_name] = []
        self.metrics[metric_name].append(value)

    def get_statistics(
        self,
        metric_name: str
    ) -> Dict[str, float]:
        """Get statistics for a metric.

        Args:
            metric_name: Name of the metric

        Returns:
            Dictionary of statistics
        """
        values = self.metrics.get(metric_name, [])
        if not values:
            return {}

        return {
            'mean': statistics.mean(values),
            'median': statistics.median(values),
            'std_dev': statistics.stdev(values) if len(values) > 1 else 0,
            'min': min(values),
            'max': max(values)
        }

    def clear(self) -> None:
        """Clear all recorded metrics."""
        for metric in self.metrics:
            self.metrics[metric] = []
