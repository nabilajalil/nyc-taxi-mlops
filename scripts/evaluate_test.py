"""Final holdout evaluation; do not tune models on these results."""
from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from src.features import prepare_data
ROOT = Path(__file__).resolve().parents[1]
model = joblib.load(ROOT / 'models/taxi_model.joblib')
x, y = prepare_data(pd.read_parquet(ROOT / 'data/raw/yellow_tripdata_2023-03.parquet'))
pred = model.predict(x)
metrics = {'test_rows': len(y), 'test_mae': float(mean_absolute_error(y, pred)),
           'test_rmse': float(np.sqrt(mean_squared_error(y, pred)))}
(ROOT / 'models/test_metrics.json').write_text(json.dumps(metrics, indent=2))
print(metrics)
