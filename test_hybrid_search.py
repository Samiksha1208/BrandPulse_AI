from app.retrieval.hybrid_search import hybrid_search

results = hybrid_search("battery range complaints", "Tesla")
for r in results:
    print(r["_score"], r["_source"]["content"][:100])
