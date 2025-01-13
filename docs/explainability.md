# Explainability in IntelliAgent

The explainability system in IntelliAgent provides detailed insights into the decision-making process. It tracks and explains how different factors influence decisions and provides visualizations of the reasoning process.

## Features

### Context Influence Analysis

The system analyzes how different context factors influence the final decision:

```python
from intelliagent import ExplainabilityEngine

engine = ExplainabilityEngine()
explanation = engine.generate_explanation(decision, context, thought_chain, confidence)
print(explanation.context_influence)
```

### Visualization

You can visualize explanations in a human-readable format:

```python
visualization = engine.visualize_explanation(explanation.decision_id)
print(visualization)
```

## Understanding Explanations

Each explanation includes:

- Decision ID
- Reasoning steps
- Supporting evidence
- Confidence scores
- Context influence analysis
- Metadata
- Timestamp

## Best Practices

1. Always provide comprehensive context
2. Use meaningful thought chains
3. Track explanation IDs for future reference
4. Review context influence scores
5. Store important explanations
