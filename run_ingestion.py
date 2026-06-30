from app.ingestion.newsapi_source import fetch_news
from app.ingestion.rss_source import fetch_rss
from app.retrieval.indexer import index_items
from app.utils.dedup import is_seen, mark_seen

def run_ingestion_cycle(brand: str):
    raw_items = fetch_news(brand) + fetch_rss(brand)
    # raw_items += fetch_reddit(brand)  # uncomment once Reddit is approved

    new_items = [item for item in raw_items if not is_seen(item["url"])]
    print(f"{len(new_items)} new items out of {len(raw_items)} fetched")

    if new_items:
        count = index_items(new_items, brand)
        print(f"Indexed {count} chunks into ElasticSearch")
        for item in new_items:
            mark_seen(item["url"])
    else:
        print("Nothing new to index.")

if __name__ == "__main__":
    run_ingestion_cycle("Tesla")
