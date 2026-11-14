"""Prometheus service metrics exposed at /metrics by Flask."""
from prometheus_client import Counter, Histogram
REQUESTS = Counter('taxi_prediction_requests_total', 'Prediction requests', ['status'])
LATENCY = Histogram('taxi_prediction_duration_seconds', 'Prediction inference latency')
