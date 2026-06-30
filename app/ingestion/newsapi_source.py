import os
from newsapi import NewsApiClient
from dotenv import load_dotenv

load_dotenv()
client = NewsApiClient(api_key=os.getenv("NEWSAPI_KEY"))

def fetch_news(brand: str, page_size: int = 20) -> list[dict]:
    response = client.get_everything(
        q=f'"{brand}"',
        language="en",
        sort_by="publishedAt",
        page_size=page_size
    )
    results = []
    for article in response["articles"]:
        results.append({
            "text": f"{article['title']}. {article['description'] or ''}",
            "url": article["url"],
            "published_at": article["publishedAt"],
            "source": "newsapi"
        })
    return results
