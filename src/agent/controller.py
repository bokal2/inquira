from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from src.agent.llm_setup import response_chain, sql_chain
from src.rate_limiting import limiter

router = APIRouter(prefix="/agent", tags=["Agent"])


class QueryRequest(BaseModel):
    question: str


@router.post("/query")
@limiter.limit("5/minute")
def query_db(request: Request, req: QueryRequest):
    try:
        sql_query = sql_chain.invoke({"question": req.question})

        result = response_chain.invoke(
            {
                "question": req.question,
                "query": sql_query,
            }
        )

        return {
            "answer": result.content.strip(),
            "query": sql_query,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
