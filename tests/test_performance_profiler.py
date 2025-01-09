import pytest
import time
from intelliagent.profiling.performance_profiler import PerformanceProfiler


@pytest.fixture
def profiler():
    return PerformanceProfiler()


def test_profile_decorator(profiler):
    @profiler.profile
    def test_function():
        time.sleep(0.1)
        return "test"

    result = test_function()

    assert result == "test"
    assert len(profiler.profiles) == 1

    # Get the profile (there should be only one)
    profile = next(iter(profiler.profiles.values()))
    assert profile["stats"] is not None
    assert profile["duration"] >= 0.1


def test_manual_profiling(profiler):
    profiler.start_profiling("test_section")
    time.sleep(0.1)
    results = profiler.stop_profiling()

    assert "duration" in results
    assert results["duration"] >= 0.1
    assert "function_calls" in results
    assert "total_time" in results
    assert "timestamp" in results


def test_nested_profiling_error(profiler):
    profiler.start_profiling("outer")
    with pytest.raises(RuntimeError):
        profiler.start_profiling("inner")


def test_stop_without_start(profiler):
    with pytest.raises(RuntimeError):
        profiler.stop_profiling()


def test_get_nonexistent_profile(profiler):
    assert profiler.get_profile("nonexistent") is None


def test_profile_stats_format(profiler):
    @profiler.profile
    def complex_function():
        sum(range(1000))
        time.sleep(0.1)

    complex_function()

    profile = next(iter(profiler.profiles.values()))
    stats = profiler._format_stats(profile)

    assert isinstance(stats["duration"], float)
    assert isinstance(stats["function_calls"], int)
    assert isinstance(stats["primitive_calls"], int)
    assert isinstance(stats["total_time"], float)
    assert isinstance(stats["timestamp"], str)
