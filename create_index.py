# create_index.py
from app.retrieval.es_client import es, INDEX_NAME

mapping = {
    "mappings": {
        "properties": {
            "content": {"type": "semantic_text"},
            "brand":        {"type": "keyword"},
            "source":       {"type": "keyword"},
            "url":          {"type": "keyword"},
            "published_at": {"type": "date", "ignore_malformed": True},
        }
    }
}

if es.indices.exists(index=INDEX_NAME):
    es.indices.delete(index=INDEX_NAME)

es.indices.create(index=INDEX_NAME, body=mapping)
print(f"Created index: {INDEX_NAME} with semantic_text field")
