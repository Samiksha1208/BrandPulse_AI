from app.ingestion.newsapi_source import fetch_news
from app.ingestion.rss_source import fetch_rss

brand = "Tesla"

news = fetch_news(brand)
print(f"NewsAPI: {len(news)} articles")
if news:
    print(news[0])

# Reddit skipped — waiting for API approval
print("\nReddit: SKIPPED (waiting for API permission)")

rss_items = fetch_rss(brand)
print(f"\nRSS: {len(rss_items)} items")
if rss_items:
    print(rss_items[0])
