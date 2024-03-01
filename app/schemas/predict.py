from typing import List, Union
from pydantic import BaseModel


class SentimentResult(BaseModel):
    label: str
    score: float

class PredictionResponse(BaseModel):
    results: List[SentimentResult]
