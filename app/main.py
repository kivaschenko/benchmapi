import os
from datetime import datetime

from fastapi import FastAPI, Depends

from .schema import AverageResults
from .repository import Repository, FakeRepository
from .services import get_results, get_results_in_time_window, average_performance

app = FastAPI()

SUPERBENCHMARK_DEBUG = os.getenv("SUPERBENCHMARK_DEBUG", "False").lower() == "true"


def get_repository() -> Repository:
    """Return the repository based on the environment variable."""
    if SUPERBENCHMARK_DEBUG:
        return FakeRepository()
    return FakeRepository()


@app.get("/results/average", response_model=AverageResults, tags=["results"])
def get_average_results(
    repository: Repository = Depends(get_repository),
) -> dict[str, float]:
    """Get the average results of all the benchmarking runs."""
    results = get_results(repository)
    return average_performance(results)


@app.get("/results/average/{start_time}/{end_time}", tags=["results"], response_model=AverageResults)
def get_average_results_in_time_window(
    start_time: str,
    end_time: str,
    repository: Repository = Depends(get_repository),
) -> dict[str, float]:
    """Get the average results of all the benchmarking runs within the time window."""

    start_dt = datetime.fromisoformat(start_time)
    end_dt = datetime.fromisoformat(end_time)

    filtered_results = get_results_in_time_window(repository, start_dt, end_dt)
    return average_performance(filtered_results)
