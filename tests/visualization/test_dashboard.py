"""Tests for the explanation dashboard."""

import pytest
from unittest.mock import MagicMock, patch

from intelliagent.visualization.dashboard import ExplanationDashboard
from intelliagent.core.explainability import ExplainabilityEngine, Explanation
from intelliagent.visualization.explanation_visualizer import ExplanationVisualizer


@pytest.fixture
def mock_engine():
    engine = MagicMock(spec=ExplainabilityEngine)
    engine._filter_explanations_by_time.return_value = []
    return engine


@pytest.fixture
def mock_visualizer():
    visualizer = MagicMock(spec=ExplanationVisualizer)
    return visualizer


@pytest.fixture
def dashboard(mock_engine, mock_visualizer):
    return ExplanationDashboard(mock_engine, mock_visualizer)


@patch('streamlit.title')
@patch('streamlit.sidebar.header')
@patch('streamlit.sidebar.selectbox')
def test_dashboard_initialization(mock_select, mock_header, mock_title, dashboard):
    """Test dashboard initialization."""
    dashboard.run()

    mock_title.assert_called_once()
    mock_header.assert_called_once()
    mock_select.assert_called_once()


def test_get_filtered_explanations(dashboard):
    """Test explanation filtering by time window."""
    _ = dashboard._get_filtered_explanations("1 hour")
    dashboard.engine._filter_explanations_by_time.assert_called_once()


@patch('streamlit.columns')
def test_show_overview_metrics(mock_columns, dashboard):
    """Test overview metrics display."""
    mock_cols = [MagicMock() for _ in range(4)]
    mock_columns.return_value = mock_cols

    explanations = []
    dashboard._show_overview_metrics(explanations)

    assert all(col.metric.called for col in mock_cols)


@patch('streamlit.plotly_chart')
def test_show_explanation_details(mock_chart, dashboard, mock_visualizer):
    """Test explanation details display."""
    explanation = MagicMock(spec=Explanation)
    dashboard._show_explanation_details(explanation)

    assert mock_chart.call_count == 2  # Two charts should be displayed
    dashboard.visualizer.create_influence_chart.assert_called_once()
    dashboard.visualizer.create_decision_flow.assert_called_once()


@patch('streamlit.plotly_chart')
def test_show_timeline(mock_chart, dashboard, mock_visualizer):
    """Test timeline visualization display."""
    explanations = [MagicMock(spec=Explanation)]
    dashboard._show_timeline(explanations)

    mock_chart.assert_called_once()
    dashboard.visualizer.create_decision_timeline.assert_called_once_with(
        explanations
    )


@patch('streamlit.plotly_chart')
@patch('streamlit.warning')
def test_show_correlations_with_insufficient_data(
    mock_warning,
    mock_chart,
    dashboard,
    mock_visualizer
):
    """Test correlation analysis with insufficient data."""
    explanations = [MagicMock(spec=Explanation)]
    dashboard._show_correlations(explanations)

    mock_warning.assert_called_once()
    mock_chart.assert_not_called()


@patch('streamlit.plotly_chart')
def test_show_correlations(mock_chart, dashboard, mock_visualizer):
    """Test correlation analysis display."""
    explanations = [MagicMock(spec=Explanation) for _ in range(2)]
    dashboard._show_correlations(explanations)

    mock_chart.assert_called_once()
    dashboard.visualizer.create_factor_correlation_heatmap.assert_called_once_with(
        explanations
    )


def test_visualization_type_selection(dashboard):
    """Test visualization type selection."""
    with patch('streamlit.sidebar.selectbox') as mock_select:
        mock_select.return_value = "Timeline"
        with patch.object(dashboard, '_show_timeline') as mock_timeline:
            dashboard.run()
            mock_timeline.assert_called_once()
