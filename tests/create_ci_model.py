from pathlib import Path

import joblib
import pandas as pd
from sklearn.dummy import DummyRegressor

model = DummyRegressor(strategy="constant", constant=12.5)

X = pd.DataFrame({
    "PULocationID": ["161", "132"],
    "DOLocationID": ["132", "161"],
    "pickup_hour": [8, 9],
    "day_of_week": [0, 1],
})

y = [12.5, 12.5]

model.fit(X, y)

output = Path("tests/ci_model.joblib")
joblib.dump(model, output)

print(f"Created {output}")
