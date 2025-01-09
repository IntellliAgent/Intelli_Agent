import pytest
from datetime import datetime, timedelta
from intelliagent.monitoring.health_check import HealthMonitor


@pytest.fixture
def monitor():
    return HealthMonitor()


def test_get_system_health(monitor):
    health = monitor.get_system_health()

    assert isinstance(health, dict)
    assert "cpu_usage" in health
    assert "memory_usage" in health
    assert "disk_usage" in health
    assert "uptime" in health

    assert isinstance(health["cpu_usage"], float)
    assert isinstance(health["memory_usage"], float)
    assert isinstance(health["disk_usage"], float)
    assert isinstance(health["uptime"], str)


def test_get_agent_health(monitor):
    class MockAgent:
        def __init__(self):
            self.cache = MockCache()
            self.memory_manager = MockMemoryManager()
            self.model = MockModel()
            self.error_handler = MockErrorHandler()

    class MockCache:
        cache = {"key": "value"}

    class MockMemoryManager:
        memories = ["memory1", "memory2"]

    class MockModel:
        def process_input(self, *args, **kwargs):
            return True

    class MockErrorHandler:
        def get_error_log(self, limit):
            return []

    agent = MockAgent()
    health = monitor.get_agent_health(agent)

    assert isinstance(health, dict)
    assert health["cache_size"] == 1
    assert health["memory_usage"] == 2
    assert health["model_status"] == "healthy"
    assert health["last_error"] is None


def test_agent_health_with_errors(monitor):
    class ErrorAgent:
        def __init__(self):
            self.model = ErrorModel()
            self.error_handler = ErrorHandler()

    class ErrorModel:
        def process_input(self, *args, **kwargs):
            raise Exception("Test error")

    class ErrorHandler:
        def get_error_log(self, limit):
            return ["Recent error"]

    agent = ErrorAgent()
    health = monitor.get_agent_health(agent)

    assert "unhealthy" in health["model_status"]
    assert "Test error" in health["model_status"]
    assert health["last_error"] == "Recent error"
