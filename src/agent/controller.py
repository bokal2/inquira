from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from src.agent.llm_setup import response_chain
from src.rate_limiting import limiter

router = APIRouter(prefix="/agent", tags=["Agent"])


class QueryRequest(BaseModel):
    question: str


@router.post("/query")
@limiter.limit("5/minute")
def query_db(request: Request, req: QueryRequest):
    try:
        result = response_chain.invoke({"question": req.question})
        return {"response": result.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
