from pathlib import Path
import sys

from fastapi.testclient import TestClient

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import app.main as main_module
from app.main import app


class FakeRetriever:
    def __init__(self, *args, **kwargs):
        pass

    def search(self, question, top_k, min_score=0.0):
        return []


class FakeGenerator:
    def __init__(self, *args, **kwargs):
        pass


def setup_fakes(monkeypatch):
    monkeypatch.setattr(main_module, "Retriever", FakeRetriever)
    monkeypatch.setattr(main_module, "Generator", FakeGenerator)


def test_health(monkeypatch):
    setup_fakes(monkeypatch)
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


def test_invalid_query(monkeypatch):
    setup_fakes(monkeypatch)
    with TestClient(app) as client:
        response = client.post("/query", json={"question": "x"})
        assert response.status_code == 422


def test_blank_query_is_rejected(monkeypatch):
    setup_fakes(monkeypatch)
    with TestClient(app) as client:
        response = client.post("/query", json={"question": "   "})
        assert response.status_code == 422


def test_empty_corpus_returns_grounded_fallback(monkeypatch):
    setup_fakes(monkeypatch)
    with TestClient(app) as client:
        response = client.post("/query", json={"question": "What is RAG?"})
        assert response.status_code == 200
        assert response.json()["sources"] == []
        assert "enough information" in response.json()["answer"]
