from fastapi.testclient import TestClient

from activity_api.main import app


client = TestClient(app)


def test_create_list_and_get_activity_record():
    payload = {
        "record_id": "activity_evt_1",
        "tenant_id": "tenant_1",
        "trace_id": "trace_1",
        "event_count": 1,
        "event_types": ["model_invocation"],
        "events": [
            {
                "event_id": "evt_1",
                "event_type": "model_invocation",
                "tenant_id": "tenant_1",
                "payload": {"model_name": "gpt-4.1"},
            }
        ],
        "summary": {"model_invocation": 1},
    }

    created = client.post("/v1/activity-records/", json=payload)
    assert created.status_code == 201
    assert created.json()["record_id"] == "activity_evt_1"

    listed = client.get("/v1/activity-records/", params={"tenant_id": "tenant_1"})
    assert listed.status_code == 200
    assert any(record["record_id"] == "activity_evt_1" for record in listed.json())

    fetched = client.get("/v1/activity-records/activity_evt_1")
    assert fetched.status_code == 200
    assert fetched.json()["trace_id"] == "trace_1"


def test_get_activity_record_returns_404_for_missing_record():
    response = client.get("/v1/activity-records/missing")

    assert response.status_code == 404
