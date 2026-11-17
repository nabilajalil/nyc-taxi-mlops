from pathlib import Path
import os
import joblib
import mlflow
import mlflow.sklearn
from mlflow.exceptions import MlflowException
from flask import Flask, jsonify, render_template, request
from src.features import make_features
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from monitoring.metrics import REQUESTS, LATENCY
from flask import Response

ROOT = Path(__file__).resolve().parents[1]
app = Flask(__name__)
_model = None


def get_model():
    global _model

    if _model is None:
        model_uri = os.environ.get("MLFLOW_MODEL_URI")

        if model_uri:
            mlflow.set_tracking_uri(
                os.environ.get(
                    "MLFLOW_TRACKING_URI",
                    f"sqlite:///{ROOT / 'mlflow.db'}",
                )
            )

            _model = mlflow.sklearn.load_model(model_uri)

        else:
            path = Path(
                os.environ.get(
                    "MODEL_PATH",
                    str(ROOT / "models/taxi_model.joblib"),
                )
            )

            if not path.is_file():
                raise FileNotFoundError(
                    "Model unavailable; train the model before starting the service"
                )

            _model = joblib.load(path)

    return _model


def estimate(payload):
    x = make_features(payload["PULocationID"], payload["DOLocationID"], payload["pickup_hour"], payload["day_of_week"])
    with LATENCY.time():
        value = float(get_model().predict(x)[0])
    return round(max(0.0, value), 2)


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health():
    try:
        get_model()
        return jsonify(status="ok")
    except (FileNotFoundError, OSError, MlflowException):
        return jsonify(status="model_unavailable"), 503


@app.post("/predict")
def predict():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error="Expected a JSON object"), 400
    try:
        result = estimate(payload)
        REQUESTS.labels(status="success").inc()
        return jsonify(predicted_duration_minutes=result)
    except (KeyError, ValueError, TypeError) as exc:
        REQUESTS.labels(status="bad_request").inc()
        return jsonify(error=str(exc)), 400
    except (FileNotFoundError, OSError, MlflowException):
        return jsonify(error="Model unavailable"), 503

@app.post("/predict-form")
def predict_form():
    try:
        result = estimate(request.form)
        return render_template("index.html", prediction=result)
    except (KeyError, ValueError, TypeError) as exc:
        return render_template("index.html", error=str(exc)), 400
    except (FileNotFoundError, OSError, MlflowException):
        return render_template("index.html", error="Model unavailable"), 503
