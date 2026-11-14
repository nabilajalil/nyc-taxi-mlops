#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p data/raw
for month in 01 02; do
  filename="yellow_tripdata_2023-${month}.parquet"
  echo "Downloading $filename"
  curl --fail --location --retry 3 --output "data/raw/$filename.part" "https://d37ci6vzurychx.cloudfront.net/trip-data/$filename"
  mv "data/raw/$filename.part" "data/raw/$filename"
done
