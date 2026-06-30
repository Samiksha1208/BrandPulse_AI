from app.agents.sentiment_agent import sentiment_agent

result = sentiment_agent.invoke({
    "messages": [{"role": "user", "content": "What's the sentiment on Tesla right now?"}]
})
print(result["messages"][-1].content)
