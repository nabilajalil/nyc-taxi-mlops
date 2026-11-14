from app.app import app


def test_index():
    client = app.test_client()
    assert client.get("/").status_code == 200


def test_bad_payload():
    client = app.test_client()
    assert client.post("/predict", json={"PULocationID": 1}).status_code == 400


def test_valid_prediction_with_mock(monkeypatch):
    class FakeModel:
        def predict(self, x):
            return [12.5]
    monkeypatch.setattr("app.app.get_model", lambda: FakeModel())
    client = app.test_client()
    r = client.post("/predict", json={"PULocationID": 161, "DOLocationID": 132, "pickup_hour": 8, "day_of_week": 0})
    assert r.status_code == 200
    assert r.json["predicted_duration_minutes"] == 12.5
