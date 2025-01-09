import pytest
from intelliagent.monitoring.health_check import HealthMonitor


@pytest.fixture
def monitor():
    return HealthMonitor()


def test_get_system_health(monitor):
    health = monitor.get_system_health()

    assert "cpu_usage" in health
    assert "memory_usage" in health
    assert "disk_usage" in health
    assert "uptime" in health

    assert isinstance(health["cpu_usage"], float)
    assert isinstance(health["memory_usage"], float)
    assert isinstance(health["disk_usage"], float)
    assert isinstance(health["uptime"], str)


def test_get_agent_health(monitor):
    # Create mock agent
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

    assert "cache_size" in health
    assert health["cache_size"] == 1
    assert "memory_usage" in health
    assert health["memory_usage"] == 2
    assert "model_status" in health
    assert health["model_status"] == "healthy"
    assert "last_error" in health
    assert health["last_error"] is None


def test_check_model_status_error(monitor):
    class MockAgent:
        def __init__(self):
            self.model = MockModel()

    class MockModel:
        def process_input(self, *args, **kwargs):
            raise Exception("Test error")

    agent = MockAgent()
    status = monitor._check_model_status(agent)

    assert "unhealthy" in status
    assert "Test error" in status


def test_get_last_error_no_handler(monitor):
    class MockAgent:
        pass

    agent = MockAgent()
    error = monitor._get_last_error(agent)

    assert error is None
