import pandas as pd

FEATURES = ["PULocationID", "DOLocationID", "pickup_hour", "day_of_week"]
ZONE_COLUMNS = ["PULocationID", "DOLocationID"]


def prepare_data(df: pd.DataFrame):
    required = ZONE_COLUMNS + ["tpep_pickup_datetime", "tpep_dropoff_datetime"]
    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    data = df[required].copy()
    data["tpep_pickup_datetime"] = pd.to_datetime(data["tpep_pickup_datetime"])
    data["tpep_dropoff_datetime"] = pd.to_datetime(data["tpep_dropoff_datetime"])
    data["duration"] = (data["tpep_dropoff_datetime"] - data["tpep_pickup_datetime"]).dt.total_seconds() / 60
    data = data[data["duration"].between(1, 60)].dropna(subset=ZONE_COLUMNS).copy()
    for col in ZONE_COLUMNS:
        data = data[data[col].between(1, 265)]
        data[col] = data[col].astype(int).astype(str)
    data["pickup_hour"] = data["tpep_pickup_datetime"].dt.hour
    data["day_of_week"] = data["tpep_pickup_datetime"].dt.dayofweek
    return data[FEATURES], data["duration"]


def make_features(pickup, dropoff, hour, weekday):
    pickup, dropoff, hour, weekday = map(int, (pickup, dropoff, hour, weekday))
    if not (1 <= pickup <= 265 and 1 <= dropoff <= 265):
        raise ValueError("Taxi zone IDs must be between 1 and 265")
    if not (0 <= hour <= 23 and 0 <= weekday <= 6):
        raise ValueError("Hour must be 0–23 and weekday must be 0–6")
    return pd.DataFrame([{"PULocationID": str(pickup), "DOLocationID": str(dropoff), "pickup_hour": hour, "day_of_week": weekday}])[FEATURES]
