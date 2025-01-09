from typing import Dict, List
import psutil
import os
import json
from datetime import datetime


class HealthMonitor:
    def __init__(self):
        self.start_time = datetime.now()

    def get_system_health(self) -> Dict:
        """Get system health metrics."""
        return {
            "cpu_usage": psutil.cpu_percent(interval=1),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "uptime": str(datetime.now() - self.start_time)
        }

    def get_agent_health(self, agent) -> Dict:
        """Get agent-specific health metrics."""
        return {
            "cache_size": len(agent.cache.cache) if hasattr(agent, 'cache') else 0,
            "memory_usage": len(agent.memory_manager.memories),
            "model_status": self._check_model_status(agent),
            "last_error": self._get_last_error(agent)
        }

    def _check_model_status(self, agent) -> str:
        """Check if the model is responding correctly."""
        try:
            agent.model.process_input("test", {})
            return "healthy"
        except Exception as e:
            return f"unhealthy: {str(e)}"

    def _get_last_error(self, agent) -> Optional[Dict]:
        """Get the last error from the error handler."""
        if hasattr(agent, 'error_handler'):
            errors = agent.error_handler.get_error_log(limit=1)
            return errors[0] if errors else None
        return None
