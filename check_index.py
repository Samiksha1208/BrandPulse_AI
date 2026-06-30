from app.retrieval.es_client import es, INDEX_NAME

result = es.count(index=INDEX_NAME)
print(f"Total documents in index: {result['count']}")

sample = es.search(index=INDEX_NAME, body={"query": {"match_all": {}}, "size": 1})
print(sample["hits"]["hits"][0]["_source"])
