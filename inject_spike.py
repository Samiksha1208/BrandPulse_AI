import asyncio
from datetime import datetime, timezone
from app.retrieval.es_client import es, INDEX_NAME
import uuid

def inject_spike(brand: str, num_docs: int = 15):
    print(f"Injecting {num_docs} fake articles for {brand} to simulate a crisis spike...")
    now = datetime.now(timezone.utc).isoformat()
    
    for i in range(num_docs):
        doc = {
            "id": str(uuid.uuid4()),
            "brand": brand,
            "title": f"BREAKING: Huge {brand} controversy erupts!",
            "content": f"Major news breaking right now regarding {brand}. Everyone is talking about it.",
            "url": "https://example.com/breaking-news",
            "published_at": now,
            "source": "Fake News Injector"
        }
        es.index(index=INDEX_NAME, document=doc)
        
    print(f"✅ Injected {num_docs} articles. Refresh your Streamlit dashboard now!")

if __name__ == "__main__":
    inject_spike("Tesla", 20)
