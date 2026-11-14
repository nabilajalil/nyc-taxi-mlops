#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mlflow ui --backend-store-uri "$(pwd)/mlruns" --host 127.0.0.1 --port 5000
