# test_services.py
import pytest
from typing import List
from datetime import datetime

from app.services import average_performance, average_performance_in_period
from app.schema import Result
from app.repository import FakeRepository


@pytest.fixture
def results() -> List[Result]:
    """Return a list of results."""
    return [
        Result(
            request_id="1",
            prompt_text="Hello, world!",
            generated_text="Hello, world few times...",
            token_count=10,
            time_to_first_token=200,
            time_per_output_token=20,
            total_generation_time=2000,
            timestamp=datetime.fromisoformat("2024-09-13T13:00:00"),
        ),
        Result(
            request_id="2",
            prompt_text="Hello, world!",
            generated_text="Hello, world few times...",
            token_count=20,
            time_to_first_token=100,
            time_per_output_token=10,
            total_generation_time=1000,
            timestamp=datetime.fromisoformat("2024-09-14T13:30:00"),
        ),
        Result(
            request_id="3",
            prompt_text="Hello, world!",
            generated_text="Hello, world few times...",
            token_count=30,
            time_to_first_token=300,
            time_per_output_token=30,
            total_generation_time=200,
            timestamp=datetime.fromisoformat("2024-09-15T13:30:00"),
        ),
        Result(
            request_id="3",
            prompt_text="Hello, world!",
            generated_text="Hello, world few times...",
            token_count=30,
            time_to_first_token=300,
            time_per_output_token=30,
            total_generation_time=200,
            timestamp=datetime.fromisoformat("2024-09-16T13:30:00"),
        ),
    ]


def test_get_average_performance_success():
    """Test average_performance function."""
    data = [
        Result(
            request_id="1",
            prompt_text="Hello, world!",
            generated_text="Hello, world few times...",
            token_count=10,
            time_to_first_token=200,
            time_per_output_token=20,
            total_generation_time=2000,
            timestamp=datetime.fromisoformat("2024-09-13T13:00:00"),
        ),
        Result(
            request_id="2",
            prompt_text="Hello, world!",
            generated_text="Hello, world few times...",
            token_count=20,
            time_to_first_token=100,
            time_per_output_token=10,
            total_generation_time=1000,
            timestamp=datetime.fromisoformat("2024-09-14T13:30:00"),
        ),
    ]
    average_response = average_performance(results=data)
    assert average_response == {
        "average_token_count": 15.0,
        "average_time_to_first_token": 150.0,
        "average_time_per_output_token": 15.0,
        "average_total_generation_time": 1500.0,
    }


def test_get_average_perforformane_invalid_data():
    """Test average_performance function with invalid data."""
    data = []
    average_response = average_performance(results=data)
    assert average_response == {
        "average_token_count": 0.0,
        "average_time_to_first_token": 0.0,
        "average_time_per_output_token": 0.0,
        "average_total_generation_time": 0.0,
    }


def test_get_average_performance_in_time_window(results):
    """Test average_performance function with time window."""
    repository = FakeRepository(results=results)
    start_time = datetime.fromisoformat("2024-09-13T00:00:00")
    end_time = datetime.fromisoformat("2024-09-14T23:59:59")
    average_response = average_performance_in_period(repository, start_time, end_time)
    assert average_response == {
        "average_token_count": 15.0,
        "average_time_to_first_token": 150.0,
        "average_time_per_output_token": 15.0,
        "average_total_generation_time": 1500.0,
    }
