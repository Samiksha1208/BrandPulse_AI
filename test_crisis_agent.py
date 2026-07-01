from app.agents.crisis_agent import crisis_agent

result = crisis_agent.invoke({
    "messages": [{"role": "user", "content": "Is there anything alarming happening with Tesla right now?"}]
})
print(result["messages"][-1].content)
