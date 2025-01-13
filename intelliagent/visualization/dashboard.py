"""Web dashboard for explanation visualization."""

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import List, Optional, Sequence

from .explanation_visualizer import ExplanationVisualizer
from ..core.explainability import ExplainabilityEngine, Explanation


class ExplanationDashboard:
    """Web dashboard for visualizing and analyzing explanations."""

    def __init__(
        self,
        engine: ExplainabilityEngine,
        visualizer: Optional[ExplanationVisualizer] = None
    ):
        """Initialize the dashboard."""
        self.engine = engine
        self.visualizer = visualizer or ExplanationVisualizer()

    def run(self):
        """Run the dashboard."""
        st.title("IntelliAgent Explanation Dashboard")

        # Sidebar filters
        st.sidebar.header("Filters")
        time_window = st.sidebar.selectbox(
            "Time Window",
            ["1 hour", "24 hours", "7 days", "30 days", "All time"]
        )

        visualization_type = st.sidebar.selectbox(
            "Visualization Type",
            ["Overview", "Timeline", "Correlations", "Detailed Analysis"]
        )

        # Get filtered explanations
        explanations = self._get_filtered_explanations(time_window)

        if visualization_type == "Overview":
            self._show_overview(explanations)
        elif visualization_type == "Timeline":
            self._show_timeline(explanations)
        elif visualization_type == "Correlations":
            self._show_correlations(explanations)
        else:
            self._show_detailed_analysis(explanations)

    def _get_filtered_explanations(
        self,
        time_window: str
    ) -> List[Explanation]:
        """Get explanations filtered by time window."""
        window_map = {
            "1 hour": timedelta(hours=1),
            "24 hours": timedelta(days=1),
            "7 days": timedelta(days=7),
            "30 days": timedelta(days=30),
            "All time": None
        }

        return self.engine._filter_explanations_by_time(
            None if time_window == "All time"
            else window_map[time_window].total_seconds()
        )

    def _show_overview(self, explanations: List[Explanation]):
        """Show overview metrics."""
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Decisions",
                len(explanations)
            )

        with col2:
            avg_confidence = sum(
                exp.confidence for exp in explanations
            ) / len(explanations) if explanations else 0
            st.metric(
                "Average Confidence",
                f"{avg_confidence:.1%}"
            )

        with col3:
            unique_categories = len({
                factor.category
                for exp in explanations
                for factor in exp.context_influence.values()
            })
            st.metric("Unique Categories", unique_categories)

        with col4:
            avg_steps = sum(
                len(exp.reasoning_steps) for exp in explanations
            ) / len(explanations) if explanations else 0
            st.metric(
                "Avg Reasoning Steps",
                f"{avg_steps:.1f}"
            )

    def _show_timeline(self, explanations: List[Explanation]):
        """Show timeline visualization."""
        st.header("Decision Timeline")

        st.plotly_chart(
            self.visualizer.create_decision_timeline(explanations),
            use_container_width=True
        )

    def _show_correlations(self, explanations: List[Explanation]):
        """Show correlation analysis."""
        st.header("Factor Correlations")

        if len(explanations) < 2:
            st.warning("Need at least 2 explanations for correlation analysis.")
            return

        st.plotly_chart(
            self.visualizer.create_factor_correlation_heatmap(explanations),
            use_container_width=True
        )

    def _show_detailed_analysis(self, explanations: List[Explanation]):
        """Show detailed analysis for a single explanation."""
        st.subheader("Context Influence")
        st.plotly_chart(
            self.visualizer.create_influence_chart(explanations[0]),
            use_container_width=True
        )

        st.subheader("Decision Flow")
        st.plotly_chart(
            self.visualizer.create_decision_flow(explanations[0]),
            use_container_width=True
        )

        st.subheader("Raw Data")
        st.json(self.engine.visualize_explanation(explanations[0].decision_id))
