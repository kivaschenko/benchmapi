import os
import json
from datetime import datetime
from typing import List
from fastapi import FastAPI, HTTPException
from .schema import Result

app = FastAPI()

SUPERBENCHMARK_DEBUG = os.getenv("SUPERBENCHMARK_DEBUG", "False").lower() == "true"


def load_test_data() -> List[Result]:
    with open("test_database.json", "r") as file:
        data = json.load(file)
    return [Result(**result) for result in data["benchmarking_results"]]


@app.get("/results/average", tags=["results"])
def get_average_results():
    """Get the average results of all the benchmarking runs."""
    if not SUPERBENCHMARK_DEBUG:
        raise HTTPException(status_code=503, detail="Feature not ready for live yet")

    results = load_test_data()
    if not results:
        return {}

    avg_token_count = sum(result.token_count for result in results) / len(results)
    avg_time_to_first_token = sum(
        result.time_to_first_token for result in results
    ) / len(results)
    avg_time_per_output_token = sum(
        result.time_per_output_token for result in results
    ) / len(results)
    avg_total_generation_time = sum(
        result.total_generation_time for result in results
    ) / len(results)

    return {
        "average_token_count": avg_token_count,
        "average_time_to_first_token": avg_time_to_first_token,
        "average_time_per_output_token": avg_time_per_output_token,
        "average_total_generation_time": avg_total_generation_time,
    }


@app.get("/results/average/{start_time}/{end_time}", tags=["results"])
def get_average_results_in_time_window(start_time: str, end_time: str):
    if not SUPERBENCHMARK_DEBUG:
        raise HTTPException(status_code=503, detail="Feature not ready for live yet")

    results = load_test_data()
    if not results:
        return {}

    start_dt = datetime.fromisoformat(start_time)
    end_dt = datetime.fromisoformat(end_time)

    filtered_results = [
        result
        for result in results
        if start_dt <= datetime.fromisoformat(result.timestamp) <= end_dt
    ]

    if not filtered_results:
        return {}

    avg_token_count = sum(result.token_count for result in filtered_results) / len(
        filtered_results
    )
    avg_time_to_first_token = sum(
        result.time_to_first_token for result in filtered_results
    ) / len(filtered_results)
    avg_time_per_output_token = sum(
        result.time_per_output_token for result in filtered_results
    ) / len(filtered_results)
    avg_total_generation_time = sum(
        result.total_generation_time for result in filtered_results
    ) / len(filtered_results)

    return {
        "average_token_count": avg_token_count,
        "average_time_to_first_token": avg_time_to_first_token,
        "average_time_per_output_token": avg_time_per_output_token,
        "average_total_generation_time": avg_total_generation_time,
    }
