# Description: This file contains the database setup and the function to load the test data.
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .schema import Result

load_dotenv()

SUPERBENCHMARK_DEBUG = os.getenv("SUPERBENCHMARK_DEBUG", "False").lower() == "true"
DATABASE_URL = os.getenv("DATABASE_URL")
FAKE_DB_PATH = Path(__file__).parent / "test_database.json"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Get the database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_test_data():
    """Load the test data from the JSON file."""
    with open(FAKE_DB_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)
    return [Result(**result) for result in data["benchmarking_results"]]

if __name__ == "__main__":
    fake_db = load_test_data()
    print(fake_db if fake_db else "No data found")
