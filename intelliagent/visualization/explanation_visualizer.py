"""Visualization module for explanations."""

from typing import List, Optional, Tuple
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import networkx as nx
import numpy as np

from ..core.explainability import Explanation


class ExplanationVisualizer:
    """Handles visualization of explanations and analysis."""

    def create_influence_chart(
        self,
        explanation: Explanation,
        top_n: int = 5
    ) -> go.Figure:
        """Create an influence chart for context factors.

        Args:
            explanation: The explanation to visualize
            top_n: Number of top factors to show

        Returns:
            go.Figure: Plotly figure object
        """
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
