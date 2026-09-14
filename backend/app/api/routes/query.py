from fastapi import APIRouter, HTTPException, Request

from ...schemas.query import QueryRequest, QueryResponse, Source
from ...utils.logging_config import logger

router = APIRouter()


@router.get("/health")
def health(request: Request):
    state = request.app.state.rag
    if state.get("startup_error"):
        return {"status": "degraded", "service": "iti-studymate-rag", "error": state["startup_error"]}
    return {"status": "ok", "service": "iti-studymate-rag"}


@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest, req: Request):
    state = req.app.state.rag
    settings = req.app.state.settings

    if state.get("startup_error"):
        raise HTTPException(status_code=503, detail=f"Service failed to start: {state['startup_error']}")

    retriever = state.get("retriever")
    generator = state.get("generator")
    if not retriever or not generator:
        raise HTTPException(status_code=503, detail="Service is still starting")

    question = request.question.strip()
    top_k = request.top_k or settings.top_k

    logger.info("query received: %r (top_k=%s)", question, top_k)
    retrieved = retriever.search(question, top_k, settings.min_retrieval_score)

    if not retrieved:
        logger.info("no chunks retrieved for question")
        return QueryResponse(
            answer="I don't have enough information in the provided documents.",
            sources=[],
        )

    try:
        answer = generator.answer(question, retrieved)
    except Exception as exc:
        logger.exception("LLM generation failed")
        raise HTTPException(
            status_code=502,
            detail="LLM generation failed. Check that Ollama is running and the configured model is available.",
        ) from exc

    sources = [
        Source(
            source=item["metadata"].get("source", "unknown"),
            chunk_id=str(item["metadata"].get("chunk_id", "")),
            page=item["metadata"].get("page"),
            score=round(item["score"], 4),
            text=item["text"],
        )
        for item in retrieved
    ]
    return QueryResponse(answer=answer, sources=sources)
