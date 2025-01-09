"""
IntelliAgent - Intelligent Agent for Dynamic Decision Making
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

IntelliAgent is a library that provides adaptive decision-making capabilities
through context-aware AI agents.

Basic usage:

   >>> from intelliagent import DecisionMaker
   >>> agent = DecisionMaker(api_key="your-api-key")
   >>> decision = agent.make_decision(
   ...     user_id="user123",
   ...     input_data="some input"
   ... )
   >>> print(decision)

For more information, please refer to the documentation:
https://intelliagent.readthedocs.io/
"""

from .version import __version__, __author__, __author_email__
from .core.decision_maker import DecisionMaker
from .core.async_decision_maker import AsyncDecisionMaker
from .core.belief_generator import BeliefGenerator
from .core.domain_adapter import DomainAdapter
from .core.memory_manager import MemoryManager

__all__ = [
    'DecisionMaker',
    'AsyncDecisionMaker',
    'BeliefGenerator',
    'DomainAdapter',
    'MemoryManager',
    '__version__',
    '__author__',
    '__author_email__'
]
