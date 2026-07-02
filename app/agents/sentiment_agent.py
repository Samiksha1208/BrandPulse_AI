from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from app.retrieval.hybrid_search import hybrid_search

model = init_chat_model("google_genai:gemini-2.0-flash", temperature=0)

def retrieve_brand_content(brand: str, query: str) -> str:
    """Retrieve the most relevant recent content chunks about a brand."""
    hits = hybrid_search(query, brand, k=8)
    return "\n\n".join(f"[{h['_source']['url']}] {h['_source']['content']}" for h in hits)

SENTIMENT_SYSTEM_PROMPT = """You are the Sentiment & Narrative Agent inside BrandPulse AI.
Retrieve relevant content using the retrieve_brand_content tool, then produce a structured sentiment analysis grounded only in retrieved evidence.
Include: overall sentiment direction, 2-4 dominant themes, and supporting evidence with source URLs.
Never state a sentiment conclusion without it being traceable to retrieved content."""

sentiment_agent = create_react_agent(
    model=model,
    tools=[retrieve_brand_content],
    name="sentiment_agent",
    prompt=SENTIMENT_SYSTEM_PROMPT
)
