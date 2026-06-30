import feedparser

FEEDS = [
    "https://techcrunch.com/feed/",
    "http://feeds.bbci.co.uk/news/business/rss.xml",
]

def fetch_rss(brand: str) -> list[dict]:
    results = []
    for feed_url in FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            if brand.lower() in (entry.title + entry.get("summary", "")).lower():
                results.append({
                    "text": f"{entry.title}. {entry.get('summary', '')}",
                    "url": entry.link,
                    "published_at": entry.get("published", ""),
                    "source": "rss"
                })
    return results
