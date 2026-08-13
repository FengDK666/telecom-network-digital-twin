#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."
. .venv/bin/activate

uvicorn telecom_twin.api:app --host 127.0.0.1 --port 8765 > /tmp/telecom-twin-api.log 2>&1 &
server_pid=$!
trap 'kill "$server_pid" 2>/dev/null || true; wait "$server_pid" 2>/dev/null || true' EXIT

for _ in {1..20}; do
    if curl --fail --silent http://127.0.0.1:8765/health > /tmp/telecom-twin-health.json; then
        break
    fi
    sleep 0.25
done

curl --fail --silent http://127.0.0.1:8765/health
printf '\n'
curl --fail --silent 'http://127.0.0.1:8765/telemetry/latest?node_id=access-07'
printf '\n'
curl --fail --silent http://127.0.0.1:8765/openapi.json \
    | python3 -c 'import json, sys; print(sorted(json.load(sys.stdin)["paths"]))'
