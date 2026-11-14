"""Train three candidate models, log MLflow runs, and export the best pipeline."""
import argparse
import json
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

from src.features import prepare_data

ROOT = Path(__file__).resolve().parents[1]
CATS = ["PULocationID", "DOLocationID"]
NUMS = ["pickup_hour", "day_of_week"]


def candidates():
    onehot = ColumnTransformer([
        ("zones", OneHotEncoder(handle_unknown="ignore"), CATS),
        ("time", "passthrough", NUMS),
    ])
    return {
        "ridge": Pipeline([
            ("preprocess", onehot),
            ("model", Ridge(alpha=1.0)),
        ]),
        "random_forest": Pipeline([
            ("preprocess", ColumnTransformer([
                ("zones", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), CATS),
                ("time", "passthrough", NUMS),
            ])),
            ("model", RandomForestRegressor(
                n_estimators=80, max_depth=16, min_samples_leaf=5,
                n_jobs=-1, random_state=42,
            )),
        ]),
        "hist_gradient_boosting": Pipeline([
            ("preprocess", ColumnTransformer([
                ("zones", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), CATS),
                ("time", "passthrough", NUMS),
            ])),
            ("model", HistGradientBoostingRegressor(
                max_iter=150, max_leaf_nodes=31,
                learning_rate=0.08, random_state=42,
            )),
        ]),
    }


def compare(train_file, val_file, max_train_rows=150000, max_val_rows=100000,
            tracking_uri=None, output_dir=None):
    output_dir = Path(output_dir) if output_dir is not None else ROOT / "models"
    output_dir.mkdir(parents=True, exist_ok=True)

    # SQLite is the default; a custom MLflow URI can still be supplied via CLI.
    tracking_uri = tracking_uri or f"sqlite:///{ROOT / 'mlflow.db'}"
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment("nyc-taxi-trip-duration")

    x_train, y_train = prepare_data(pd.read_parquet(train_file))
    x_val, y_val = prepare_data(pd.read_parquet(val_file))
    if x_train.empty or x_val.empty:
        raise ValueError("No valid trips after filtering")

    if max_train_rows and len(x_train) > max_train_rows:
        chosen = x_train.sample(n=max_train_rows, random_state=42).index
        x_train, y_train = x_train.loc[chosen], y_train.loc[chosen]
    if max_val_rows and len(x_val) > max_val_rows:
        chosen = x_val.sample(n=max_val_rows, random_state=42).index
        x_val, y_val = x_val.loc[chosen], y_val.loc[chosen]

    results = []
    best_name, best_model, best_rmse = None, None, float("inf")
    for name, pipeline in candidates().items():
        print(f"Training {name} ...", flush=True)
        with mlflow.start_run(run_name=name) as run:
            mlflow.set_tag("model_type", name)
            mlflow.log_params({
                "train_month": "2023-01",
                "validation_month": "2023-02",
                "max_train_rows": max_train_rows,
                "max_val_rows": max_val_rows,
                "random_state": 42,
            })
            mlflow.log_params({
                f"model_{k}": v
                for k, v in pipeline.named_steps["model"].get_params().items()
                if k in {"alpha", "n_estimators", "max_depth", "min_samples_leaf",
                         "max_iter", "max_leaf_nodes", "learning_rate"}
            })
            pipeline.fit(x_train, y_train)
            pred = pipeline.predict(x_val)
            mae = float(mean_absolute_error(y_val, pred))
            rmse = float(np.sqrt(mean_squared_error(y_val, pred)))
            mlflow.log_metrics({
                "val_mae": mae,
                "val_rmse": rmse,
                "train_rows": len(x_train),
                "validation_rows": len(x_val),
            })
            mlflow.sklearn.log_model(
                sk_model=pipeline,
                name="model",
                skops_trusted_types=[
                    "sklearn.tree._tree.Tree",
                    "sklearn.ensemble._hist_gradient_boosting.predictor.TreePredictor",
                ],
            )
            results.append({
                "model": name,
                "run_id": run.info.run_id,
                "val_mae": mae,
                "val_rmse": rmse,
            })
            if rmse < best_rmse:
                best_name, best_model, best_rmse = name, pipeline, rmse
            print(f"{name}: MAE={mae:.3f} RMSE={rmse:.3f}")

    results.sort(key=lambda r: r["val_rmse"])
    joblib.dump(best_model, output_dir / "taxi_model.joblib")
    report = {
        "selection_metric": "val_rmse",
        "winner": best_name,
        "tracking_uri": tracking_uri,
        "results": results,
        "note": "Selected on February validation data; evaluate on untouched later test month before real production.",
    }
    (output_dir / "comparison.json").write_text(json.dumps(report, indent=2) + "\n")
    print("\nWINNER:", best_name)
    print("Production artifact:", output_dir / "taxi_model.joblib")
    print("Comparison report:", output_dir / "comparison.json")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", type=Path, default=ROOT / "data/raw/yellow_tripdata_2023-01.parquet")
    parser.add_argument("--validation", type=Path, default=ROOT / "data/raw/yellow_tripdata_2023-02.parquet")
    parser.add_argument("--max-train-rows", type=int, default=150000)
    parser.add_argument("--max-val-rows", type=int, default=100000)
    parser.add_argument("--tracking-uri", default=None)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "models")
    args = parser.parse_args()
    compare(args.train, args.validation, args.max_train_rows, args.max_val_rows,
            args.tracking_uri, args.output_dir)
