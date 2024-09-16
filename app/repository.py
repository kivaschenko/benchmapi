from typing import Protocol, List
from datetime import datetime

from .schema import Result
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

    def get_results(self) -> List[Result]:
        pass

    def get_results_in_time_window(
        self, start_time: datetime, end_time: datetime
    ) -> List[Result]:
        pass
