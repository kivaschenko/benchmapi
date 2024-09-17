# test_e2e.py
import pytest


def test_endpoints():
    from app.main import app
    from fastapi.testclient import TestClient

    client = TestClient(app)

    response = client.get("/results/average/2024-06-01T00:00:00/2024-06-02T00:00:00")
    assert response.status_code == 200
    assert response.json() == {
        "average_token_count": 9.667,
        "average_time_to_first_token": 216.667,
        "average_time_per_output_token": 25.0,
        "average_total_generation_time": 436.667,
    }
