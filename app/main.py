import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api.routes_query import router as query_router
from app.api.routes_ingest import router as ingest_router
from app.api.routes_brand import router as brand_router
from app.api.routes_chat import router as chat_router

load_dotenv()

app = FastAPI(
    title="BrandPulse AI",
    description="Multi-agent media intelligence platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(query_router, prefix="/query", tags=["query"])
app.include_router(ingest_router, prefix="/ingest", tags=["ingestion"])
app.include_router(brand_router, prefix="/brands", tags=["brand"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])

@app.get("/healthz", tags=["health"])
def health():
    return {"status": "ok", "version": "1.0.0"}
