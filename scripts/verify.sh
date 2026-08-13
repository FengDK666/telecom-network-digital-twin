#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."
. .venv/bin/activate
ruff check .
pytest -q
telecom-twin experiment --output-dir /tmp/telecom-twin-verification
telecom-twin benchmark --output-dir /tmp/telecom-twin-benchmark --trials-per-root 2
