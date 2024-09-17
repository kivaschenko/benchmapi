import json
import os
from datetime import datetime
from sqlalchemy.orm import Session

from app.database import engine, Base, FAKE_DB_PATH
from app.model_db import ResultModel
from app.repository import DatabaseRepository, FakeRepository

def load_test_data():
    """Load the test data from the JSON file."""
    with open(FAKE_DB_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data["benchmarking_results"]

def seed_database():
    """Seed the database with test data."""
    Base.metadata.create_all(bind=engine)
    session = Session(bind=engine)
    
    try:
        if os.getenv("SUPERBENCHMARK_DEBUG", "False").lower() == "true":
            results = load_test_data()
            repository = FakeRepository(results)
        else:
            # Load actual data from the database or another source
            results = load_test_data()  # Replace with actual data loading logic
            repository = DatabaseRepository(session)

        for result in results:
            result_model = ResultModel(
                request_id=result["request_id"],
                prompt_text=result["prompt_text"],
                generated_text=result["generated_text"],
                token_count=result["token_count"],
                time_to_first_token=result["time_to_first_token"],
                time_per_output_token=result["time_per_output_token"],
                total_generation_time=result["total_generation_time"],
                timestamp=datetime.fromisoformat(result["timestamp"])
            )
            session.add(result_model)
            print(f"Seeding database with: {result}")
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_database()
    print("Database seeded successfully.")