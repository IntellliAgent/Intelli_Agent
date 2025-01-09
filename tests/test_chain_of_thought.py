import pytest
from datetime import datetime
from intelliagent.core.chain_of_thought import ChainOfThought, Thought


@pytest.fixture
def chain():
    return ChainOfThought()


def test_add_thought(chain):
    content = "Test thought"
    confidence = 0.8
    context = {"key": "value"}

    thought_id = chain.add_thought(content, confidence, context)

    assert thought_id is not None
    assert thought_id.startswith("thought_")
    assert len(chain.thoughts) == 1
    assert chain.thoughts[0].content == content
    assert chain.thoughts[0].confidence == confidence
    assert chain.thoughts[0].context == context


def test_get_chain_no_thought_id(chain):
    # Add multiple thoughts
    chain.add_thought("First thought", 0.8, {})
    thought_id = chain.add_thought("Second thought", 0.9, {})

    # Get current chain
    thought_chain = chain.get_chain()

    assert len(thought_chain) == 2
    assert thought_chain[-1].content == "Second thought"


def test_get_chain_with_thought_id(chain):
    # Create a chain of thoughts
    first_id = chain.add_thought("First", 0.8, {})
    second_id = chain.add_thought(
        "Second",
        0.9,
        {},
        previous_thought_id=first_id
    )
    chain.add_thought(
        "Third",
        0.7,
        {},
        previous_thought_id=second_id
    )

    # Get chain for second thought
    chain_for_second = chain.get_chain(second_id)

    assert len(chain_for_second) == 2
    assert chain_for_second[0].content == "First"
    assert chain_for_second[1].content == "Second"


def test_analyze_chain(chain):
    # Create a chain with known values
    chain.add_thought("First", 0.8, {"context": "initial"})
    thought_id = chain.add_thought("Second", 0.6, {"context": "updated"})

    # Get and analyze the chain
    thought_chain = chain.get_chain(thought_id)
    analysis = chain.analyze_chain(thought_chain)

    assert "length" in analysis
    assert analysis["length"] == 2
    assert "average_confidence" in analysis
    assert analysis["average_confidence"] == 0.7
    assert "context_evolution" in analysis


def test_analyze_context_evolution(chain):
    # Create thoughts with changing context
    chain.add_thought(
        "First",
        0.8,
        {"key1": "value1", "key2": "old"}
    )
    thought_id = chain.add_thought(
        "Second",
        0.9,
        {"key1": "value1", "key2": "new"}
    )

    # Get and analyze the chain
    thought_chain = chain.get_chain(thought_id)
    analysis = chain.analyze_chain(thought_chain)

    context_changes = analysis["context_evolution"]
    assert len(context_changes) > 0
    assert any("key2" in changes for changes in context_changes.values())
