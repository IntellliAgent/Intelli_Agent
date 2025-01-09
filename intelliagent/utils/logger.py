import logging
import sys
from typing import Optional
from datetime import datetime
import os


class Logger:
    def __init__(
        self,
        name: str,
        log_file: Optional[str] = None,
        level: int = logging.INFO
    ):
        """Initialize the logger."""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.log_file = log_file

        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )

        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # Create file handler if log_file specified
        if log_file:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)

    def info(self, message: str, **kwargs) -> None:
        """Log info message."""
        self._log(logging.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        """Log warning message."""
        self._log(logging.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs) -> None:
        """Log error message."""
        self._log(logging.ERROR, message, **kwargs)

    def debug(self, message: str, **kwargs) -> None:
        """Log debug message."""
        self._log(logging.DEBUG, message, **kwargs)

    def _log(self, level: int, message: str, **kwargs) -> None:
        """Internal logging method with metadata."""
        metadata = {
            "timestamp": datetime.now().isoformat(),
            **kwargs
        }
        self.logger.log(level, f"{message} | {metadata}")
