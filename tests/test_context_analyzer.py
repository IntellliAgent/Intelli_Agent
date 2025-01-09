import pytest
from datetime import datetime, timedelta
from intelliagent.utils.context_analyzer import ContextAnalyzer


@pytest.fixture
def analyzer():
    return ContextAnalyzer()


def test_analyze_input_with_entities(analyzer):
    input_text = "Contact me at test@example.com or +1234567890. Pay $100.50"
    result = analyzer.analyze_input(input_text)

    assert "entities" in result
    assert "email" in result["entities"]
    assert "phone" in result["entities"]
    assert "money" in result["entities"]
    assert result["entities"]["email"] == ["test@example.com"]
    assert result["entities"]["phone"] == ["+1234567890"]
    assert result["entities"]["money"] == ["$100.50"]


def test_sentiment_analysis(analyzer):
    positive_text = "This is a great and excellent result!"
    negative_text = "This is a terrible and poor outcome."
    neutral_text = "This is a regular standard day."

    pos_result = analyzer.analyze_input(positive_text)
    neg_result = analyzer.analyze_input(negative_text)
    neu_result = analyzer.analyze_input(neutral_text)

    assert pos_result["sentiment"]["positive"] > pos_result["sentiment"]["negative"]
    assert neg_result["sentiment"]["negative"] > neg_result["sentiment"]["positive"]
    assert neu_result["sentiment"]["neutral"] > 0.5


def test_merge_contexts(analyzer):
    old_context = {
        "entities": ["email1@test.com"],
        "sentiment": {"positive": 0.8},
        "metadata": {"count": 1}
    }
    new_context = {
        "entities": ["email2@test.com"],
        "sentiment": {"negative": 0.6},
        "metadata": {"count": 2}
    }

    merged = analyzer.merge_contexts(old_context, new_context)

    assert len(merged["entities"]) == 2
    assert "count" in merged["metadata"]
    assert merged["metadata"]["count"] == 2


def test_context_relevance(analyzer):
    current_context = {
        "entities": {"email": ["test@example.com"]},
        "sentiment": {"positive": 0.8},
        "timestamp": datetime.now().isoformat()
    }

    old_context = {
        "entities": {"email": ["test@example.com"]},
        "sentiment": {"positive": 0.7},
        "timestamp": (datetime.now() - timedelta(days=1)).isoformat()
    }

    unrelated_context = {
        "entities": {"email": ["other@example.com"]},
        "sentiment": {"negative": 0.9},
        "timestamp": datetime.now().isoformat()
    }

    relevance_score1 = analyzer._calculate_relevance(
        old_context, current_context)
    relevance_score2 = analyzer._calculate_relevance(
        unrelated_context,
        current_context
    )

    assert relevance_score1 > relevance_score2


def test_key_points_extraction(analyzer):
    text = (
        "This is important: save money. "
        "You must invest wisely. "
        "The weather is nice today. "
        "It is critical to diversify."
    )

    result = analyzer.analyze_input(text)

    assert len(result["key_points"]) == 3
    assert any("save money" in kp for kp in result["key_points"])
    assert any("invest wisely" in kp for kp in result["key_points"])
    assert any("diversify" in kp for kp in result["key_points"])
