"""Tests for uncertainty handling system."""

import pytest
from datetime import datetime
from intelliagent.core.uncertainty_handler import (
    UncertaintyHandler,
    UncertaintyMetrics
)


@pytest.fixture
def handler():
    return UncertaintyHandler(confidence_threshold=0.7)


def test_evaluate_uncertainty_empty_predictions(handler):
    score, details = handler.evaluate_uncertainty([], {})

    assert score == 1.0
    assert "error" in details
    assert details["error"] == "No predictions available"


def test_evaluate_uncertainty_valid_predictions(handler):
    predictions = [0.8, 0.7, 0.9]
    context = {"confidence": 0.8}

    score, details = handler.evaluate_uncertainty(predictions, context)

    assert 0 <= score <= 1
    assert "metrics" in details
    assert "context_factors" in details
    assert "threshold" in details
    assert details["threshold"] == 0.7


def test_calculate_metrics(handler):
    predictions = [0.8, 0.7, 0.9]
    metrics = handler._calculate_metrics(predictions)

    assert isinstance(metrics, UncertaintyMetrics)
    assert 0 <= metrics.confidence_score <= 1
    assert metrics.entropy >= 0
    assert metrics.variance >= 0
    assert 0 <= metrics.prediction_spread <= 1


def test_compute_uncertainty_score(handler):
    metrics = UncertaintyMetrics(
        confidence_score=0.8,
        entropy=0.5,
        variance=0.1,
        prediction_spread=0.2
    )

    score = handler._compute_uncertainty_score(metrics)

    assert 0 <= score <= 1


def test_analyze_context_uncertainty_empty_context(handler):
    factors = handler._analyze_context_uncertainty({})

    assert "missing_context" in factors
    assert factors["missing_context"] == 1.0


def test_analyze_context_uncertainty_with_timestamp(handler):
    context = {
        "timestamp": datetime.now().isoformat(),
        "confidence": 0.8
    }

    factors = handler._analyze_context_uncertainty(context)

    assert "temporal_uncertainty" in factors
    assert "explicit_confidence" in factors
    assert factors["explicit_confidence"] == 0.2


def test_analyze_context_uncertainty_invalid_timestamp(handler):
    context = {
        "timestamp": "invalid_timestamp",
        "confidence": 0.8
    }

    factors = handler._analyze_context_uncertainty(context)

    assert "invalid_timestamp" in factors
    assert factors["invalid_timestamp"] == 1.0
