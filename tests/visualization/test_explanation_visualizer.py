"""Tests for the explanation visualizer."""

import pytest
from datetime import datetime, timedelta
import plotly.graph_objects as go

from intelliagent.visualization.explanation_visualizer import ExplanationVisualizer
from intelliagent.core.explainability import Explanation, ContextFactor


@pytest.fixture
def visualizer():
    return ExplanationVisualizer()


@pytest.fixture
def sample_explanation():
    return Explanation(
        decision_id="test_decision",
        reasoning_steps=["Step 1", "Step 2"],
        evidence={"source1": ["evidence1"]},
        confidence=0.8,
        metadata={"decision_type": "recommendation"},
        timestamp=datetime.now(),
        context_influence={
            "factor1": ContextFactor(
                name="factor1",
                value="value1",
                influence_score=0.6,
                confidence=0.8,
                category="category1"
            ),
            "factor2": ContextFactor(
                name="factor2",
                value="value2",
                influence_score=0.4,
                confidence=0.7,
                category="category2"
            )
        },
        key_factors=["factor1", "factor2"]
    )


def test_create_influence_chart(visualizer, sample_explanation):
    """Test influence chart creation."""
    chart = visualizer.create_influence_chart(sample_explanation)

    assert isinstance(chart, go.Figure)
    assert chart.layout.title.text == "Top Context Factors by Influence"
    assert len(chart.data) == 1
    assert isinstance(chart.data[0], go.Bar)


def test_create_confidence_trend(visualizer, sample_explanation):
    """Test confidence trend visualization."""
    explanations = [sample_explanation]
    chart = visualizer.create_confidence_trend(explanations)

    assert isinstance(chart, go.Figure)
    assert chart.layout.title.text == "Confidence Trend Over Time"
    assert len(chart.data) == 1


def test_create_confidence_trend_with_window(visualizer, sample_explanation):
    """Test confidence trend with time window."""
    explanations = [sample_explanation]
    window = timedelta(hours=1)
    chart = visualizer.create_confidence_trend(explanations, window)

    assert isinstance(chart, go.Figure)


def test_create_category_distribution(visualizer, sample_explanation):
    """Test category distribution visualization."""
    explanations = [sample_explanation]
    chart = visualizer.create_category_distribution(explanations)

    assert isinstance(chart, go.Figure)
    assert chart.layout.title.text == "Context Factor Category Distribution"
    assert len(chart.data) == 1
    assert isinstance(chart.data[0], go.Sunburst)


def test_create_decision_flow(visualizer, sample_explanation):
    """Test decision flow visualization."""
    chart = visualizer.create_decision_flow(sample_explanation)

    # Since _create_network_graph is a placeholder, we expect None
    assert chart is None


def test_create_network_graph(visualizer):
    """Test network graph creation."""
    nodes = ["Node1", "Node2", "Node3"]
    edges = [("Node1", "Node2"), ("Node2", "Node3")]

    chart = visualizer._create_network_graph(nodes, edges)

    assert isinstance(chart, go.Figure)
    assert len(chart.data) == 2  # One trace for edges, one for nodes
    assert chart.layout.title.text == "Decision Flow Network"


def test_create_factor_correlation_heatmap(visualizer, sample_explanation):
    """Test correlation heatmap creation."""
    # Create multiple explanations with different factors
    explanations = [
        sample_explanation,
        Explanation(
            decision_id="test_decision_2",
            reasoning_steps=["Step 1"],
            evidence={"source1": ["evidence1"]},
            confidence=0.7,
            metadata={"decision_type": "recommendation"},
            timestamp=datetime.now(),
            context_influence={
                "factor1": ContextFactor(
                    name="factor1",
                    value="value1",
                    influence_score=0.3,
                    confidence=0.8,
                    category="category1"
                ),
                "factor3": ContextFactor(
                    name="factor3",
                    value="value3",
                    influence_score=0.7,
                    confidence=0.9,
                    category="category3"
                )
            },
            key_factors=["factor1", "factor3"]
        )
    ]

    chart = visualizer.create_factor_correlation_heatmap(explanations)

    assert isinstance(chart, go.Figure)
    assert chart.layout.title.text == "Context Factor Correlation Heatmap"
    assert len(chart.data) == 1
    assert isinstance(chart.data[0], go.Heatmap)


def test_create_decision_timeline(visualizer, sample_explanation):
    """Test timeline visualization creation."""
    explanations = [
        sample_explanation,
        Explanation(
            decision_id="test_decision_2",
            reasoning_steps=["Step 1"],
            evidence={"source1": ["evidence1"]},
            confidence=0.7,
            metadata={"decision_type": "classification"},
            timestamp=datetime.now(),
            context_influence={
                "factor1": ContextFactor(
                    name="factor1",
                    value="value1",
                    influence_score=0.8,
                    confidence=0.7,
                    category="category1"
                )
            },
            key_factors=["factor1"]
        )
    ]

    chart = visualizer.create_decision_timeline(explanations)

    assert isinstance(chart, go.Figure)
    assert chart.layout.title.text == "Decision Timeline"
    assert len(chart.data) >= 2  # At least confidence line and one decision type


def test_create_decision_timeline_with_window(visualizer, sample_explanation):
    """Test timeline visualization with time window."""
    explanations = [sample_explanation]
    window = timedelta(hours=1)

    chart = visualizer.create_decision_timeline(explanations, window)

    assert isinstance(chart, go.Figure)
    assert chart.layout.title.text == "Decision Timeline"
