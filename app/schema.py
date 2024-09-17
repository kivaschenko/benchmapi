# This file contains the Pydantic schema for the FastAPI application.
from pydantic import BaseModel
from datetime import datetime


class Result(BaseModel):
    """Data model for the output of the GPT-3 API."""
    request_id: str
    prompt_text: str
    generated_text: str
    token_count: int
    time_to_first_token: int  # in milliseconds
    time_per_output_token: int  # in milliseconds
    total_generation_time: int  # in milliseconds
    timestamp:datetime 

    class Config:
        from_attributes = True


class AverageResults(BaseModel):
    """Data model for the average performance metrics."""

    average_token_count: float
    average_time_to_first_token: float
    average_time_per_output_token: float
    average_total_generation_time: float
