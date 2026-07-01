import time
from app.agents.supervisor import graph

def print_result(result):
    last = result["messages"][-1]
    content = last.content
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and "text" in block:
                print(block["text"])
            else:
                print(block)
    elif content:
        print(content)
    else:
        print("[Empty response]")

# Test 1: pure sentiment question
config = {"configurable": {"thread_id": "test-thread-001"}}
print("=== TEST 1: Sentiment routing ===")
result = graph.invoke({
    "messages": [{"role": "user", "content": "What's the overall sentiment on Tesla this week?"}],
    "brand": "Tesla",
    "competitors": []
}, config=config)
print_result(result)

# Wait 60s to reset Gemini rate limit (5 req/min on free tier)
print("\n--- Waiting 60s for rate limit reset ---")
time.sleep(60)

# Test 2: multi-agent question
config2 = {"configurable": {"thread_id": "test-thread-002"}}
print("\n=== TEST 2: Multi-agent routing ===")
result2 = graph.invoke({
    "messages": [{"role": "user", "content": "How is Tesla's sentiment compared to Rivian?"}],
    "brand": "Tesla",
    "competitors": ["Rivian"]
}, config=config2)
print_result(result2)

# Wait 60s again
print("\n--- Waiting 60s for rate limit reset ---")
time.sleep(60)

# Test 3: follow-up in the SAME thread — tests Postgres memory
print("\n=== TEST 3: Memory across turns (same thread) ===")
result3 = graph.invoke({
    "messages": [{"role": "user", "content": "Which of the two has more legal issues?"}],
    "brand": "Tesla",
    "competitors": ["Rivian"]
}, config=config2)   # same thread_id as test 2
print_result(result3)
