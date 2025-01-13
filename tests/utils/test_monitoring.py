"""Tests for system monitoring utilities."""

import time
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

from intelliagent.utils.monitoring import SystemMonitor, SystemMetrics


@pytest.fixture
def mock_psutil():
    """Mock psutil for testing."""
    with patch('intelliagent.utils.monitoring.psutil') as mock:
        mock.cpu_percent.return_value = 50.0
        mock.virtual_memory().percent = 60.0
        mock.disk_usage('/').percent = 70.0
        mock.net_io_counters.return_value = MagicMock(
            _asdict=lambda: {'bytes_sent': 1000, 'bytes_recv': 2000}
        )
        mock.Process.return_value = MagicMock(
            cpu_percent=lambda: 30.0,
            memory_percent=lambda: 40.0,
            num_threads=lambda: 4,
            num_fds=lambda: 10
        )
        yield mock


def test_system_metrics():
    """Test SystemMetrics class."""
    metrics = SystemMetrics(
        timestamp=1234567890.0,
        cpu_percent=50.0,
        memory_percent=60.0,
        disk_usage_percent=70.0,
        network_io_counters={'bytes_sent': 1000, 'bytes_recv': 2000},
        process_metrics={
            'cpu_percent': 30.0,
            'memory_percent': 40.0,
            'num_threads': 4,
            'num_fds': 10
        }
    )

    metrics_dict = metrics.to_dict()
    assert metrics_dict['timestamp'] == 1234567890.0
    assert metrics_dict['cpu_percent'] == 50.0
    assert metrics_dict['memory_percent'] == 60.0


def test_system_monitor_start_stop(mock_psutil, tmp_path):
    """Test starting and stopping the system monitor."""
    monitor = SystemMonitor(interval=0.1, output_dir=str(tmp_path))

    monitor.start()
    assert monitor.is_running
    time.sleep(0.3)  # Allow some metrics to be collected
    monitor.stop()
    assert not monitor.is_running

    # Check if metrics files were created
    metrics_files = list(tmp_path.glob("metrics_*.json"))
    assert len(metrics_files) > 0


def test_system_monitor_metrics_collection(mock_psutil):
    """Test metrics collection."""
    monitor = SystemMonitor(interval=0.1)
    monitor.start()
    time.sleep(0.2)
    monitor.stop()

    metrics = monitor.get_latest_metrics()
    assert metrics is not None
    assert metrics.cpu_percent == 50.0
    assert metrics.memory_percent == 60.0
    assert metrics.disk_usage_percent == 70.0


def test_system_monitor_average_metrics(mock_psutil):
    """Test average metrics calculation."""
    monitor = SystemMonitor(interval=0.1)
    monitor.start()
    time.sleep(0.3)  # Collect multiple samples
    monitor.stop()

    avg_metrics = monitor.get_average_metrics(num_samples=3)
    assert avg_metrics is not None
    assert avg_metrics.cpu_percent == 50.0
    assert avg_metrics.memory_percent == 60.0


def test_system_monitor_error_handling(mock_psutil):
    """Test error handling in monitoring loop."""
    mock_psutil.cpu_percent.side_effect = Exception("Test error")

    monitor = SystemMonitor(interval=0.1)
    monitor.start()
    time.sleep(0.2)
    monitor.stop()

    # Monitor should continue running despite errors
    assert monitor.get_latest_metrics() is None
