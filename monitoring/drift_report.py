"""Generate Evidently drift report comparing historical pickup features to recent data.
Usage: python -m monitoring.drift_report --reference data/raw/yellow_tripdata_2023-01.parquet --current data/raw/yellow_tripdata_2023-02.parquet
"""
import argparse
from pathlib import Path
import pandas as pd
from evidently import Report, Dataset, DataDefinition
from evidently.presets import DataDriftPreset
from src.features import prepare_data

def report_drift(reference, current, output, max_rows=10000):
    x_ref, _ = prepare_data(pd.read_parquet(reference))
    x_cur, _ = prepare_data(pd.read_parquet(current))
    x_ref = x_ref.sample(n=min(len(x_ref), max_rows), random_state=42)
    x_cur = x_cur.sample(n=min(len(x_cur), max_rows), random_state=42)
    definition = DataDefinition(
        categorical_columns=['PULocationID', 'DOLocationID'],
        numerical_columns=['pickup_hour', 'day_of_week'],
    )
    ref = Dataset.from_pandas(x_ref, data_definition=definition)
    cur = Dataset.from_pandas(x_cur, data_definition=definition)
    result = Report([DataDriftPreset()]).run(cur, ref)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    result.save_html(str(output))
    print(f'Drift report: {output}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--reference', default='data/raw/yellow_tripdata_2023-01.parquet')
    parser.add_argument('--current', default='data/raw/yellow_tripdata_2023-02.parquet')
    parser.add_argument('--output', default='reports/drift.html')
    args = parser.parse_args()
    report_drift(args.reference, args.current, args.output)
