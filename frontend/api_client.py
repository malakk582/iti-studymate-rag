"""Thin wrapper around the backend API so app.py never talks to `requests` directly."""
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load frontend/.env explicitly (not relying on cwd) so this works whether Streamlit
# is launched from the repo root, from inside frontend/, or via an absolute path.
load_dotenv(Path(__file__).resolve().parent / ".env")

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")


class BackendError(Exception):
    """Raised when the backend call fails (timeout, connection error, or bad response)."""


def health_check(timeout: float = 5.0) -> dict:
    response = requests.get(f"{API_BASE_URL}/health", timeout=timeout)
    response.raise_for_status()
    return response.json()


def ask_question(question: str, top_k: int = 4, timeout: float = 120.0) -> dict:
    """Send a question to the backend and return the parsed {answer, sources} payload.

    Raises BackendError with a user-friendly message on any failure.
    """
    try:
        response = requests.post(
            f"{API_BASE_URL}/query",
            json={"question": question, "top_k": top_k},
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json()
    except requests.Timeout as exc:
        raise BackendError(
            "The request timed out. Make sure Ollama is running and the model is loaded."
        ) from exc
    except requests.RequestException as exc:
        detail = getattr(exc.response, "text", "") if exc.response is not None else ""
        raise BackendError(f"Backend request failed: {detail or exc}") from exc
