from app.retrieval.es_client import es, INDEX_NAME

def hybrid_search(query: str, brand: str, k: int = 8):
    body = {
        "retriever": {
            "rrf": {
                "retrievers": [
                    {"standard": {"query": {"bool": {
                        "must": [{"match": {"content": query}}],
                        "filter": [{"term": {"brand": brand}}]
                    }}}},
                    {"standard": {"query": {"bool": {
                        "must": [{"semantic": {"field": "content", "query": query}}],
                        "filter": [{"term": {"brand": brand}}]
                    }}}}
                ]
            }
        },
        "size": k
    }
    return es.search(index=INDEX_NAME, body=body)["hits"]["hits"]
