import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph_supervisor import create_supervisor
from langgraph.checkpoint.postgres import PostgresSaver
import psycopg
from app.agents.sentiment_agent import sentiment_agent
from app.agents.crisis_agent import crisis_agent
from app.agents.competitive_agent import competitive_agent

load_dotenv()

SUPERVISOR_PROMPT = """You are the orchestration supervisor for BrandPulse AI.

You manage three specialist agents:
- sentiment_agent: analyzes sentiment and narrative themes for a brand from recent content
- crisis_agent: checks for mention-volume anomalies that may indicate a reputational crisis
- competitive_agent: compares share of voice and sentiment between a brand and named competitors

Rules for routing:
1. Questions about general sentiment, opinion, or "what people are saying" → sentiment_agent
2. Questions about risk, anomalies, spikes, or "is something wrong" → crisis_agent
3. Questions mentioning a competitor by name or asking for comparison → competitive_agent
4. Multi-part questions needing more than one perspective → route to each relevant agent
   sequentially, then synthesize into one final answer
5. Once you have enough information to fully answer, respond directly and stop routing

Never fabricate data. If no specialist has retrieved relevant information, say so honestly."""

def build_graph():
    model = init_chat_model("google_genai:gemini-2.0-flash", temperature=0)

    workflow = create_supervisor(
        agents=[sentiment_agent, crisis_agent, competitive_agent],
        model=model,
        prompt=SUPERVISOR_PROMPT
    )

    db_url = os.getenv("DATABASE_URL")

    # Setup requires autocommit for CREATE INDEX CONCURRENTLY
    setup_conn = psycopg.connect(db_url, autocommit=True)
    setup_checkpointer = PostgresSaver(setup_conn)
    setup_checkpointer.setup()
    setup_conn.close()

    # Regular connection for checkpointing
    conn = psycopg.connect(db_url)
    checkpointer = PostgresSaver(conn)

    return workflow.compile(checkpointer=checkpointer)

graph = build_graph()
