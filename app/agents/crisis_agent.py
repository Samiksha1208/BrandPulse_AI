from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from app.retrieval.hybrid_search import hybrid_search
from app.agents.crisis_detection import detect_volume_spike

model = init_chat_model("google_genai:gemini-2.0-flash", temperature=0)

def check_for_crisis(brand: str) -> dict:
    """Check whether a brand currently has an anomalous spike in mention volume."""
    return detect_volume_spike(brand)

def retrieve_brand_content(brand: str, query: str) -> str:
    """Retrieve the most relevant recent content chunks about a brand."""
    hits = hybrid_search(query, brand, k=8)
    return "\n\n".join(f"[{h['_source']['url']}] {h['_source']['content']}" for h in hits)

CRISIS_SYSTEM_PROMPT = """You are the Crisis Detection Agent inside BrandPulse AI.

First, call check_for_crisis to see if there's an anomalous spike in mention volume for the brand.
If is_anomaly is false, clearly state there is no crisis-level anomaly right now and stop.
If is_anomaly is true, call retrieve_brand_content to find out what's driving the spike, then draft a brief with:
1. What happened (1-2 factual sentences, no speculation)
2. Why it triggered the spike, citing specific retrieved sources
3. Severity: LOW / MEDIUM / HIGH, with one sentence of justification
4. One recommended next step

Never escalate severity beyond what the evidence supports. Keep the brief under 150 words.
This is a recommendation for human review, not a final declaration — say so explicitly."""

crisis_agent = create_react_agent(
    model=model,
    tools=[check_for_crisis, retrieve_brand_content],
    name="crisis_agent",
    prompt=CRISIS_SYSTEM_PROMPT
)
