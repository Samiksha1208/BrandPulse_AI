from pydantic import BaseModel, Field
from typing import Optional

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=500)
    brand: str = Field(..., min_length=1)
    competitors: list[str] = []
    session_id: str = Field(..., min_length=1)

class QueryResponse(BaseModel):
    answer: str
    session_id: str
    brand: str

class IngestRequest(BaseModel):
    brand: str

class IngestResponse(BaseModel):
    brand: str
    new_items: int
    chunks_indexed: int

class SentimentPoint(BaseModel):
    date: str
    mention_count: int

class SentimentResponse(BaseModel):
    brand: str
    total_mentions: int
    series: list[SentimentPoint]

class CrisisResponse(BaseModel):
    brand: str
    spike_detected: bool
    spike_ratio: float
    recent_6h: int
    baseline_per_6h: float
    message: str
