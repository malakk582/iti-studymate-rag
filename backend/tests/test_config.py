from pathlib import Path
import os
import sys

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.core.config import ROOT_DIR, Settings


def test_default_data_paths_are_absolute_and_project_anchored(monkeypatch):
    monkeypatch.delenv("DOCS_PATH", raising=False)
    monkeypatch.delenv("VECTOR_STORE_PATH", raising=False)
    settings = Settings(_env_file=None)

    assert Path(settings.docs_path).is_absolute()
    assert Path(settings.vector_store_path).is_absolute()
    assert Path(settings.docs_path) == ROOT_DIR / "data" / "documents"
    assert Path(settings.vector_store_path) == ROOT_DIR / "data" / "vector_store"


def test_relative_env_paths_are_resolved_against_project_root(monkeypatch):
    monkeypatch.setenv("DOCS_PATH", "./data/documents")
    monkeypatch.setenv("VECTOR_STORE_PATH", "./data/vector_store")
    settings = Settings(_env_file=None)

    assert Path(settings.docs_path) == ROOT_DIR / "data" / "documents"
    assert Path(settings.vector_store_path) == ROOT_DIR / "data" / "vector_store"
