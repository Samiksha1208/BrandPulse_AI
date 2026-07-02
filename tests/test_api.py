import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_crisis_check_returns_valid_schema():
    response = client.get("/brands/Tesla/crisis-check")
    assert response.status_code == 200
    data = response.json()
    assert "spike_detected" in data
    assert "spike_ratio" in data
    assert "message" in data

def test_sentiment_returns_series():
    response = client.get("/brands/Tesla/sentiment?days=7")
    assert response.status_code == 200
    data = response.json()
    assert "series" in data
    assert len(data["series"]) == 7
    assert "total_mentions" in data

def test_ingest_returns_valid_schema():
    response = client.post("/ingest", json={"brand": "Tesla"})
    assert response.status_code == 200
    data = response.json()
    assert "new_items" in data
    assert "chunks_indexed" in data

def test_query_missing_fields_returns_422():
    response = client.post("/query", json={"question": "test"})
    assert response.status_code == 422
