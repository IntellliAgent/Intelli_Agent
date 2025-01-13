"""Tests for benchmarking utilities."""

import time
from unittest.mock import patch
import pytest

from intelliagent.utils.benchmarking import (
    benchmark,
    timer,
    PerformanceMonitor,
    BenchmarkResult
)


def test_benchmark_decorator():
    """Test benchmark decorator."""
    @benchmark(name="test_func", iterations=3)
    def test_function():
        time.sleep(0.1)
        return 42

    result = test_function()
    assert result == 42


def test_benchmark_result():
    """Test benchmark result class."""
    result = BenchmarkResult(
        name="test",
        execution_time=1.234,
        memory_usage=100.5,
        cpu_usage=50.0
    )

    assert "test" in str(result)
    assert "1.234" in str(result)
    assert "100.5" in str(result)
    assert "50.0" in str(result)


def test_timer_context():
    """Test timer context manager."""
    with patch('time.perf_counter') as mock_time:
        mock_time.side_effect = [0, 1.5]  # Start and end times

        with timer("Test Operation"):
            pass  # Operation being timed


def test_performance_monitor():
    """Test performance monitor."""
    monitor = PerformanceMonitor()

    # Record some metrics
    monitor.record_metric('execution_time', 1.0)
    monitor.record_metric('execution_time', 2.0)
    monitor.record_metric('execution_time', 3.0)

    # Get statistics
    stats = monitor.get_statistics('execution_time')
    assert stats['mean'] == 2.0
    assert stats['median'] == 2.0
    assert stats['min'] == 1.0
    assert stats['max'] == 3.0

    # Clear metrics
    monitor.clear()
    assert not monitor.metrics['execution_time']


@pytest.mark.benchmark
def test_benchmark_with_warmup():
    """Test benchmark with warmup iterations."""
    counter = 0

    @benchmark(name="warmup_test", iterations=2, warmup=1)
    def test_function():
        nonlocal counter
        counter += 1
        return counter

    result = test_function()
    assert counter == 3  # 1 warmup + 2 iterations
