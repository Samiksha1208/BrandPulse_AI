import requests
import json

base_url = "http://127.0.0.1:8000"

print("1. Health Check:")
try:
    r = requests.get(f"{base_url}/healthz")
    print(json.dumps(r.json(), indent=2))
except Exception as e:
    print(f"Failed: {e}")

print("\n2. Ingest Tesla:")
try:
    r = requests.post(f"{base_url}/ingest", json={"brand": "Tesla"})
    print(json.dumps(r.json(), indent=2))
except Exception as e:
    print(f"Failed: {e}")

print("\n3. Crisis Check Tesla:")
try:
    r = requests.get(f"{base_url}/brands/Tesla/crisis-check")
    print(json.dumps(r.json(), indent=2))
except Exception as e:
    print(f"Failed: {e}")

print("\n4. Sentiment Tesla (7 days):")
try:
    r = requests.get(f"{base_url}/brands/Tesla/sentiment?days=7")
    print(json.dumps(r.json(), indent=2))
except Exception as e:
    print(f"Failed: {e}")
