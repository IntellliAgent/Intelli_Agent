"""Visualization module for IntelliAgent.

This module provides visualization capabilities for analyzing and understanding
decision explanations. It includes various chart types and analysis tools.

Typical usage example:

    visualizer = ExplanationVisualizer()
    chart = visualizer.create_influence_chart(explanation)
    chart.show()
"""

from typing import List, Optional, Tuple, Dict, Any, Union
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import networkx as nx
from datetime import datetime, timedelta

from ..core.explainability import Explanation, ContextFactor


class ExplanationVisualizer:
    """Handles visualization of explanations and analysis.

    This class provides methods for creating various visualizations to analyze
    decision explanations, including influence charts, timelines, correlation
    analysis, and more.

    Attributes:
        None

    Methods:
        create_influence_chart: Creates a bar chart showing factor influence.
        create_decision_flow: Creates a network graph of the decision process.
        create_factor_correlation_heatmap: Creates a correlation matrix heatmap.
        create_decision_timeline: Creates a timeline visualization.
        ...
    """

    def create_influence_chart(
        self,
        explanation: Explanation,
        top_n: int = 5,
        color_scale: Optional[str] = 'Viridis'
    ) -> go.Figure:
        """Creates an influence chart for context factors.

        Generates a bar chart showing the relative influence of different context
        factors on the decision, sorted by influence score.

        Args:
            explanation: The explanation to visualize.
            top_n: Number of top factors to show. Defaults to 5.
            color_scale: Plotly color scale to use. Defaults to 'Viridis'.

        Returns:
            A plotly Figure object containing the influence chart.

        Raises:
            ValueError: If explanation has no context factors.
        """
        if not explanation.context_influence:
            raise ValueError("Explanation has no context factors")

        # Sort factors by influence score
        factors = sorted(
            explanation.context_influence.items(),
            key=lambda x: x[1].influence_score,
            reverse=True
        )[:top_n]

        # Create bar chart
        fig = go.Figure([
            go.Bar(
                x=[f[0] for f in factors],
                y=[f[1].influence_score for f in factors],
                text=[f"{f[1].influence_score:.2%}" for f in factors],
                textposition='auto',
                hovertemplate=(
                    "Factor: %{x}<br>"
                    "Influence: %{y:.2%}<br>"
                    "Category: %{customdata}<br>"
                    "<extra></extra>"
                ),
                customdata=[f[1].category for f in factors]
            )
        ])

        fig.update_layout(
            title="Top Context Factors by Influence",
            xaxis_title="Factors",
            yaxis_title="Influence Score",
            showlegend=False
        )

        return fig

    def create_confidence_trend(
        self,
        explanations: List[Explanation],
        window: Optional[timedelta] = None
    ) -> go.Figure:
        """Create a confidence trend visualization.

        Args:
            explanations: List of explanations to analyze
            window: Optional time window to filter

        Returns:
            go.Figure: Plotly figure object
        """
        if window:
            cutoff = datetime.now() - window
            explanations = [
                exp for exp in explanations
                if exp.timestamp >= cutoff
            ]

        # Create dataframe
        df = pd.DataFrame([
            {
                'timestamp': exp.timestamp,
                'confidence': exp.confidence,
                'decision_type': exp.metadata['decision_type']
            }
            for exp in explanations
        ])

        # Create line plot
        fig = px.line(
            df,
            x='timestamp',
            y='confidence',
            color='decision_type',
            title='Confidence Trend Over Time'
        )

        fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Confidence Score",
            hovermode='x unified'
        )

        return fig

    def create_category_distribution(
        self,
        explanations: List[Explanation]
    ) -> go.Figure:
        """Create a category distribution visualization.

        Args:
            explanations: List of explanations to analyze

        Returns:
            go.Figure: Plotly figure object
        """
        # Collect category data
        categories = {}
        for exp in explanations:
            for factor in exp.context_influence.values():
                if factor.category not in categories:
                    categories[factor.category] = {
                        'count': 0,
                        'total_influence': 0
                    }
                categories[factor.category]['count'] += 1
                categories[factor.category]['total_influence'] += factor.influence_score

        # Create sunburst chart
        fig = go.Figure(go.Sunburst(
            labels=list(categories.keys()),
            parents=[''] * len(categories),
            values=[data['count'] for data in categories.values()],
            branchvalues='total',
            hovertemplate=(
                "Category: %{label}<br>"
                "Count: %{value}<br>"
                "Avg Influence: %{customdata:.2%}<br>"
                "<extra></extra>"
            ),
            customdata=[
                data['total_influence'] / data['count']
                for data in categories.values()
            ]
        ))

        fig.update_layout(
            title="Context Factor Category Distribution"
        )

        return fig

    def create_decision_flow(
        self,
        explanation: Explanation
    ) -> go.Figure:
        """Create a decision flow visualization.

        Args:
            explanation: The explanation to visualize

        Returns:
            go.Figure: Plotly figure object
        """
        # Create nodes for steps
        nodes = []
        edges = []

        # Add context nodes
        for i, (name, factor) in enumerate(explanation.context_influence.items()):
            nodes.append(f"Context: {name}")
            edges.append(("Context", f"Context: {name}"))

        # Add reasoning steps
        for i, step in enumerate(explanation.reasoning_steps):
            nodes.append(f"Step {i+1}: {step}")
            if i == 0:
                # Connect first step to all context factors
                for node in nodes[:-1]:
                    edges.append((node, f"Step {i+1}: {step}"))
            else:
                # Connect to previous step
                edges.append((
                    f"Step {i}: {explanation.reasoning_steps[i-1]}",
                    f"Step {i+1}: {step}"
                ))

        # Create network graph
        return self._create_network_graph(nodes, edges)

    def _create_network_graph(
        self,
        nodes: List[str],
        edges: List[Tuple[str, str]]
    ) -> go.Figure:
        """Create a network graph visualization.

        Args:
            nodes: List of node labels
            edges: List of (source, target) tuples

        Returns:
            go.Figure: Network graph visualization
        """
        # Create graph
        G = nx.DiGraph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        # Use spring layout for node positions
        pos = nx.spring_layout(G)

        # Extract node positions
        node_x = []
        node_y = []
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)

        # Create edges
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        # Create figure
        fig = go.Figure()

        # Add edges
        fig.add_trace(go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines'
        ))

        # Add nodes
        fig.add_trace(go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=nodes,
            textposition="top center",
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                )
            )
        ))

        # Update layout
        fig.update_layout(
            title="Decision Flow Network",
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )

        return fig

    def create_factor_correlation_heatmap(
        self,
        explanations: List[Explanation]
    ) -> go.Figure:
        """Create a heatmap showing correlations between context factors.

        Args:
            explanations: List of explanations to analyze

        Returns:
            go.Figure: Correlation heatmap
        """
        # Collect all unique factors
        all_factors = set()
        for exp in explanations:
            all_factors.update(exp.context_influence.keys())

        # Create correlation matrix
        factor_list = sorted(all_factors)
        n_factors = len(factor_list)
        correlations = np.zeros((n_factors, n_factors))

        # Calculate correlations
        for i, factor1 in enumerate(factor_list):
            for j, factor2 in enumerate(factor_list):
                if i == j:
                    correlations[i][j] = 1.0
                    continue

                # Get influence scores for both factors
                scores1 = []
                scores2 = []
                for exp in explanations:
                    if (factor1 in exp.context_influence and
                            factor2 in exp.context_influence):
                        scores1.append(exp.context_influence[factor1].influence_score)
                        scores2.append(exp.context_influence[factor2].influence_score)

                # Calculate correlation if we have enough data
                if len(scores1) > 1:
                    correlations[i][j] = np.corrcoef(scores1, scores2)[0, 1]

        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=correlations,
            x=factor_list,
            y=factor_list,
            colorscale='RdBu',
            zmid=0,
            text=np.round(correlations, 2),
            texttemplate='%{text}',
            textfont={"size": 10},
            hoverongaps=False
        ))

        fig.update_layout(
            title="Context Factor Correlation Heatmap",
            xaxis_title="Factors",
            yaxis_title="Factors",
            height=800
        )

        return fig

    def create_decision_timeline(
        self,
        explanations: List[Explanation],
        window: Optional[timedelta] = None
    ) -> go.Figure:
        """Create a timeline visualization of decisions.

        Args:
            explanations: List of explanations to visualize
            window: Optional time window to filter

        Returns:
            go.Figure: Timeline visualization
        """
        if window:
            cutoff = datetime.now() - window
            explanations = [
                exp for exp in explanations
                if exp.timestamp >= cutoff
            ]

        # Create timeline data
        data = []
        for exp in explanations:
            # Get top factor
            top_factor = max(
                exp.context_influence.items(),
                key=lambda x: x[1].influence_score
            )

            data.append({
                'timestamp': exp.timestamp,
                'decision_id': exp.decision_id,
                'confidence': exp.confidence,
                'top_factor': top_factor[0],
                'factor_influence': top_factor[1].influence_score,
                'decision_type': exp.metadata['decision_type']
            })

        df = pd.DataFrame(data)

        # Create figure
        fig = go.Figure()

        # Add confidence line
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['confidence'],
            mode='lines+markers',
            name='Confidence',
            hovertemplate=(
                "Time: %{x}<br>"
                "Confidence: %{y:.2%}<br>"
                "Decision ID: %{customdata[0]}<br>"
                "Top Factor: %{customdata[1]}<br>"
                "<extra></extra>"
            ),
            customdata=df[['decision_id', 'top_factor']].values
        ))

        # Add decision type markers
        for decision_type in df['decision_type'].unique():
            mask = df['decision_type'] == decision_type
            fig.add_trace(go.Scatter(
                x=df[mask]['timestamp'],
                y=df[mask]['confidence'],
                mode='markers',
                name=decision_type,
                marker=dict(size=12),
                showlegend=True
            ))

        fig.update_layout(
            title="Decision Timeline",
            xaxis_title="Time",
            yaxis_title="Confidence",
            hovermode='closest'
        )

        return fig

    def create_decision_sankey(
        self,
        explanation: Explanation
    ) -> go.Figure:
        """Create a Sankey diagram of the decision flow.

        Args:
            explanation: The explanation to visualize

        Returns:
            go.Figure: Sankey diagram
        """
        # Prepare nodes and links
        nodes = []
        links = []
        node_indices = {}
        current_index = 0

        # Add context factors as source nodes
        for name, factor in explanation.context_influence.items():
            nodes.append({
                "label": f"Factor: {name}",
                "color": "blue"
            })
            node_indices[name] = current_index
            current_index += 1

        # Add reasoning steps as intermediate nodes
        for i, step in enumerate(explanation.reasoning_steps):
            nodes.append({
                "label": f"Step {i+1}: {step}",
                "color": "green"
            })
            node_indices[f"step_{i}"] = current_index
            current_index += 1

        # Add final decision node
        nodes.append({
            "label": "Decision",
            "color": "red"
        })
        decision_index = current_index

        # Create links from factors to first step
        for name, factor in explanation.context_influence.items():
            links.append({
                "source": node_indices[name],
                "target": node_indices["step_0"],
                "value": factor.influence_score,
                "color": "rgba(0,0,255,0.2)"
            })

        # Create links between steps
        for i in range(len(explanation.reasoning_steps) - 1):
            links.append({
                "source": node_indices[f"step_{i}"],
                "target": node_indices[f"step_{i+1}"],
                "value": 1,
                "color": "rgba(0,255,0,0.2)"
            })

        # Create link from last step to decision
        last_step = len(explanation.reasoning_steps) - 1
        if last_step >= 0:
            links.append({
                "source": node_indices[f"step_{last_step}"],
                "target": decision_index,
                "value": 1,
                "color": "rgba(255,0,0,0.2)"
            })

        # Create figure
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=[node["label"] for node in nodes],
                color=[node["color"] for node in nodes]
            ),
            link=dict(
                source=[link["source"] for link in links],
                target=[link["target"] for link in links],
                value=[link["value"] for link in links],
                color=[link["color"] for link in links]
            )
        )])

        fig.update_layout(
            title="Decision Flow (Sankey Diagram)",
            font_size=10,
            height=600
        )

        return fig

    def create_factor_importance_trend(
        self,
        explanations: List[Explanation],
        top_n: int = 5
    ) -> go.Figure:
        """Create a visualization of how factor importance changes over time.

        Args:
            explanations: List of explanations to analyze
            top_n: Number of top factors to track

        Returns:
            go.Figure: Factor importance trend visualization
        """
        # Get all factors and their total influence
        factor_totals = {}
        for exp in explanations:
            for name, factor in exp.context_influence.items():
                if name not in factor_totals:
                    factor_totals[name] = 0
                factor_totals[name] += factor.influence_score

        # Get top N factors
        top_factors = sorted(
            factor_totals.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_n]
        top_factor_names = [f[0] for f in top_factors]

        # Create timeline data
        data = []
        for exp in sorted(explanations, key=lambda x: x.timestamp):
            row = {'timestamp': exp.timestamp}
            for factor in top_factor_names:
                if factor in exp.context_influence:
                    row[factor] = exp.context_influence[factor].influence_score
                else:
                    row[factor] = 0
            data.append(row)

        df = pd.DataFrame(data)

        # Create figure
        fig = go.Figure()

        # Add line for each factor
        for factor in top_factor_names:
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df[factor],
                mode='lines+markers',
                name=factor,
                hovertemplate=(
                    "Time: %{x}<br>"
                    f"{factor}: %{{y:.2%}}<br>"
                    "<extra></extra>"
                )
            ))

        fig.update_layout(
            title="Factor Importance Trend",
            xaxis_title="Time",
            yaxis_title="Influence Score",
            hovermode='x unified',
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )

        return fig

    def create_category_evolution(
        self,
        explanations: List[Explanation],
        window_size: int = 10
    ) -> go.Figure:
        """Create a visualization of how categories evolve over time.

        Args:
            explanations: List of explanations to analyze
            window_size: Size of the rolling window for trend analysis

        Returns:
            go.Figure: Category evolution visualization
        """
        # Sort explanations by time
        sorted_exps = sorted(explanations, key=lambda x: x.timestamp)

        # Collect category data over time
        data = []
        for exp in sorted_exps:
            categories = {}
            total_influence = 0

            for factor in exp.context_influence.values():
                if factor.category not in categories:
                    categories[factor.category] = 0
                categories[factor.category] += factor.influence_score
                total_influence += factor.influence_score

            # Normalize influence scores
            if total_influence > 0:
                for category in categories:
                    categories[category] /= total_influence

            data.append({
                'timestamp': exp.timestamp,
                **categories
            })

        df = pd.DataFrame(data).fillna(0)

        # Calculate rolling averages
        for col in df.columns:
            if col != 'timestamp':
                df[f'{col}_rolling'] = df[col].rolling(window=window_size).mean()

        # Create figure
        fig = go.Figure()

        # Add area traces for each category
        categories = [col for col in df.columns if col != 'timestamp']
        for category in categories:
            if category.endswith('_rolling'):
                continue

            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df[category],
                name=category,
                mode='lines',
                stackgroup='one',
                hovertemplate=(
                    "Time: %{x}<br>"
                    f"{category}: %{{y:.1%}}<br>"
                    "<extra></extra>"
                )
            ))

            # Add rolling average line
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df[f'{category}_rolling'],
                name=f'{category} (trend)',
                line=dict(dash='dot'),
                visible='legendonly'
            ))

        fig.update_layout(
            title="Category Influence Evolution",
            xaxis_title="Time",
            yaxis_title="Relative Influence",
            hovermode='x unified',
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )

        return fig

    def create_confidence_distribution(
        self,
        explanations: List[Explanation]
    ) -> go.Figure:
        """Create a visualization of confidence distribution.

        Args:
            explanations: List of explanations to analyze

        Returns:
            go.Figure: Confidence distribution visualization
        """
        # Get confidence values
        confidences = [exp.confidence for exp in explanations]

        # Create histogram and KDE
        fig = go.Figure()

        # Add histogram
        fig.add_trace(go.Histogram(
            x=confidences,
            name="Histogram",
            histnorm='probability density',
            opacity=0.7,
            nbinsx=20,
            hovertemplate=(
                "Confidence: %{x:.1%}<br>"
                "Density: %{y:.3f}<br>"
                "<extra></extra>"
            )
        ))

        # Add KDE (using numpy's histogram and gaussian_filter)
        hist, bin_edges = np.histogram(
            confidences,
            bins=50,
            density=True
        )
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

        from scipy.ndimage import gaussian_filter
        smoothed = gaussian_filter(hist, sigma=1.5)

        fig.add_trace(go.Scatter(
            x=bin_centers,
            y=smoothed,
            name="KDE",
            line=dict(width=2),
            hovertemplate=(
                "Confidence: %{x:.1%}<br>"
                "Density: %{y:.3f}<br>"
                "<extra></extra>"
            )
        ))

        # Add mean line
        mean_confidence = np.mean(confidences)
        fig.add_vline(
            x=mean_confidence,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Mean: {mean_confidence:.1%}"
        )

        fig.update_layout(
            title="Confidence Distribution",
            xaxis_title="Confidence",
            yaxis_title="Density",
            showlegend=True,
            bargap=0.1
        )

        return fig

    def create_category_comparison(
        self,
        explanations: List[Explanation]
    ) -> go.Figure:
        """Create a visualization comparing factor categories.

        Args:
            explanations: List of explanations to analyze

        Returns:
            go.Figure: Category comparison visualization
        """
        # Collect category statistics
        categories = {}
        for exp in explanations:
            for factor in exp.context_influence.values():
                if factor.category not in categories:
                    categories[factor.category] = {
                        'count': 0,
                        'total_influence': 0,
                        'total_confidence': 0,
                        'high_influence_count': 0  # Count of times influence > 0.5
                    }

                cat_stats = categories[factor.category]
                cat_stats['count'] += 1
                cat_stats['total_influence'] += factor.influence_score
                cat_stats['total_confidence'] += factor.confidence
                if factor.influence_score > 0.5:
                    cat_stats['high_influence_count'] += 1

        # Prepare data for visualization
        data = []
        for category, stats in categories.items():
            data.append({
                'Category': category,
                'Average Influence': stats['total_influence'] / stats['count'],
                'Average Confidence': stats['total_confidence'] / stats['count'],
                'High Influence Rate': stats['high_influence_count'] / stats['count'],
                'Usage Count': stats['count']
            })

        df = pd.DataFrame(data)

        # Create parallel coordinates plot
        fig = go.Figure(data=go.Parcoords(
            line=dict(
                color=df['Usage Count'],
                colorscale='Viridis'
            ),
            dimensions=[
                dict(
                    range=[0, 1],
                    label='Average Influence',
                    values=df['Average Influence']
                ),
                dict(
                    range=[0, 1],
                    label='Average Confidence',
                    values=df['Average Confidence']
                ),
                dict(
                    range=[0, 1],
                    label='High Influence Rate',
                    values=df['High Influence Rate']
                ),
                dict(
                    range=[df['Usage Count'].min(), df['Usage Count'].max()],
                    label='Usage Count',
                    values=df['Usage Count']
                )
            ]
        ))

        fig.update_layout(
            title="Category Comparison (Parallel Coordinates)",
            height=500,
            showlegend=False
        )

        return fig

    def create_factor_value_distribution(
        self,
        explanations: List[Explanation],
        factor_name: str
    ) -> go.Figure:
        """Create a visualization of value distribution for a specific factor.

        Args:
            explanations: List of explanations to analyze
            factor_name: Name of the factor to analyze

        Returns:
            go.Figure: Factor value distribution visualization
        """
        # Collect factor values and their influence
        values = []
        influences = []
        confidences = []

        for exp in explanations:
            if factor_name in exp.context_influence:
                factor = exp.context_influence[factor_name]
                values.append(factor.value)
                influences.append(factor.influence_score)
                confidences.append(factor.confidence)

        # Create figure
        fig = go.Figure()

        # Add scatter plot
        fig.add_trace(go.Scatter(
            x=values,
            y=influences,
            mode='markers',
            marker=dict(
                size=10,
                color=confidences,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Confidence")
            ),
            name='Values',
            hovertemplate=(
                "Value: %{x}<br>"
                "Influence: %{y:.2%}<br>"
                "Confidence: %{marker.color:.2%}<br>"
                "<extra></extra>"
            )
        ))

        # Add trend line if numeric values
        if all(isinstance(v, (int, float)) for v in values):
            z = np.polyfit(values, influences, 1)
            p = np.poly1d(z)
            x_range = np.linspace(min(values), max(values), 100)

            fig.add_trace(go.Scatter(
                x=x_range,
                y=p(x_range),
                mode='lines',
                name='Trend',
                line=dict(dash='dash')
            ))

        fig.update_layout(
            title=f"Value Distribution for {factor_name}",
            xaxis_title="Factor Value",
            yaxis_title="Influence Score",
            showlegend=True
        )

        return fig

    def create_outcome_analysis(
        self,
        explanations: List[Explanation]
    ) -> go.Figure:
        """Create a visualization analyzing decision outcomes.

        Args:
            explanations: List of explanations to analyze

        Returns:
            go.Figure: Decision outcome analysis visualization
        """
        # Collect outcome data
        data = []
        for exp in explanations:
            outcome = exp.metadata.get('outcome', 'unknown')
            data.append({
                'timestamp': exp.timestamp,
                'confidence': exp.confidence,
                'outcome': outcome,
                'decision_type': exp.metadata.get('decision_type', 'unknown'),
                'top_factor': max(
                    exp.context_influence.items(),
                    key=lambda x: x[1].influence_score
                )[0]
            })

        df = pd.DataFrame(data)

        # Create figure with secondary y-axis
        fig = make_subplots(
            rows=2,
            cols=1,
            subplot_titles=(
                "Outcome Distribution by Decision Type",
                "Confidence vs Outcome"
            ),
            vertical_spacing=0.2
        )

        # Add outcome distribution
        outcome_counts = df.groupby(['decision_type', 'outcome']).size().unstack()
        fig.add_trace(
            go.Bar(
                x=outcome_counts.index,
                y=outcome_counts[col],
                name=col,
                hovertemplate=(
                    "Decision Type: %{x}<br>"
                    f"Outcome: {col}<br>"
                    "Count: %{y}<br>"
                    "<extra></extra>"
                )
            ) for col in outcome_counts.columns
        )

        # Add confidence vs outcome box plot
        fig.add_trace(
            go.Box(
                x=df['outcome'],
                y=df['confidence'],
                name='Confidence',
                boxpoints='all',
                jitter=0.3,
                pointpos=-1.8,
                hovertemplate=(
                    "Outcome: %{x}<br>"
                    "Confidence: %{y:.2%}<br>"
                    "<extra></extra>"
                )
            ),
            row=2,
            col=1
        )

        # Update layout
        fig.update_layout(
            title="Decision Outcome Analysis",
            showlegend=True,
            height=800,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )

        # Update y-axes
        fig.update_yaxes(title_text="Count", row=1, col=1)
        fig.update_yaxes(title_text="Confidence", row=2, col=1)

        return fig

    def create_decision_comparison(
        self,
        explanation1: Explanation,
        explanation2: Explanation
    ) -> go.Figure:
        """Create a visualization comparing two decisions.

        Args:
            explanation1: First explanation to compare
            explanation2: Second explanation to compare

        Returns:
            go.Figure: Decision comparison visualization
        """
        # Create figure with subplots
        fig = make_subplots(
            rows=2,
            cols=2,
            subplot_titles=(
                "Factor Influence Comparison",
                "Confidence Breakdown",
                "Category Distribution",
                "Reasoning Steps"
            )
        )

        # Get common factors
        all_factors = set(explanation1.context_influence.keys()) | set(
            explanation2.context_influence.keys()
        )

        # Add factor influence comparison
        factors1 = [
            explanation1.context_influence.get(
                f, ContextFactor(name=f, value="", influence_score=0,
                                 confidence=0, category="")
            ).influence_score
            for f in all_factors
        ]
        factors2 = [
            explanation2.context_influence.get(
                f, ContextFactor(name=f, value="", influence_score=0,
                                 confidence=0, category="")
            ).influence_score
            for f in all_factors
        ]

        fig.add_trace(
            go.Bar(
                name="Decision 1",
                x=list(all_factors),
                y=factors1,
                text=[f"{v:.1%}" for v in factors1],
                textposition='auto',
            ),
            row=1,
            col=1
        )
        fig.add_trace(
            go.Bar(
                name="Decision 2",
                x=list(all_factors),
                y=factors2,
                text=[f"{v:.1%}" for v in factors2],
                textposition='auto',
            ),
            row=1,
            col=1
        )

        # Add confidence breakdown
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=explanation1.confidence,
                delta={'reference': explanation2.confidence},
                gauge={'axis': {'range': [0, 1]}},
                title={'text': "Confidence Comparison"}
            ),
            row=1,
            col=2
        )

        # Add category distribution
        categories1 = {}
        categories2 = {}
        for f in explanation1.context_influence.values():
            categories1[f.category] = categories1.get(f.category, 0) + 1
        for f in explanation2.context_influence.values():
            categories2[f.category] = categories2.get(f.category, 0) + 1

        fig.add_trace(
            go.Pie(
                labels=list(categories1.keys()),
                values=list(categories1.values()),
                name="Decision 1",
                domain={'x': [0, 0.45], 'y': [0, 0.45]},
                showlegend=False
            ),
            row=2,
            col=1
        )
        fig.add_trace(
            go.Pie(
                labels=list(categories2.keys()),
                values=list(categories2.values()),
                name="Decision 2",
                domain={'x': [0.55, 1], 'y': [0, 0.45]},
                showlegend=False
            ),
            row=2,
            col=1
        )

        # Add reasoning steps comparison
        steps1 = [f"Step {i+1}" for i in range(len(explanation1.reasoning_steps))]
        steps2 = [f"Step {i+1}" for i in range(len(explanation2.reasoning_steps))]

        fig.add_trace(
            go.Table(
                header=dict(
                    values=['Decision 1', 'Decision 2'],
                    align='center'
                ),
                cells=dict(
                    values=[explanation1.reasoning_steps, explanation2.reasoning_steps],
                    align='left'
                )
            ),
            row=2,
            col=2
        )

        # Update layout
        fig.update_layout(
            title="Decision Comparison",
            height=800,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        return fig
