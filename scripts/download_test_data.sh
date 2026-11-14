#!/usr/bin/env bash
set -euo pipefail
mkdir -p data/raw
curl -fL --retry 3 -o data/raw/yellow_tripdata_2023-03.parquet \
  https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet
