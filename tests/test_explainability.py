"""Tests for the explainability engine."""

import pytest
from datetime import datetime
from intelliagent.core.explainability import ExplainabilityEngine, Explanation, ContextFactor


@pytest.fixture
def engine():
    return ExplainabilityEngine()


def test_generate_explanation(engine):
    """Test basic explanation generation."""
    decision = "Buy stocks"
    context = {"market_trend": "up", "risk_level": "medium"}
    thought_chain = [
        {"content": "Market is trending upward", "confidence": 0.9},
        {"content": "Risk level is acceptable", "confidence": 0.8}
    ]
    confidence = 0.85

    explanation = engine.generate_explanation(
        decision, context, thought_chain, confidence
    )

    assert isinstance(explanation, Explanation)
    assert explanation.decision_id.startswith("exp_")
    assert len(explanation.reasoning_steps) == 2
    assert explanation.confidence == 0.85
    assert explanation.context_influence is not None
    assert len(explanation.context_influence) == 2
    assert all(0 <= v <= 1 for v in explanation.context_influence.values())


def test_visualize_explanation(engine):
    """Test explanation visualization."""
    # First generate an explanation
    decision = "Sell stocks"
    context = {"market_trend": "down"}
    thought_chain = [{"content": "Market is declining", "confidence": 0.9}]
    confidence = 0.9

    explanation = engine.generate_explanation(
        decision, context, thought_chain, confidence
    )

    # Test visualization
    visualization = engine.visualize_explanation(explanation.decision_id)

    assert isinstance(visualization, str)
    assert "Decision ID" in visualization
    assert "Reasoning Steps" in visualization
    assert "Evidence" in visualization
    assert "Context Influence" in visualization


def test_analyze_context_influence(engine):
    """Test context influence analysis."""
    context = {
        "factor1": "value1",
        "factor2": "value2",
        "factor3": "value3"
    }

    influence = engine._analyze_context_influence(context)

    assert len(influence) == 3
    assert abs(sum(influence.values()) - 1.0) < 0.0001  # Should sum to 1
    assert all(v == 1/3 for v in influence.values())  # Equal distribution


def test_get_nonexistent_explanation(engine):
    """Test retrieving non-existent explanation."""
    result = engine.get_explanation("nonexistent_id")
    assert result is None


def test_visualize_nonexistent_explanation(engine):
    """Test visualizing non-existent explanation."""
    result = engine.visualize_explanation("nonexistent_id")
    assert result == "Explanation not found."


def test_explanation_with_empty_context(engine):
    """Test explanation generation with empty context."""
    decision = "No action"
    context = {}
    thought_chain = [{"content": "No context available", "confidence": 0.5}]
    confidence = 0.5

    explanation = engine.generate_explanation(
        decision, context, thought_chain, confidence
    )

    assert explanation.context_influence == {}
    assert explanation.metadata["context_size"] == 0


def test_explanation_metadata(engine):
    """Test explanation metadata generation."""
    decision = "Should invest"
    context = {"funds": "available"}
    thought_chain = [{"content": "Investment possible", "confidence": 0.8}]
    confidence = 0.8

    explanation = engine.generate_explanation(
        decision, context, thought_chain, confidence
    )

    assert explanation.metadata["decision_type"] == "recommendation"
    assert explanation.metadata["context_size"] == 1
    assert explanation.metadata["chain_length"] == 1


def test_advanced_context_influence(engine):
    """Test advanced context influence analysis."""
    context = {
        "priority_factor": "high",
        "user_age": 25,
        "timestamp": "2024-03-21T12:00:00",
        "is_active": True
    }

    influence = engine._analyze_context_influence(context)

    assert len(influence) == 4
    assert all(isinstance(v, ContextFactor) for v in influence.values())
    assert influence["priority_factor"].influence_score > influence["user_age"].influence_score
    assert influence["user_age"].category == "numerical"
    assert influence["timestamp"].category == "temporal"


def test_factor_confidence_calculation(engine):
    """Test confidence calculation for different factor types."""
    assert engine._calculate_factor_confidence(42) == 1.0
    assert engine._calculate_factor_confidence(True) == 1.0
    assert engine._calculate_factor_confidence("") == 0.0
    assert engine._calculate_factor_confidence(None) == 0.0
    assert 0 < engine._calculate_factor_confidence("test") < 1


def test_text_visualization_format(engine):
    """Test text format visualization."""
    decision = "Test decision"
    context = {"test_factor": "value"}
    thought_chain = [{"content": "Test thought", "confidence": 0.8}]

    explanation = engine.generate_explanation(
        decision, context, thought_chain, 0.8
    )

    text_viz = engine.visualize_explanation(
        explanation.decision_id,
        format='text'
    )

    assert isinstance(text_viz, str)
    assert "Decision Explanation" in text_viz
    assert "Reasoning Steps" in text_viz
    assert "Key Factors" in text_viz


def test_compare_explanations(engine):
    """Test explanation comparison."""
    # Create two explanations
    context1 = {"factor1": "value1", "factor2": "value2"}
    context2 = {"factor1": "value1", "factor3": "value3"}

    exp1 = engine.generate_explanation(
        "Decision 1",
        context1,
        [{"content": "Thought 1", "confidence": 0.8}],
        0.8
    )

    exp2 = engine.generate_explanation(
        "Decision 2",
        context2,
        [{"content": "Thought 2", "confidence": 0.9}],
        0.9
    )

    comparison = engine.compare_explanations(
        exp1.decision_id,
        exp2.decision_id
    )

    assert comparison["confidence_diff"] == 0.1
    assert len(comparison["context_changes"]["added"]) == 1
    assert len(comparison["context_changes"]["removed"]) == 1
    assert len(comparison["context_changes"]["unchanged"]) == 1


def test_explanation_summary(engine):
    """Test explanation summarization."""
    context = {
        "priority_factor": "high",
        "risk_level": "medium",
        "user_age": 25
    }

    explanation = engine.generate_explanation(
        "Test decision",
        context,
        [{"content": "Test thought", "confidence": 0.8}],
        0.8
    )

    summary = engine.summarize_explanation(explanation.decision_id)

    assert isinstance(summary, str)
    assert "confidence" in summary.lower()
    assert "key factors" in summary.lower()


def test_historical_analysis(engine):
    """Test historical analysis."""
    # Generate multiple explanations
    for i in range(3):
        engine.generate_explanation(
            f"Decision {i}",
            {"factor": f"value{i}"},
            [{"content": f"Thought {i}", "confidence": 0.7 + i * 0.1}],
            0.7 + i * 0.1
        )

    analysis = engine.get_historical_analysis()

    assert analysis["total_decisions"] == 3
    assert "average_confidence" in analysis
    assert "confidence_trend" in analysis
    assert analysis["confidence_trend"]["trend"] == "increasing"


def test_medium_summary_format(engine):
    """Test medium-length summary generation."""
    context = {
        "priority_factor": "high",
        "risk_level": "medium",
        "user_age": 25
    }
    thought_chain = [
        {"content": "First thought", "confidence": 0.8},
        {"content": "Second thought", "confidence": 0.9}
    ]

    explanation = engine.generate_explanation(
        "Test decision",
        context,
        thought_chain,
        0.85
    )

    summary = engine.summarize_explanation(
        explanation.decision_id,
        format='medium'
    )

    assert "Decision Analysis" in summary
    assert "Key Factors" in summary
    assert "Reasoning Steps" in summary
    assert all(f"- {thought['content']}" in summary for thought in thought_chain)


def test_long_summary_format(engine):
    """Test detailed summary generation."""
    context = {
        "priority_factor": "high",
        "risk_level": "medium",
        "user_age": 25
    }
    thought_chain = [{"content": "Test thought", "confidence": 0.8}]

    explanation = engine.generate_explanation(
        "Test decision",
        context,
        thought_chain,
        0.8
    )

    summary = engine.summarize_explanation(
        explanation.decision_id,
        format='long'
    )

    assert "Evidence Analysis" in summary
    assert "Context Categories" in summary
    assert all(
        category in summary
        for category in ["numerical", "general"]
    )


def test_category_distribution_analysis(engine):
    """Test analysis of context factor categories."""
    # Generate explanations with different categories
    contexts = [
        {"user_age": 25, "timestamp": "2024-03-21"},
        {"priority": "high", "status": "active"},
        {"user_name": "test", "time_spent": 30}
    ]

    for context in contexts:
        engine.generate_explanation(
            "Test decision",
            context,
            [{"content": "Test thought", "confidence": 0.8}],
            0.8
        )

    analysis = engine.get_historical_analysis()
    distribution = analysis["category_distribution"]

    assert "temporal" in distribution
    assert "numerical" in distribution
    assert "user" in distribution
    assert all(
        "percentage" in stats and "avg_influence" in stats
        for stats in distribution.values()
    )
