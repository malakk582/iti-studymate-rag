from functools import lru_cache
from pathlib import Path

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/app/core/config.py -> project root
ROOT_DIR = Path(__file__).resolve().parents[3]
BACKEND_DIR = ROOT_DIR / "backend"


class Settings(BaseSettings):
    """Application settings with paths anchored to the project, not the cwd."""

    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:3b"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    vector_store_path: str = str(ROOT_DIR / "data" / "vector_store")
    docs_path: str = str(ROOT_DIR / "data" / "documents")
    top_k: int = 4
    min_retrieval_score: float = 0.35

    # Support both documented locations. backend/.env is loaded after the root
    # .env, so a component-specific value can override the shared configuration.
    model_config = SettingsConfigDict(
        env_file=(str(ROOT_DIR / ".env"), str(BACKEND_DIR / ".env")),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @model_validator(mode="after")
    def resolve_project_paths(self):
        """Resolve relative data paths against the project root.

        This prevents the classic `data/documents does not exist` failure when
        Uvicorn is launched from `backend/` instead of the repository root.
        """
        for field_name in ("vector_store_path", "docs_path"):
            value = Path(getattr(self, field_name)).expanduser()
            if not value.is_absolute():
                value = ROOT_DIR / value
            setattr(self, field_name, str(value.resolve()))
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
