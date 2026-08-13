# Architecture

The first phase uses a deterministic in-memory digital-twin snapshot:

1. `topology.py` creates synthetic core, aggregation, and access nodes.
2. `simulation.py` generates one-second node telemetry and injects one declared
   access-node congestion episode.
3. The alarm engine evaluates latency and packet-loss thresholds.
4. `protocols.py` replays the same telemetry through fixed polling and adaptive
   delta/heartbeat strategies.
5. `api.py` exposes a read-only FastAPI interface over the generated snapshot.
6. `experiment.py` writes portable CSV files and a deterministic PNG.

The API and experiment paths call the same topology, simulation, alarm, and
protocol functions. There is no duplicate hidden implementation for the demo.

## API routes

- `GET /health`
- `GET /topology`
- `GET /telemetry/latest?node_id=access-07`
- `GET /alarms?limit=100`
- `GET /experiments/protocols`
- `GET /experiments/root-cause`

FastAPI supplies an OpenAPI document and interactive documentation at `/docs`.
The API runs on loopback by default and does not include authentication because
it exposes only deterministic synthetic data.
