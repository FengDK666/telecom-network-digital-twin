"""FastAPI read API over a deterministic in-memory digital-twin snapshot."""

from __future__ import annotations

from fastapi import FastAPI, Query

from telecom_twin.protocols import compare_protocols
from telecom_twin.root_cause import evaluate_root_cause
from telecom_twin.simulation import generate_alarms, generate_telemetry
from telecom_twin.topology import generate_topology

nodes, links = generate_topology()
samples = generate_telemetry(nodes)
alarms = generate_alarms(samples)
protocol_results = compare_protocols(samples)
root_cause_results = evaluate_root_cause(nodes, links)

app = FastAPI(
    title="Synthetic Telecom Network Digital Twin",
    version="0.1.0",
    description="Reproducible synthetic data only; not connected to an operator network.",
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "data_mode": "synthetic", "node_count": len(nodes)}


@app.get("/topology")
def topology() -> dict:
    return {
        "nodes": [node.to_dict() for node in nodes],
        "links": [link.to_dict() for link in links],
    }


@app.get("/telemetry/latest")
def latest_telemetry(node_id: str | None = Query(default=None)) -> list[dict]:
    latest = {sample.node_id: sample for sample in samples}
    if node_id is not None:
        return [latest[node_id].to_dict()] if node_id in latest else []
    return [latest[key].to_dict() for key in sorted(latest)]


@app.get("/alarms")
def alarm_feed(limit: int = Query(default=100, ge=1, le=1000)) -> list[dict]:
    return [alarm.to_dict() for alarm in alarms[-limit:]]


@app.get("/experiments/protocols")
def protocol_experiment() -> list[dict]:
    return protocol_results


@app.get("/experiments/root-cause")
def root_cause_experiment() -> list[dict]:
    return root_cause_results
