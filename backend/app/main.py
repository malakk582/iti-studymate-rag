from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes.query import router as query_router
from .core.config import get_settings
from .services.generation import Generator
from .services.retrieval import Retriever
from .utils.logging_config import configure_logging, logger

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    app.state.settings = settings
    state: dict = {}
    docs_path = settings.docs_path
    try:
        logger.info("Loading vector store from %s", settings.vector_store_path)
        state["retriever"] = Retriever(settings.vector_store_path, settings.embedding_model, docs_path)
        state["generator"] = Generator(settings.ollama_host, settings.ollama_model)
        state["startup_error"] = None
        logger.info("Startup complete: RAG service ready")
    except Exception as exc:
        logger.exception("Startup failed")
        state["startup_error"] = str(exc)
    app.state.rag = state
    yield
    app.state.rag.clear()


app = FastAPI(title="ITI StudyMate RAG API", version="1.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
app.include_router(query_router)
