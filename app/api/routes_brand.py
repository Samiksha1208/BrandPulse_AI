from fastapi import APIRouter, HTTPException
from app.models.schemas import SentimentResponse, SentimentPoint, CrisisResponse
from app.agents.crisis_detection import detect_volume_spike
from app.retrieval.es_client import es, INDEX_NAME
from datetime import datetime, timedelta, timezone

router = APIRouter()

@router.get("/{brand}/sentiment", response_model=SentimentResponse)
async def get_sentiment(brand: str, days: int = 7):
    try:
        series = []
        total = 0
        for i in range(days):
            day = datetime.now(timezone.utc) - timedelta(days=i)
            day_start = day.replace(hour=0, minute=0, second=0).isoformat()
            day_end = day.replace(hour=23, minute=59, second=59).isoformat()

            result = es.count(index=INDEX_NAME, body={
                "query": {"bool": {"filter": [
                    {"term": {"brand": brand}},
                    {"range": {"published_at": {"gte": day_start, "lte": day_end}}}
                ]}}
            })
            count = result["count"]
            total += count
            series.append(SentimentPoint(
                date=day.strftime("%Y-%m-%d"),
                mention_count=count
            ))

        return SentimentResponse(
            brand=brand,
            total_mentions=total,
            series=list(reversed(series))
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{brand}/crisis-check", response_model=CrisisResponse)
async def crisis_check(brand: str):
    try:
        result = detect_volume_spike(brand)
        return CrisisResponse(
            brand=brand,
            spike_detected=result["is_anomaly"],
            spike_ratio=result["spike_ratio"],
            recent_6h=result["recent_6h"],
            baseline_per_6h=result["baseline_per_6h"],
            message="Crisis-level anomaly detected. Human review recommended." 
                    if result["is_anomaly"] else "No anomaly detected."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
