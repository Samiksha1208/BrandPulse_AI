from app.retrieval.es_client import es, INDEX_NAME
from app.retrieval.chunking import chunk_article

def index_items(items: list[dict], brand: str):
    indexed_count = 0
    for item in items:
        docs = chunk_article(item["text"], {
            "brand": brand,
            "source": item["source"],
            "url": item["url"],
            "published_at": item["published_at"]
        })
        for doc in docs:
            es.index(index=INDEX_NAME, document=doc)
            indexed_count += 1
    return indexed_count
