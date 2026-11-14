"""Prefect training flow; run with python -m pipelines.training_flow."""
import pipelines.prefect_compat

from pathlib import Path
import json
from prefect import flow, task
from src.train_compare import compare, ROOT

@task(retries=2, retry_delay_seconds=10)
def train_and_compare():
    return compare(ROOT / 'data/raw/yellow_tripdata_2023-01.parquet',
                   ROOT / 'data/raw/yellow_tripdata_2023-02.parquet')

@task
def verify_artifact(report):
    path = ROOT / 'models/taxi_model.joblib'
    if not path.is_file() or not report.get('winner'):
        raise RuntimeError('Missing model or winner')
    return {'winner': report['winner'], 'artifact': str(path)}

@flow(name='nyc-taxi-training')
def training_flow():
    return verify_artifact(train_and_compare())

if __name__ == '__main__':
    print(training_flow())
