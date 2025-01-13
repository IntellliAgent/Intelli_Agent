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

### Decision Flow Visualizations

The decision flow can be visualized in two ways:

1. Network Graph:

```python
chart = visualizer.create_decision_flow(explanation)
```

2. Sankey Diagram:

```python
chart = visualizer.create_decision_sankey(explanation)
```

The Sankey diagram provides an alternative view of the decision flow, showing:

- Factor influence as flow width
- Clear progression through reasoning steps
- Color-coded nodes for factors, steps, and decisions

### Factor Importance Trend

Track how the importance of different context factors changes over time:

```python
chart = visualizer.create_factor_importance_trend(explanations, top_n=5)
```

This visualization helps identify:

- Which factors consistently have high influence
- How factor importance evolves over time
- Patterns in factor relationships
- Sudden changes in factor importance

The chart includes:

- Lines for top N most influential factors
- Interactive tooltips with detailed information
- Unified hover mode for easy comparison
- Clear legend for factor identification

### Confidence Distribution

Analyze the distribution of decision confidence levels:

```python
chart = visualizer.create_confidence_distribution(explanations)
```

This visualization includes:

- Histogram of confidence values
- Kernel Density Estimation (KDE) curve
- Mean confidence line
- Interactive tooltips with density information

The distribution analysis helps identify:

- Common confidence ranges
- Unusual confidence values
- Overall decision certainty patterns
- Potential biases in confidence assessment

### Factor Value Distribution

Analyze how different values of a factor affect its influence:

```python
chart = visualizer.create_factor_value_distribution(explanations, factor_name="temperature")
```

This visualization includes:

- Scatter plot of factor values vs influence
- Color-coded confidence levels
- Trend line for numeric values
- Interactive tooltips with detailed information

The value distribution analysis helps identify:

- Value ranges with high influence
- Correlation between values and influence
- Confidence patterns across values
- Potential value thresholds

### Decision Outcome Analysis

Analyze the relationship between decisions and their outcomes:

```python
chart = visualizer.create_outcome_analysis(explanations)
```

This visualization includes:

- Outcome distribution by decision type
- Confidence vs outcome analysis
- Interactive tooltips with detailed information
- Combined view of multiple outcome metrics

The outcome analysis helps identify:

- Success rates for different decision types
- Confidence patterns for successful/failed decisions
- Decision type effectiveness
- Potential areas for improvement

### Decision Comparison

Compare two decisions side by side:

```python
chart = visualizer.create_decision_comparison(explanation1, explanation2)
```

This visualization includes:

- Factor influence comparison
- Confidence breakdown with delta
- Category distribution comparison
- Side-by-side reasoning steps

The comparison helps identify:

- Differences in factor influence
- Confidence variations
- Category distribution changes
- Reasoning step variations

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

## Interactive Features

The dashboard includes several interactive features:

- Time window selection
- Visualization type switching
- Decision comparison tool
- Factor selection and filtering
- Interactive tooltips and legends
- Expandable metadata view
- Customizable chart parameters
