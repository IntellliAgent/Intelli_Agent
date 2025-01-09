import pytest
from datetime import datetime, timedelta
from intelliagent.core.belief_generator import BeliefGenerator, Belief


@pytest.fixture
def generator():
    return BeliefGenerator(confidence_threshold=0.7)


def test_generate_belief(generator):
    input_data = "The sky is blue"
    context = {"time": "day"}
    evidence = ["Visual observation", "Scientific fact"]

    belief = generator.generate_belief(input_data, context, evidence)

    assert isinstance(belief, Belief)
    assert belief.statement == input_data
    assert belief.confidence >= generator.confidence_threshold
    assert belief.evidence == evidence
    assert isinstance(belief.timestamp, datetime)
    assert belief.metadata["context"] == context


def test_update_belief(generator):
    # First create a belief
    statement = "Water boils at 100°C"
    initial_evidence = ["Laboratory test"]
    belief = generator.generate_belief(statement, {}, initial_evidence)

    # Then update it
    new_evidence = ["Multiple confirmations"]
    updated_belief = generator.update_belief(statement, new_evidence)

    assert updated_belief is not None
    assert len(updated_belief.evidence) == 2
    assert updated_belief.confidence > belief.confidence


def test_get_beliefs(generator):
    # Generate multiple beliefs
    generator.generate_belief(
        "Fact 1",
        {},
        ["Evidence 1", "Evidence 2"]
    )
    generator.generate_belief(
        "Fact 2",
        {},
        ["Evidence 3"]
    )

    beliefs = generator.get_beliefs()
    assert len(beliefs) > 0
    assert all(b.confidence >= generator.confidence_threshold for b in beliefs)


def test_confidence_calculation(generator):
    # Test with varying amounts of evidence
    no_evidence = generator._calculate_confidence("test", [])
    assert no_evidence == 0.0

    some_evidence = generator._calculate_confidence("test", ["Evidence 1"])
    more_evidence = generator._calculate_confidence(
        "test",
        ["Evidence 1", "Evidence 2"]
    )
    assert more_evidence > some_evidence
