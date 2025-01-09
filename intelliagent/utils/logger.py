import logging
from typing import Optional
from datetime import datetime
import os


class AgentLogger:
    def __init__(
        self,
        name: str = "intelliagent",
        log_level: int = logging.INFO,
        log_file: Optional[str] = None
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # File handler (optional)
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def log_decision(self, user_id: str, input_data: str, decision: dict) -> None:
        """Log a decision made by the agent."""
        self.logger.info(
            f"Decision made for user {user_id}:\n"
            f"Input: {input_data}\n"
            f"Decision: {decision}"
        )

    def log_error(self, error: Exception, context: dict) -> None:
        """Log an error with context."""
        self.logger.error(
            f"Error occurred: {str(error)}\n"
            f"Context: {context}"
        )

    def log_feedback(self, user_id: str, feedback: str) -> None:
        """Log user feedback."""
        self.logger.info(
            f"Feedback received from user {user_id}:\n"
            f"Feedback: {feedback}"
        )
