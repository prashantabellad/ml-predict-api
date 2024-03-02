import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from typing import List
from fastapi import APIRouter
from pydantic import BaseModel
from transformers import pipeline

from app import __version__, schemas
from app.config import settings

# api_router = FastAPI()
api_router = APIRouter()

# Load the sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

class Text(BaseModel):
    text: str
    
@api_router.get("/health", response_model=schemas.Health, status_code=200)
def health() -> dict:
    """
    Root Get
    """
    health = schemas.Health(
        name=settings.PROJECT_NAME, api_version=__version__, model_version=__version__
    )

    return health.dict()

@api_router.post("/predict/", response_model=schemas.PredictionResponse)
async def predict(text: Text) -> schemas.PredictionResponse:
    results = sentiment_pipeline(text.text)
    processed_results = [schemas.SentimentResult(label=result['label'], score=result['score']) for result in results]
    return schemas.PredictionResponse(results=processed_results)
