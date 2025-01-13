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


def test_create_decision_sankey(visualizer, sample_explanation):
    """Test Sankey diagram creation."""
    chart = visualizer.create_decision_sankey(sample_explanation)

    assert isinstance(chart, go.Figure)
    assert chart.layout.title.text == "Decision Flow (Sankey Diagram)"
    assert len(chart.data) == 1
    assert isinstance(chart.data[0], go.Sankey)

    # Check node and link data
    sankey_data = chart.data[0]
    assert len(sankey_data.node.label) >= len(sample_explanation.context_influence) + 1
    assert len(sankey_data.link.source) >= len(sample_explanation.context_influence)


def test_create_factor_importance_trend(visualizer, sample_explanation):
    """Test factor importance trend visualization."""
    # Create multiple explanations with varying factor importance
    explanations = [
        sample_explanation,
        Explanation(
            decision_id="test_decision_2",
            reasoning_steps=["Step 1"],
            evidence={"source1": ["evidence1"]},
            confidence=0.7,
            metadata={"decision_type": "recommendation"},
            timestamp=datetime.now() + timedelta(hours=1),
            context_influence={
                "factor1": ContextFactor(
                    name="factor1",
                    value="value1",
                    influence_score=0.4,
                    confidence=0.8,
                    category="category1"
                ),
                "factor2": ContextFactor(
                    name="factor2",
                    value="value2",
                    influence_score=0.6,
                    confidence=0.7,
                    category="category2"
                )
            },
            key_factors=["factor1", "factor2"]
        )
    ]

    chart = visualizer.create_factor_importance_trend(explanations)

    assert isinstance(chart, go.Figure)
    assert chart.layout.title.text == "Factor Importance Trend"
    assert len(chart.data) > 0  # Should have at least one trace
    assert all(isinstance(trace, go.Scatter) for trace in chart.data)


def test_create_category_evolution(visualizer, sample_explanation):
    """Test category evolution visualization."""
    # Create multiple explanations with different timestamps
    explanations = [
        sample_explanation,
        Explanation(
            decision_id="test_decision_2",
            reasoning_steps=["Step 1"],
            evidence={"source1": ["evidence1"]},
            confidence=0.7,
            metadata={"decision_type": "recommendation"},
            timestamp=datetime.now() + timedelta(hours=1),
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

    chart = visualizer.create_category_evolution(explanations)

    assert isinstance(chart, go.Figure)
    assert chart.layout.title.text == "Category Influence Evolution"
    assert len(chart.data) > 0
    assert all(isinstance(trace, go.Scatter) for trace in chart.data)


def test_create_confidence_distribution(visualizer, sample_explanation):
    """Test confidence distribution visualization."""
    # Create multiple explanations with different confidence levels
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
                    influence_score=0.8,
                    confidence=0.7,
                    category="category1"
                )
            },
            key_factors=["factor1"]
        )
    ]

    chart = visualizer.create_confidence_distribution(explanations)

    assert isinstance(chart, go.Figure)
    assert chart.layout.title.text == "Confidence Distribution"
    assert len(chart.data) >= 2  # Histogram and KDE
    assert isinstance(chart.data[0], go.Histogram)
    assert isinstance(chart.data[1], go.Scatter)  # KDE line


def test_create_category_comparison(visualizer, sample_explanation):
    """Test category comparison visualization."""
    # Create multiple explanations with different categories
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
                    influence_score=0.8,
                    confidence=0.7,
                    category="category1"
                ),
                "factor3": ContextFactor(
                    name="factor3",
                    value="value3",
                    influence_score=0.3,
                    confidence=0.9,
                    category="category3"
                )
            },
            key_factors=["factor1", "factor3"]
        )
    ]

    chart = visualizer.create_category_comparison(explanations)

    assert isinstance(chart, go.Figure)
    assert chart.layout.title.text == "Category Comparison (Parallel Coordinates)"
    assert len(chart.data) == 1
    assert isinstance(chart.data[0], go.Parcoords)


def test_create_factor_value_distribution(visualizer, sample_explanation):
    """Test factor value distribution visualization."""
    # Create multiple explanations with different factor values
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
                    value="value2",  # Different value
                    influence_score=0.8,
                    confidence=0.7,
                    category="category1"
                )
            },
            key_factors=["factor1"]
        )
    ]

    chart = visualizer.create_factor_value_distribution(explanations, "factor1")

    assert isinstance(chart, go.Figure)
    assert chart.layout.title.text == "Value Distribution for factor1"
    assert len(chart.data) >= 1  # At least scatter plot
    assert isinstance(chart.data[0], go.Scatter)


def test_create_outcome_analysis(visualizer, sample_explanation):
    """Test outcome analysis visualization."""
    # Create multiple explanations with different outcomes
    explanations = [
        sample_explanation,
        Explanation(
            decision_id="test_decision_2",
            reasoning_steps=["Step 1"],
            evidence={"source1": ["evidence1"]},
            confidence=0.7,
            metadata={
                "decision_type": "classification",
                "outcome": "success"
            },
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

    chart = visualizer.create_outcome_analysis(explanations)

    assert isinstance(chart, go.Figure)
    assert chart.layout.title.text == "Decision Outcome Analysis"
    assert len(chart.data) >= 2  # At least distribution and box plot
    assert any(isinstance(trace, go.Bar) for trace in chart.data)
    assert any(isinstance(trace, go.Box) for trace in chart.data)


def test_create_decision_comparison(visualizer, sample_explanation):
    """Test decision comparison visualization."""
    explanation2 = Explanation(
        decision_id="test_decision_2",
        reasoning_steps=["Step 1", "Step 2"],
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
            ),
            "factor3": ContextFactor(
                name="factor3",
                value="value3",
                influence_score=0.3,
                confidence=0.9,
                category="category3"
            )
        },
        key_factors=["factor1", "factor3"]
    )

    chart = visualizer.create_decision_comparison(sample_explanation, explanation2)

    assert isinstance(chart, go.Figure)
    assert chart.layout.title.text == "Decision Comparison"
    assert len(chart.data) >= 4  # At least bars, gauge, pies, and table
    assert any(isinstance(trace, go.Bar) for trace in chart.data)
    assert any(isinstance(trace, go.Indicator) for trace in chart.data)
    assert any(isinstance(trace, go.Pie) for trace in chart.data)
    assert any(isinstance(trace, go.Table) for trace in chart.data)
