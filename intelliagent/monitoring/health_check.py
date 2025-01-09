"""Health monitoring system for IntelliAgent."""

import psutil
from typing import Dict, Any
from datetime import datetime, timedelta


class HealthMonitor:
    def __init__(self):
        """Initialize the health monitor."""
        self.start_time = datetime.now()

    def get_system_health(self) -> Dict[str, Any]:
        """Get system health metrics.

        Returns:
            Dict[str, Any]: System health metrics.
        """
        return {
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "uptime": str(datetime.now() - self.start_time)
        }

    def get_agent_health(self, agent: Any) -> Dict[str, Any]:
        """Get agent-specific health metrics.

        Args:
            agent: The agent instance to monitor.

        Returns:
            Dict[str, Any]: Agent health metrics.
        """
        return {
            "cache_size": self._get_cache_size(agent),
            "memory_usage": self._get_memory_usage(agent),
            "model_status": self._check_model_status(agent),
            "last_error": self._get_last_error(agent)
        }

    def _get_cache_size(self, agent: Any) -> int:
        """Get size of agent's cache."""
        try:
            return len(agent.cache.cache)
        except AttributeError:
            return 0

    def _get_memory_usage(self, agent: Any) -> int:
        """Get agent's memory usage."""
        try:
            return len(agent.memory_manager.memories)
        except AttributeError:
            return 0

    def _check_model_status(self, agent: Any) -> str:
        """Check if agent's model is functioning."""
        try:
            agent.model.process_input("health_check", {})
            return "healthy"
        except Exception as e:
            return f"unhealthy: {str(e)}"

    def _get_last_error(self, agent: Any) -> str:
        """Get agent's last error."""
        try:
            errors = agent.error_handler.get_error_log(limit=1)
            return errors[0] if errors else None
        except AttributeError:
            return None
