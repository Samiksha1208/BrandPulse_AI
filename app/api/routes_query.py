from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest, QueryResponse
from app.agents.supervisor import graph

router = APIRouter()

@router.post("", response_model=QueryResponse)
async def query(req: QueryRequest):
    try:
        result = graph.invoke(
            {
                "messages": [{"role": "user", "content": req.question}],
                "brand": req.brand,
                "competitors": req.competitors
            },
            config={"configurable": {"thread_id": req.session_id}}
        )
        return QueryResponse(
            answer=result["messages"][-1].content,
            session_id=req.session_id,
            brand=req.brand
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
