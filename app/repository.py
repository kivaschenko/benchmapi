from typing import Protocol, List
from datetime import datetime

from sqlalchemy.orm import Session

from .schema import Result
from .model_db import ResultModel
from .database import load_test_data


class Repository(Protocol):
    """Interface for the repository."""
    def get_results(self) -> List[Result]:
        """Return all the benchmarking results."""
        ...

    def get_results_in_time_window(
        self, start_time: datetime, end_time: datetime
    ) -> List[Result]:
        """Return all the benchmarking results within the time window."""
        ...


class FakeRepository(Repository):
    """Fake repository for testing purposes."""
    def __init__(self, results: List[Result] = load_test_data()):
        self.results = results
        print(f"Loaded results to fake repository: {results[:1]}...")

    def get_results(self) -> List[Result]:
        return self.results

    def get_results_in_time_window(
        self, start_time: datetime, end_time: datetime
    ) -> List[Result]:
        return [
            result
            for result in self.results
            if start_time <= result.timestamp <= end_time
        ]   
    

class DatabaseRepository(Repository):
    """Repository for the real database."""

    def __init__(self, db: Session):
        self.db = db

    def get_results(self) -> List[Result]:
        """Return all the benchmarking results."""
        results = self.db.query(ResultModel).with_entities(
            ResultModel.timestamp,
            ResultModel.request_id,
            ResultModel.prompt_text,
            ResultModel.generated_text,
            ResultModel.token_count,
            ResultModel.time_to_first_token,
            ResultModel.time_per_output_token,
            ResultModel.total_generation_time
        ).all()
        print(f"results from db: {results}")
        return [
            Result(
                timestamp=result.timestamp,
                request_id=result.request_id,
                prompt_text=result.prompt_text,
                generated_text=result.generated_text,
                token_count=result.token_count,
                time_to_first_token=result.time_to_first_token,
                time_per_output_token=result.time_per_output_token,
                total_generation_time=result.total_generation_time
            )
            for result in results
        ]

    def get_results_in_time_window(
        self, start_time: datetime, end_time: datetime
    ) -> List[Result]:
        """Return all the benchmarking results within the time window."""
        results = self.db.query(ResultModel).with_entities(
            ResultModel.timestamp,
            ResultModel.request_id,
            ResultModel.prompt_text,
            ResultModel.generated_text,
            ResultModel.token_count,
            ResultModel.time_to_first_token,
            ResultModel.time_per_output_token,
            ResultModel.total_generation_time
        ).filter(
            ResultModel.timestamp >= start_time,
            ResultModel.timestamp <= end_time
        ).all()
        print(f"results from db within time window: {results}")
        return [
            Result(
                timestamp=result.timestamp,
                request_id=result.request_id,
                prompt_text=result.prompt_text,
                generated_text=result.generated_text,
                token_count=result.token_count,
                time_to_first_token=result.time_to_first_token,
                time_per_output_token=result.time_per_output_token,
                total_generation_time=result.total_generation_time
            )
            for result in results
        ]