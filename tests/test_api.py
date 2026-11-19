
import pytest
from fastapi.testclient import TestClient

import api
import app as workforce

client = TestClient(api.app)


@pytest.fixture(autouse=True)
def isolate_test_data(tmp_path, monkeypatch):
    """Use a temporary JSON file for every test."""
    monkeypatch.setattr(
        workforce,
        "DATA_FILE",
        tmp_path / "leave_requests.json"
    )


def test_get_employees():
    response = client.get("/employees")

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_create_leave_request():
    response = client.post(
        "/leave-requests",
        json={
            "employee_id": "E001",
            "leave_days": 2,
            "reason": "Testing API"
        }
    )

    assert response.status_code == 201
    assert response.json()["status"] == "Pending"
    assert response.json()["employee"] == "John Smith"


def test_unknown_employee_is_rejected():
    response = client.post(
        "/leave-requests",
        json={
            "employee_id": "E999",
            "leave_days": 2,
            "reason": "Testing API"
        }
    )

    assert response.status_code == 404


def test_approve_request_and_prevent_second_decision():
    created = client.post(
        "/leave-requests",
        json={
            "employee_id": "E002",
            "leave_days": 1,
            "reason": "Testing approval"
        }
    )

    request_id = created.json()["request_id"]

    decision = client.patch(
        f"/leave-requests/{request_id}",
        json={
            "decision": "approve",
            "note": "Approved in automated test"
        }
    )

    assert decision.status_code == 200
    assert decision.json()["status"] == "Approved"

    second_decision = client.patch(
        f"/leave-requests/{request_id}",
        json={
            "decision": "reject",
            "note": "Second attempt"
        }
    )

    assert second_decision.status_code == 400
