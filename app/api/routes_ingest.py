from fastapi import APIRouter, HTTPException
from app.models.schemas import IngestRequest, IngestResponse
from app.ingestion.newsapi_source import fetch_news
from app.ingestion.rss_source import fetch_rss
from app.retrieval.indexer import index_items
from app.utils.dedup import is_seen, mark_seen

router = APIRouter()

@router.post("", response_model=IngestResponse)
async def ingest(req: IngestRequest):
    try:
        raw_items = fetch_news(req.brand) + fetch_rss(req.brand)
        new_items = [item for item in raw_items if not is_seen(item["url"])]

        chunks_indexed = 0
        if new_items:
            chunks_indexed = index_items(new_items, req.brand)
            for item in new_items:
                mark_seen(item["url"])

        return IngestResponse(
            brand=req.brand,
            new_items=len(new_items),
            chunks_indexed=chunks_indexed
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
