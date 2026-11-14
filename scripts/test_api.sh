#!/usr/bin/env bash
set -euo pipefail
curl -fsS http://localhost:8000/health
printf '\n'
curl -fsS -X POST http://localhost:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{"PULocationID":161,"DOLocationID":132,"pickup_hour":8,"day_of_week":0}'
printf '\n'
