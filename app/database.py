# If debug mode is enbled then use fake db from json file else use real db
import json
from pathlib import Path
from .schema import Result

FAKE_DB_PATH = Path(__file__).parent / "test_database.json"


def load_test_data():
    """Load the test data from the JSON file."""
    with open(FAKE_DB_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)
    return [Result(**result) for result in data["benchmarking_results"]]


if __name__ == "__main__":
    fake_db = load_test_data()
    print(fake_db if fake_db else "No data found")
