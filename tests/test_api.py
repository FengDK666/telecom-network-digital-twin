from fastapi.testclient import TestClient

from telecom_twin.api import app


def test_api_exposes_synthetic_snapshot() -> None:
    client = TestClient(app)
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json() == {"status": "ok", "data_mode": "synthetic", "node_count": 27}
    topology = client.get("/topology").json()
    assert len(topology["nodes"]) == 27
    assert len(topology["links"]) == 27
    assert len(client.get("/telemetry/latest").json()) == 27
    assert len(client.get("/experiments/protocols").json()) == 2


def test_latest_telemetry_unknown_node_returns_empty_list() -> None:
    client = TestClient(app)
    assert client.get("/telemetry/latest", params={"node_id": "not-real"}).json() == []
