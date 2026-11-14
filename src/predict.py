import argparse
from pathlib import Path
import joblib
from src.features import make_features

ROOT = Path(__file__).resolve().parents[1]


def predict(pickup, dropoff, hour, weekday, model_path=None):
    model_path = Path(model_path or ROOT / "models/taxi_model.joblib")
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found: {model_path}. Run training first.")
    model = joblib.load(model_path)  # Only load trusted local model files.
    result = float(model.predict(make_features(pickup, dropoff, hour, weekday))[0])
    return max(0.0, result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pickup", type=int, default=161)
    parser.add_argument("--dropoff", type=int, default=132)
    parser.add_argument("--hour", type=int, default=8)
    parser.add_argument("--weekday", type=int, default=0)
    args = parser.parse_args()
    print(f"Estimated trip: {predict(args.pickup, args.dropoff, args.hour, args.weekday):.1f} minutes")
