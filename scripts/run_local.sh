#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
exec gunicorn --bind 0.0.0.0:8000 --workers 2 app.app:app
