import pandas as pd
import pytest
from src.features import make_features, prepare_data


def test_make_features():
    row = make_features(161, 132, 8, 0).iloc[0]
    assert row["PULocationID"] == "161"
    assert row["pickup_hour"] == 8


@pytest.mark.parametrize("args", [(0, 132, 8, 0), (161, 132, 24, 0), (161, 132, 8, 7)])
def test_bad_features(args):
    with pytest.raises(ValueError):
        make_features(*args)


def test_duration_filtering():
    df = pd.DataFrame({"PULocationID": [161, 161], "DOLocationID": [132, 132], "tpep_pickup_datetime": pd.to_datetime(["2023-01-01 08:00", "2023-01-01 08:00"]), "tpep_dropoff_datetime": pd.to_datetime(["2023-01-01 08:15", "2023-01-01 11:00"])})
    x, y = prepare_data(df)
    assert len(x) == 1
    assert y.iloc[0] == 15
