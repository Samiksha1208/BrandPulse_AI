import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

es = Elasticsearch(
    os.getenv("ES_URL"),
    api_key=os.getenv("ES_API_KEY")
)

INDEX_NAME = os.getenv("ES_INDEX_NAME", "brandpulse-content")
