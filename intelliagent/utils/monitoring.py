"""System monitoring utilities for IntelliAgent."""

import os
import time
import psutil
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from threading import Thread
from queue import Queue
import json
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class SystemMetrics:
    """Container for system metrics."""

    timestamp: float
    cpu_percent: float
    memory_percent: float
    disk_usage_percent: float
    network_io_counters: Dict[str, int]
    process_metrics: Dict[str, float]

    def to_dict(self) -> Dict:
        """Convert metrics to dictionary."""
        return {
            'timestamp': self.timestamp,
            'cpu_percent': self.cpu_percent,
            'memory_percent': self.memory_percent,
            'disk_usage_percent': self.disk_usage_percent,
            'network_io_counters': self.network_io_counters,
            'process_metrics': self.process_metrics
        }


class SystemMonitor:
    """Monitor system resources and performance."""

    def __init__(
        self,
        interval: float = 1.0,
        output_dir: Optional[str] = None
    ):
        """Initialize the system monitor.

        Args:
            interval: Sampling interval in seconds
            output_dir: Directory to save metrics (optional)
        """
        self.interval = interval
        self.output_dir = Path(output_dir) if output_dir else None
        self.metrics_queue: Queue = Queue()
        self.is_running = False
        self.monitoring_thread: Optional[Thread] = None
        self.process = psutil.Process(os.getpid())

    def start(self) -> None:
        """Start monitoring system metrics."""
        if self.is_running:
            logger.warning("Monitor is already running")
            return

        self.is_running = True
        self.monitoring_thread = Thread(target=self._monitor_loop, daemon=True)
        self.monitoring_thread.start()
        logger.info("System monitoring started")

    def stop(self) -> None:
        """Stop monitoring system metrics."""
        self.is_running = False
        if self.monitoring_thread:
            self.monitoring_thread.join()
        logger.info("System monitoring stopped")

    def _monitor_loop(self) -> None:
        """Main monitoring loop."""
        while self.is_running:
            try:
                metrics = self._collect_metrics()
                self.metrics_queue.put(metrics)
                self._save_metrics(metrics)
                time.sleep(self.interval)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")

    def _collect_metrics(self) -> SystemMetrics:
        """Collect current system metrics."""
        return SystemMetrics(
            timestamp=time.time(),
            cpu_percent=psutil.cpu_percent(),
            memory_percent=psutil.virtual_memory().percent,
            disk_usage_percent=psutil.disk_usage('/').percent,
            network_io_counters=dict(psutil.net_io_counters()._asdict()),
            process_metrics={
                'cpu_percent': self.process.cpu_percent(),
                'memory_percent': self.process.memory_percent(),
                'num_threads': self.process.num_threads(),
                'num_fds': self.process.num_fds()
            }
        )

    def _save_metrics(self, metrics: SystemMetrics) -> None:
        """Save metrics to file if output directory is specified."""
        if not self.output_dir:
            return

        self.output_dir.mkdir(parents=True, exist_ok=True)
        metrics_file = self.output_dir / f"metrics_{int(time.time())}.json"

        with open(metrics_file, 'w') as f:
            json.dump(metrics.to_dict(), f, indent=2)

    def get_latest_metrics(self) -> Optional[SystemMetrics]:
        """Get the most recent metrics."""
        if self.metrics_queue.empty():
            return None
        return self.metrics_queue.get()

    def get_average_metrics(
        self,
        num_samples: int = 10
    ) -> Optional[SystemMetrics]:
        """Calculate average metrics over recent samples.

        Args:
            num_samples: Number of samples to average

        Returns:
            Averaged system metrics or None if no samples available
        """
        metrics_list: List[SystemMetrics] = []
        while not self.metrics_queue.empty() and len(metrics_list) < num_samples:
            metrics_list.append(self.metrics_queue.get())

        if not metrics_list:
            return None

        avg_metrics = {
            'cpu_percent': sum(m.cpu_percent for m in metrics_list) / len(metrics_list),
            'memory_percent': sum(m.memory_percent for m in metrics_list) / len(metrics_list),
            'disk_usage_percent': sum(m.disk_usage_percent for m in metrics_list) / len(metrics_list),
            'process_metrics': {
                key: sum(m.process_metrics[key]
                         for m in metrics_list) / len(metrics_list)
                for key in metrics_list[0].process_metrics
            }
        }

        return SystemMetrics(
            timestamp=time.time(),
            cpu_percent=avg_metrics['cpu_percent'],
            memory_percent=avg_metrics['memory_percent'],
            disk_usage_percent=avg_metrics['disk_usage_percent'],
            network_io_counters=metrics_list[-1].network_io_counters,
            process_metrics=avg_metrics['process_metrics']
        )
