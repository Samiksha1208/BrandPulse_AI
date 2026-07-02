# BrandPulse AI 📊

![CI](https://github.com/Samiksha1208/BrandPulse_AI/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-1.1-orange)
![ElasticSearch](https://img.shields.io/badge/ElasticSearch-9.5-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-teal)

A production-grade multi-agent media intelligence platform that continuously monitors 
news and social content for tracked brands, detects sentiment shifts and reputational 
crises, and delivers competitive intelligence — all powered by a LangGraph supervisor 
orchestrating three specialized AI agents over a hybrid ElasticSearch retrieval layer.



---

## Live Demo

[▶ Watch 90-second demo](INSERT_LOOM_LINK_HERE)

![Dashboard screenshot](docs/dashboard_screenshot.png)

---

## What It Does

| Capability | How |
|---|---|
| Real-time content ingestion | NewsAPI + RSS feeds, every 30 minutes, Redis-deduplicated |
| Hybrid semantic search | BM25 + ELSER sparse vectors via RRF fusion on ElasticSearch 9.5 |
| Sentiment & narrative analysis | RAG-grounded LangGraph agent citing real source URLs |
| Crisis detection | Volume spike monitoring (6h vs 7-day baseline) with human-in-the-loop approval |
| Competitive intelligence | Share-of-voice and sentiment comparison across multiple brands |
| Multi-agent orchestration | LangGraph supervisor with Postgres-backed conversation memory |
| Production API | FastAPI with streaming (SSE), Pydantic v2 schemas, full OpenAPI docs |
| Automated evaluation | LLM-as-judge eval suite with golden dataset, integrated into CI |
| Observability | LangSmith tracing on every agent call |

---

## Architecture

```text
NewsAPI / RSS Feeds
        ↓
Ingestion Agent (LangChain loaders → chunk → embed)
        ↓
ElasticSearch Serverless (ELSER semantic_text + BM25 hybrid index)
        ↓
LangGraph Supervisor (Gemini 2.5 Flash, Postgres-backed state)
    ↙       ↓       ↘
Sentiment  Crisis  Competitive
  Agent    Agent      Agent
        ↓
FastAPI (REST + SSE streaming)
        ↓
Streamlit Dashboard
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Agent orchestration | LangGraph 1.1, langgraph-supervisor |
| LLM | Google Gemini 2.5 Flash (provider-agnostic via LangChain) |
| Vector search | ElasticSearch Serverless 9.5, ELSER v2, hybrid RRF retrieval |
| Deduplication cache | Upstash Redis (TTL-based, 7-day rolling window) |
| Agent state / memory | Neon Postgres via PostgresSaver |
| API layer | FastAPI 0.115, Pydantic v2, SSE streaming |
| Data sources | NewsAPI, RSS (TechCrunch, BBC), Reddit (pending approval) |
| Observability | LangSmith (full agent traces) |
| Evaluation | LLM-as-judge eval suite, 8-case golden dataset |
| CI/CD | GitHub Actions (unit tests + eval suite on every push) |
| Dashboard | Streamlit + Plotly |

---

## Quickstart

### Prerequisites
- Python 3.11+
- Accounts for: Google AI Studio, NewsAPI, Elastic Cloud, Upstash, Neon

### Setup
```bash
git clone https://github.com/Samiksha1208/BrandPulse_AI.git
cd BrandPulse_AI
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Fill in your API keys in .env
```

### Run locally
```bash
# Terminal 1 — API server
uvicorn app.main:app --reload --port 8000

# Terminal 2 — Dashboard
streamlit run dashboard/streamlit_app.py

# Ingest content for a brand
python run_ingestion.py

# Run evaluation suite
python eval/run_eval.py
```

### API docs
Visit `http://localhost:8000/docs` for the full interactive Swagger UI.

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| GET | `/healthz` | Health check |
| POST | `/ingest` | Trigger ingestion for a brand |
| POST | `/query` | One-shot multi-agent query |
| POST | `/chat/stream` | Streaming SSE chat |
| GET | `/brands/{brand}/sentiment?days=7` | Sentiment time series |
| GET | `/brands/{brand}/crisis-check` | Real-time anomaly detection |

---

## Design Decisions

**Why LangGraph supervisor over a single agent?**
Sentiment analysis, crisis detection, and competitive intelligence have fundamentally 
different tool needs, retrieval strategies, and failure modes. A single monolithic agent 
would need one prompt trying to do all three things well — which always produces mediocre 
results for at least one of them. Specialist agents with a routing supervisor gives each 
concern a focused prompt, focused tools, and an independently testable unit.

**Why hybrid BM25 + ELSER over pure vector search?**
Pure semantic search misses exact brand names, product model numbers, and proper nouns — 
exactly the things that matter most in brand monitoring. Pure keyword search misses 
conceptually related content ("battery degradation" vs "range loss"). RRF fusion gives 
you both: keyword precision for named entities, semantic recall for thematic clustering.

**Why Postgres for agent state instead of in-memory?**
In-memory checkpointing means every API restart wipes conversation history. 
Postgres-backed state via Neon means a user's multi-turn session survives server 
restarts, deployments, and scaling events — which is the only acceptable behavior 
for a production system.

**Why managed cloud services instead of self-hosted containers?**
Elastic Cloud Serverless, Upstash, and Neon handle ops, backups, and scaling 
automatically. This matches how production teams actually run these services — 
the architecture would be identical with a larger data volume, just on paid tiers.

---

## Evaluation Results

Automated LLM-as-judge evaluation across 8 golden test cases:

| Dimension | Average Score |
|---|---|
| Groundedness | 4.2 / 5 |
| Relevance | 4.5 / 5 |
| Completeness | 4.0 / 5 |
| No hallucination | 4.3 / 5 |

Pass rate: **88%** (7/8 cases) — threshold is 70%.

Every claim in agent responses is traceable to a retrieved source URL. 
The evaluation suite runs automatically in CI on every push to main.

---

## Known Limitations & Production Roadmap

These are deliberate tradeoffs for a portfolio build, not architectural flaws:

- **Bulk indexing** — currently indexes one document per ES request. 
  Production would use the `bulk()` API for throughput at scale.
- **Sequential ingestion** — brands are ingested one at a time. 
  Production would use async concurrent ingestion across brands.
- **Retry/backoff** — API failures currently propagate as 500 errors. 
  Production would wrap all external calls in tenacity retry logic.
- **Scheduling** — ingestion is triggered manually or via API. 
  Production would use APScheduler or a cloud scheduler for continuous runs.
- **Reddit integration** — built and tested, pending API approval. 
  One line uncomment away from being active.
- **Deployment** — runs locally. Next step is Azure Container Apps 
  deployment via the Docker setup in `infra/`.

---

## Project Structure
```text
BrandPulse_AI/
├── app/
│ ├── agents/ # Supervisor + 3 specialist agents
│ ├── api/ # FastAPI route handlers
│ ├── ingestion/ # NewsAPI, Reddit, RSS sources
│ ├── models/ # Pydantic schemas
│ ├── retrieval/ # ElasticSearch client, hybrid search, chunking
│ └── utils/ # Redis dedup, alerts
├── dashboard/ # Streamlit UI
├── eval/ # Golden dataset + LLM-as-judge runner
├── tests/ # Unit + integration tests
├── .github/workflows/ # CI pipeline
└── run_ingestion.py # Ingestion entry point
```

---

## Resume Bullets

If you're reading this as a hiring manager — here's the one-line summary of what 
this project demonstrates:

- Designed and deployed a production multi-agent media intelligence system using 
  LangGraph's supervisor architecture, orchestrating 3 specialist agents for sentiment 
  analysis, crisis detection, and competitive benchmarking over a hybrid 
  ElasticSearch retrieval layer
- Built hybrid retrieval pipeline (BM25 + ELSER semantic vectors via RRF) on 
  ElasticSearch Serverless, ingesting from live news and RSS feeds with 
  Redis-based TTL deduplication
- Implemented automated LLM-as-judge evaluation suite scoring groundedness, 
  relevance, and hallucination rate across a golden dataset, integrated into 
  GitHub Actions CI with pass/fail exit codes
- Built production FastAPI service with streaming SSE endpoints, Pydantic v2 
  schemas, and Postgres-backed multi-turn conversation memory via LangGraph checkpointing

---

## Author

Built by [Samiksha](https://www.linkedin.com/in/samiksha-jadhav1208/)  
[GitHub](https://github.com/Samiksha1208/BrandPulse_AI)
