from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ResultModel(Base):
    """ORM model for the benchmarking results."""
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, unique=True, index=True)
    prompt_text = Column(String)
    generated_text = Column(String)
    token_count = Column(Integer)
    time_to_first_token = Column(Integer)  # in milliseconds
    time_per_output_token = Column(Integer)  # in milliseconds
    total_generation_time = Column(Integer)  # in milliseconds
    timestamp = Column(DateTime)
