from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from app.retrieval.hybrid_search import hybrid_search

model = init_chat_model("google_genai:gemini-2.0-flash", temperature=0)

def retrieve_brand_content(brand: str, query: str) -> str:
    """Retrieve the most relevant recent content chunks about a specific brand. Call this once per brand you want to compare."""
    try:
        hits = hybrid_search(query, brand, k=8)
        if not hits:
            return f"No content found for {brand}."
        return "\n\n".join(f"[{h['_source']['url']}] {h['_source']['content']}" for h in hits)
    except Exception as e:
        return f"Error retrieving content for {brand}: {str(e)}"

COMPETITIVE_SYSTEM_PROMPT = """You are the Competitive Intelligence Agent inside BrandPulse AI.

Given a primary brand and one or more competitor brands, call retrieve_brand_content for each brand
one at a time. Use a query relevant to the user's question.

Then produce:
1. A short summary stating who currently "leads the conversation" and why
2. A comparison breakdown: brand | approx. mention volume (count chunks retrieved) | dominant sentiment | key theme
3. One forward-looking recommendation for the primary brand's communications strategy

Ground every comparison in retrieved evidence. If a competitor has too little retrieved content
to compare fairly, say so explicitly instead of guessing. Never invent volume or sentiment data
for a brand you have not actually retrieved content for.

IMPORTANT: Always call the tool for each brand separately, never skip this step."""

competitive_agent = create_react_agent(
    model=model,
    tools=[retrieve_brand_content],
    name="competitive_agent",
    prompt=COMPETITIVE_SYSTEM_PROMPT
)
