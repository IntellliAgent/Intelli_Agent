"""Shared test fixtures."""
import pytest
from intelliagent import DecisionMaker
from intelliagent.models import GPTModel
from intelliagent.utils import ContextAnalyzer, DataProcessor


@pytest.fixture
def api_key():
    """Dummy API key for testing."""
    return "test-api-key-12345"


@pytest.fixture
def decision_maker(api_key):
    """Create a DecisionMaker instance for testing."""
    return DecisionMaker(
        api_key=api_key,
        model="gpt-4",
        domain="test_domain",
        continuous_learning=True
    )


@pytest.fixture
def gpt_model(api_key):
    """Create a GPTModel instance for testing."""
    return GPTModel(
        api_key=api_key,
        model="gpt-4",
        temperature=0.7,
        max_tokens=150
    )


@pytest.fixture
def context_analyzer():
    """Create a ContextAnalyzer instance for testing."""
    return ContextAnalyzer()


@pytest.fixture
def data_processor():
    """Create a DataProcessor instance for testing."""
    return DataProcessor()


@pytest.fixture
def sample_context():
    """Create a sample context for testing."""
    return {
        "user_id": "test_user",
        "domain": "test_domain",
        "entities": {
            "email": ["test@example.com"],
            "phone": ["+1234567890"]
        },
        "sentiment": {
            "positive": 0.8,
            "negative": 0.1,
            "neutral": 0.1
        },
        "metadata": {
            "timestamp": "2024-03-21T12:00:00",
            "source": "test"
        }
    }
