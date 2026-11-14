import argparse
import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from src.features import prepare_data

ROOT = Path(__file__).resolve().parents[1]


def train(train_file, val_file, model_file):
    x_train, y_train = prepare_data(pd.read_parquet(train_file))
    x_val, y_val = prepare_data(pd.read_parquet(val_file))
    if x_train.empty or x_val.empty:
        raise ValueError("No valid records after filtering; check your input data")
    prep = ColumnTransformer([
        ("zones", OneHotEncoder(handle_unknown="ignore"), ["PULocationID", "DOLocationID"]),
        ("time", "passthrough", ["pickup_hour", "day_of_week"]),
    ])
    pipeline = Pipeline([("preprocess", prep), ("model", Ridge(alpha=1.0))])
    pipeline.fit(x_train, y_train)
    pred = pipeline.predict(x_val)
    metrics = {
        "train_rows": len(x_train), "validation_rows": len(x_val),
        "median_baseline_mae": float(mean_absolute_error(y_val, np.full(len(y_val), y_train.median()))),
        "mae": float(mean_absolute_error(y_val, pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_val, pred))),
    }
    model_file = Path(model_file)
    model_file.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, model_file)
    (model_file.parent / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")
    print(json.dumps(metrics, indent=2))
    print(f"Saved model to {model_file}")
    return metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", type=Path, default=ROOT / "data/raw/yellow_tripdata_2023-01.parquet")
    parser.add_argument("--validation", type=Path, default=ROOT / "data/raw/yellow_tripdata_2023-02.parquet")
    parser.add_argument("--model", type=Path, default=ROOT / "models/taxi_model.joblib")
    args = parser.parse_args()
    train(args.train, args.validation, args.model)
