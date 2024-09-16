# This file contains the Pydantic schema for the FastAPI application.
from pydantic import BaseModel


class Result(BaseModel):
    """Data model for the output of the GPT-3 API."""
    request_id: str
    prompt_text: str
    generated_text: str
    token_count: int
    time_to_first_token: int  # in milliseconds
    time_per_output_token: int  # in milliseconds
    total_generation_time: int  # in milliseconds
    timestamp: str
