# Visualization Features

IntelliAgent provides rich visualization capabilities for analyzing and understanding decision explanations.

## Available Visualizations

### Influence Chart

Shows the relative influence of different context factors on the decision:

```python
from intelliagent.visualization import ExplanationVisualizer

visualizer = ExplanationVisualizer()
chart = visualizer.create_influence_chart(explanation)
```

### Confidence Trend

Visualizes how decision confidence changes over time:

```python
chart = visualizer.create_confidence_trend(explanations, window=timedelta(days=7))
```

### Category Distribution

Shows the distribution of different context factor categories:

```python
chart = visualizer.create_category_distribution(explanations)
```

### Decision Flow

Creates a network graph showing how context factors lead to the final decision:

```python
chart = visualizer.create_decision_flow(explanation)
```

### Correlation Analysis

Analyze correlations between different context factors:

```python
chart = visualizer.create_factor_correlation_heatmap(explanations)
```

The correlation heatmap shows how different factors influence each other across multiple decisions. This can help identify patterns and relationships between context factors.

### Decision Timeline

Visualize how decisions and their confidence levels change over time:

```python
chart = visualizer.create_decision_timeline(explanations, window=timedelta(days=7))
```

The timeline visualization includes:

- Confidence trend line
- Decision type markers
- Top influencing factors
- Interactive tooltips with detailed information

## Interactive Dashboard

The dashboard provides an interactive interface for exploring explanations:

```python
from intelliagent.visualization import ExplanationDashboard

dashboard = ExplanationDashboard(engine)
dashboard.run()
```

Features include:

- Time-based filtering
- Overview metrics
- Interactive visualizations
- Detailed explanation analysis

## Dashboard Features

### Overview

- Total decisions made
- Average confidence
- Unique categories
- Average reasoning steps

### Timeline View

Shows the temporal progression of decisions with:

- Confidence trends
- Decision type distribution
- Top factors over time

### Correlation Analysis

Provides insights into:

- Factor relationships
- Influence patterns
- Category correlations

### Detailed Analysis

For specific decisions:

- Context influence breakdown
- Decision flow visualization
- Raw explanation data
