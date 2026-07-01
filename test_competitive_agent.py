from app.agents.competitive_agent import competitive_agent

try:
    result = competitive_agent.invoke({
        "messages": [{"role": "user", "content": "How does Tesla compare to Rivian right now?"}]
    })

    last_msg = result["messages"][-1]
    content = last_msg.content
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and "text" in block:
                print(block["text"])
            else:
                print(block)
    elif content:
        print(content)
    else:
        print("Empty content. Full message chain:")
        for i, msg in enumerate(result["messages"]):
            print(f"  [{i}] {type(msg).__name__}: {repr(msg.content)[:200]}")
except Exception as e:
    print(f"Error: {e}")
