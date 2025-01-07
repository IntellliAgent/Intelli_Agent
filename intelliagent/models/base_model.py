from abc import ABC, abstractmethod
from typing import Dict


class BaseModel(ABC):
    @abstractmethod
    def process_input(self, input_data: str, context: Dict) -> Dict:
        """Process input data with given context."""
        pass

    @abstractmethod
    def update_learning(self, feedback: str, context: Dict) -> None:
        """Update model based on feedback."""
        pass

    @abstractmethod
    def get_model_context(self) -> Dict:
        """Get current model context."""
        pass
