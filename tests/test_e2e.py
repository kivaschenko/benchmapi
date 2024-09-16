# test_e2e.py
import pytest


def test_endpoints():
    from app.main import app
    from fastapi.testclient import TestClient

    client = TestClient(app)

    response = client.get("/results/average/2021-01-01T00:00:00/2021-01-02T00:00:00")
    assert response.status_code == 200
    assert response.json() == {
        "average_token_count": 10,
        "average_time_to_first_token": 0.1,
        "average_time_per_output_token": 0.01,
        "average_total_generation_time": 1,
    }

    response = client.get("/results/average/2021-01-01T00:00:00/2021-01-01T00:00:00")
    assert response.status_code == 200
    assert response.json() == {}

    response = client.get("/results/average/2021-01-01T00:00:00/2021-01-03T00:00:00")
    assert response.status_code == 200
    assert response.json() == {
        "average_token_count": 10,
        "average_time_to_first_token": 0.1,
        "average_time_per_output_token": 0.01,
        "average_total_generation_time": 1,
    }

    response = client.get("/results/average/2021-01-01T00:00:00/2021-01-04T00:00:00")
    assert response.status_code == 200
    assert response.json() == {
        "average_token_count": 10,
        "average_time_to_first_token": 0.1,
        "average_time_per_output_token": 0.01,
        "average_total_generation_time": 1,
    }

    response = client.get("/results/average/2021-01-01T00:00:00/2021-01-05T00:00:00")
    assert response.status_code == 200
    assert response.json() == {
        "average_token_count": 10,
        "average_time_to_first_token": 0.1,
        "average_time_per_output_token": 0.01,
        "average_total_generation_time": 1,
    }

    response = client.get("/results/average/2021-01-01T00:00:00/2021-01-06T00:00:00")
