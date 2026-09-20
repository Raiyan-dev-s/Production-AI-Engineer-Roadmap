import time
from collections import deque
from dataclasses import dataclass, field

from app.monitoring.logger import setup_logging

logger = setup_logging(__name__)


@dataclass
class RequestMetric:
    model: str
    latency_ms: float
    success: bool
    timestamp: float = field(default_factory=time.time)


class MetricsCollector:
    """Collects and computes metrics for monitoring.

    Tracks:
    - Request count (total, per model)
    - Error count and rate
    - Latency (avg, p95, p99)
    - Tokens per second (TODO)

    TODO: Integrate with observability platforms:
    - Prometheus + Grafana
    - Datadog
    - New Relic
    - OpenTelemetry
    """

    def __init__(self, window_size: int = 1000):
        self._requests: deque[RequestMetric] = deque(maxlen=window_size)
        self._start_time = time.time()

    def record_request(
        self,
        model: str,
        latency_ms: float,
        success: bool,
    ) -> None:
        """Record a single request metric."""
        metric = RequestMetric(
            model=model,
            latency_ms=latency_ms,
            success=success,
        )
        self._requests.append(metric)

        if not success:
            logger.warning(
                f"Failed request to model={model}, latency={latency_ms:.1f}ms"
            )

    def get_summary(self) -> dict:
        """Get a summary of collected metrics."""
        if not self._requests:
            return {
                "total_requests": 0,
                "total_errors": 0,
                "error_rate": 0.0,
                "avg_latency_ms": 0.0,
                "p95_latency_ms": 0.0,
                "p99_latency_ms": 0.0,
                "uptime_seconds": time.time() - self._start_time,
            }

        latencies = sorted(r.latency_ms for r in self._requests)
        total = len(self._requests)
        errors = sum(1 for r in self._requests if not r.success)

        return {
            "total_requests": total,
            "total_errors": errors,
            "error_rate": round(errors / total, 4) if total else 0.0,
            "avg_latency_ms": round(sum(latencies) / total, 2),
            "p95_latency_ms": round(self._percentile(latencies, 0.95), 2),
            "p99_latency_ms": round(self._percentile(latencies, 0.99), 2),
            "uptime_seconds": round(time.time() - self._start_time, 1),
        }

    def get_model_metrics(self) -> dict[str, dict]:
        """Get per-model metrics."""
        model_metrics: dict[str, list[RequestMetric]] = {}
        for r in self._requests:
            model_metrics.setdefault(r.model, []).append(r)

        result = {}
        for model, metrics in model_metrics.items():
            latencies = sorted(m.latency_ms for m in metrics)
            result[model] = {
                "requests": len(metrics),
                "errors": sum(1 for m in metrics if not m.success),
                "avg_latency_ms": round(sum(latencies) / len(latencies), 2),
            }
        return result

    @staticmethod
    def _percentile(sorted_data: list[float], percentile: float) -> float:
        """Compute a percentile from sorted data."""
        if not sorted_data:
            return 0.0
        index = int(len(sorted_data) * percentile)
        index = min(index, len(sorted_data) - 1)
        return sorted_data[index]
