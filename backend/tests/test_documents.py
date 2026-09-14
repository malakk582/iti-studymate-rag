from pathlib import Path
import sys

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.services.documents import chunk_records, read_documents


def test_read_documents_uses_relative_paths(tmp_path):
    docs = tmp_path / "documents"
    (docs / "course_a").mkdir(parents=True)
    (docs / "course_b").mkdir(parents=True)
    (docs / "course_a" / "notes.txt").write_text("alpha", encoding="utf-8")
    (docs / "course_b" / "notes.txt").write_text("beta", encoding="utf-8")

    records = read_documents(docs)
    assert [r["source"] for r in records] == ["course_a/notes.txt", "course_b/notes.txt"]

    chunks = chunk_records(records, chunk_size=100, overlap=0)
    assert len({c["id"] for c in chunks}) == 2
    assert {c["metadata"]["source"] for c in chunks} == {
        "course_a/notes.txt",
        "course_b/notes.txt",
    }


def test_missing_documents_path_has_clear_error(tmp_path):
    missing = tmp_path / "does-not-exist"
    try:
        read_documents(missing)
    except FileNotFoundError as exc:
        assert str(missing.resolve()) in str(exc)
    else:
        raise AssertionError("read_documents should fail for a missing folder")
