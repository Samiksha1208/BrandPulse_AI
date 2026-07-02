from app.retrieval.es_client import es, INDEX_NAME
from datetime import datetime, timedelta, timezone

def count_mentions(brand: str, hours: int) -> int:
    since = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
    body = {
        "query": {
            "bool": {
                "filter": [
                    {"term": {"brand": brand}},
                    {"range": {"published_at": {"gte": since}}}
                ]
            }
        }
    }
    result = es.count(index=INDEX_NAME, body=body)
    return result["count"]
