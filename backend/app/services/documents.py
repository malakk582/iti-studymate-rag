from pathlib import Path
import re

from pypdf import PdfReader

SUPPORTED_SUFFIXES = {".md", ".txt", ".pdf"}


def read_documents(folder: str | Path) -> list[dict]:
    """Read supported documents recursively using paths relative to *folder*.

    Keeping the relative path in `source` prevents two files with the same
    basename in different subdirectories from colliding in the vector store.
    """
    folder = Path(folder).expanduser().resolve()
    if not folder.exists():
        raise FileNotFoundError(f"Documents folder does not exist: {folder}")
    if not folder.is_dir():
        raise NotADirectoryError(f"Documents path is not a directory: {folder}")

    records = []
    for path in sorted(folder.glob("**/*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_SUFFIXES:
            continue

        source = path.relative_to(folder).as_posix()
        if path.suffix.lower() in {".md", ".txt"}:
            text = path.read_text(encoding="utf-8")
            records.append({"source": source, "page": None, "text": text})
        else:
            reader = PdfReader(str(path))
            for page_no, page in enumerate(reader.pages, start=1):
                records.append({
                    "source": source,
                    "page": page_no,
                    "text": page.extract_text() or "",
                })
    return records


GUTENBERG_BOILERPLATE = re.compile(
    r"\*\*\*\s*(START|END) OF (THE|THIS) PROJECT GUTENBERG EBOOK[^*]*\*\*\*",
    re.IGNORECASE,
)


def clean_text(text: str) -> str:
    text = text or ""
    text = GUTENBERG_BOILERPLATE.sub(" ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def chunk_records(records: list[dict], chunk_size: int = 900, overlap: int = 150) -> list[dict]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size - 1")

    chunks = []
    for record in records:
        text = clean_text(record.get("text", ""))
        if not text:
            continue

        source = str(record["source"])
        page = record.get("page")
        start = 0
        part = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            # Prefer a natural boundary without creating tiny chunks.
            if end < len(text):
                boundary = text.rfind(" ", start, end)
                if boundary > start + chunk_size // 2:
                    end = boundary

            chunk_text = text[start:end].strip()
            if chunk_text:
                metadata = {"source": source, "chunk_id": part}
                if page is not None:
                    metadata["page"] = page
                chunks.append({
                    "id": f"{source}::{page if page is not None else 'na'}::{part}",
                    "text": chunk_text,
                    "metadata": metadata,
                })

            if end >= len(text):
                break
            start = max(end - overlap, start + 1)
            part += 1
    return chunks
