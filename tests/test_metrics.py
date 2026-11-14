from monitoring.metrics import REQUESTS, LATENCY

def test_metrics_exist():
    assert REQUESTS is not None
    assert LATENCY is not None
