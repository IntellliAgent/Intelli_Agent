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

        # Show comparison if active
        self._show_comparison(explanations)

        # Show main content
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

        # Add confidence distribution
        st.subheader("Confidence Distribution")
        st.plotly_chart(
            self.visualizer.create_confidence_distribution(explanations),
            use_container_width=True
        )

        # Add factor importance trend
        st.subheader("Factor Importance Over Time")
        st.plotly_chart(
            self.visualizer.create_factor_importance_trend(explanations),
            use_container_width=True
        )

        # Add outcome analysis
        st.subheader("Decision Outcomes")
        st.plotly_chart(
            self.visualizer.create_outcome_analysis(explanations),
            use_container_width=True
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

        tab1, tab2, tab3 = st.tabs([
            "Correlation Heatmap",
            "Category Evolution",
            "Category Comparison"
        ])

        with tab1:
            st.plotly_chart(
                self.visualizer.create_factor_correlation_heatmap(explanations),
                use_container_width=True
            )

        with tab2:
            window_size = st.slider(
                "Trend Window Size",
                min_value=2,
                max_value=50,
                value=10
            )
            st.plotly_chart(
                self.visualizer.create_category_evolution(
                    explanations,
                    window_size=window_size
                ),
                use_container_width=True
            )

        with tab3:
            st.plotly_chart(
                self.visualizer.create_category_comparison(explanations),
                use_container_width=True
            )

    def _show_detailed_analysis(self, explanations: List[Explanation]):
        """Show detailed analysis for a single explanation."""
        if not explanations:
            st.warning("No explanations available for analysis.")
            return

        # Add explanation selector
        col1, col2 = st.columns([3, 1])
        with col1:
            selected_index = st.selectbox(
                "Select Explanation",
                range(len(explanations)),
                format_func=lambda i: (
                    f"{explanations[i].decision_id} - "
                    f"{explanations[i].timestamp.strftime('%Y-%m-%d %H:%M:%S')} - "
                    f"Confidence: {explanations[i].confidence:.1%}"
                )
            )
        with col2:
            st.button(
                "Compare Decisions",
                on_click=self._show_comparison_dialog,
                args=(explanations, selected_index)
            )

        explanation = explanations[selected_index]

        # Add metadata display
        with st.expander("Explanation Metadata", expanded=False):
            st.json(explanation.metadata)

        # Add tabs for different visualizations
        tab1, tab2, tab3, tab4 = st.tabs([
            "Context Influence",
            "Decision Flow",
            "Factor Values",
            "Raw Data"
        ])

        with tab1:
            # Add top-n selector
            top_n = st.slider(
                "Number of top factors to show",
                min_value=3,
                max_value=10,
                value=5
            )
            st.plotly_chart(
                self.visualizer.create_influence_chart(
                    explanation,
                    top_n=top_n
                ),
                use_container_width=True
            )

        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Network Graph")
                st.plotly_chart(
                    self.visualizer.create_decision_flow(explanation),
                    use_container_width=True
                )
            with col2:
                st.subheader("Sankey Diagram")
                st.plotly_chart(
                    self.visualizer.create_decision_sankey(explanation),
                    use_container_width=True
                )

        with tab3:
            col1, col2 = st.columns([1, 3])
            with col1:
                # Add factor selector
                factor_name = st.selectbox(
                    "Select Factor",
                    options=list(explanation.context_influence.keys())
                )
                # Add factor details
                factor = explanation.context_influence[factor_name]
                st.metric("Influence Score", f"{factor.influence_score:.1%}")
                st.metric("Confidence", f"{factor.confidence:.1%}")
                st.metric("Category", factor.category)

            with col2:
                st.plotly_chart(
                    self.visualizer.create_factor_value_distribution(
                        explanations,
                        factor_name
                    ),
                    use_container_width=True
                )

        with tab4:
            st.json(self.engine.visualize_explanation(explanation.decision_id))

    def _show_comparison_dialog(
        self,
        explanations: List[Explanation],
        current_index: int
    ):
        """Show dialog for comparing decisions."""
        st.session_state.show_comparison = True
        st.session_state.comparison_index1 = current_index

    def _show_comparison(self, explanations: List[Explanation]):
        """Show comparison between two decisions."""
        if not hasattr(st.session_state, 'show_comparison'):
            return

        if st.session_state.show_comparison:
            with st.sidebar:
                st.subheader("Decision Comparison")

                # Add second explanation selector
                selected_index2 = st.selectbox(
                    "Compare with",
                    range(len(explanations)),
                    format_func=lambda i: (
                        f"{explanations[i].decision_id} - "
                        f"{explanations[i].timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
                    )
                )

                if st.button("Close Comparison"):
                    st.session_state.show_comparison = False
                    return

                # Show comparison visualization
                st.plotly_chart(
                    self.visualizer.create_decision_comparison(
                        explanations[st.session_state.comparison_index1],
                        explanations[selected_index2]
                    ),
                    use_container_width=True
                )
