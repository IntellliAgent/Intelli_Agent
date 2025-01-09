"""IntelliAgent - A sophisticated AI agent framework."""

from .core.decision_maker import DecisionMaker
from .core.belief_generator import BeliefGenerator, Belief
from .core.chain_of_thought import ChainOfThought, Thought
from .core.uncertainty_handler import UncertaintyHandler, UncertaintyMetrics
from .core.explainability import ExplainabilityEngine, Explanation

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = [
    "DecisionMaker",
    "BeliefGenerator",
    "Belief",
    "ChainOfThought",
    "Thought",
    "UncertaintyHandler",
    "UncertaintyMetrics",
    "ExplainabilityEngine",
    "Explanation"
]
