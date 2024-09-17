from typing import List
from datetime import datetime

from .repository import Repository
from .schema import Result


def get_results(repository: Repository) -> List[Result]:
    """Return all the benchmarking results."""
    return repository.get_results()


def get_results_in_time_window(
    repository: Repository, start_time: datetime, end_time: datetime
) -> List[Result]:
    """Return all the benchmarking results within the time window."""
    return repository.get_results_in_time_window(start_time, end_time)


def average_performance(results: List[Result]) -> dict[str, float]:
    """Calculate the average performance metrics from the benchmarking results."""
    if not results:
        return {
            "average_token_count": 0,
            "average_time_to_first_token": 0,
            "average_time_per_output_token": 0,
            "average_total_generation_time": 0,
        }
    avg_token_count = round(sum(result.token_count for result in results) / len(results), 3)
    avg_time_to_first_token = round(sum(
        result.time_to_first_token for result in results
    ) / len(results), 3)
    avg_time_per_output_token = round(sum(
        result.time_per_output_token for result in results
    ) / len(results), 3)
    avg_total_generation_time = round(sum(
        result.total_generation_time for result in results
    ) / len(results), 3)

    return {
        "average_token_count": avg_token_count,
        "average_time_to_first_token": avg_time_to_first_token,
        "average_time_per_output_token": avg_time_per_output_token,
        "average_total_generation_time": avg_total_generation_time,
    }


def average_performance_in_period(
    repository: Repository, start_time: datetime, end_time: datetime
) -> dict[str, float]:
    """Calculate the average performance metrics from the benchmarking
    results within the time window."""
    filtered_results = get_results_in_time_window(repository, start_time, end_time)
    return average_performance(filtered_results)
