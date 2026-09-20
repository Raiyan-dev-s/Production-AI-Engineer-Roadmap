"""Tests for the Production AI System."""

from app.monitoring.metrics import MetricsCollector


def test_metrics_collector_records_latency():
    """Metrics collector records latency values."""
    collector = MetricsCollector()
    collector.record_request(model="test", latency_ms=100.0, success=True)
    collector.record_request(model="test", latency_ms=200.0, success=True)
    stats = collector.get_summary()
    assert stats["total_requests"] == 2
    assert stats["avg_latency_ms"] > 0


def test_metrics_collector_records_error():
    """Metrics collector records errors."""
    collector = MetricsCollector()
    collector.record_request(model="test", latency_ms=50.0, success=False)
    stats = collector.get_summary()
    assert stats["total_errors"] == 1


def test_data_validators():
    """Input validators reject empty data."""
    import pytest

    from app.core.exceptions import ValidationError
    from app.data.validators import validate_text_input

    with pytest.raises(ValidationError):
        validate_text_input("")
