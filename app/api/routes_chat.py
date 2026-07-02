from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.models.schemas import QueryRequest
from app.agents.supervisor import graph
import json

router = APIRouter()

@router.post("/stream")
async def stream_chat(req: QueryRequest):
    async def event_generator():
        try:
            for chunk in graph.stream(
                {
                    "messages": [{"role": "user", "content": req.question}],
                    "brand": req.brand,
                    "competitors": req.competitors
                },
                config={"configurable": {"thread_id": req.session_id}},
                stream_mode="values"
            ):
                last_msg = chunk["messages"][-1]
                if hasattr(last_msg, "content") and last_msg.content:
                    yield f"data: {json.dumps({'content': last_msg.content})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
