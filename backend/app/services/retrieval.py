from pathlib import Path

from .documents import chunk_records, read_documents


class Retriever:
    """Persistent semantic retriever backed by Chroma + Sentence Transformers."""

    COLLECTION_NAME = "iti_studymate"

    def __init__(self, vector_store_path: str, embedding_model: str, documents_path: str | Path | None = None):
        # Lazy imports keep API validation/tests usable even before ML dependencies are installed.
        import chromadb
        from sentence_transformers import SentenceTransformer

        self.vector_store_path = str(Path(vector_store_path).expanduser().resolve())
        Path(self.vector_store_path).mkdir(parents=True, exist_ok=True)
        self.embedder = SentenceTransformer(embedding_model)
        self.client = chromadb.PersistentClient(path=self.vector_store_path)
        self.collection = self.client.get_or_create_collection(
            self.COLLECTION_NAME,
            metadata={"hnsw:space": "l2"},
        )
        if self.collection.count() == 0 and documents_path:
            self.ingest(documents_path)

    def ingest(self, documents_path: str | Path, *, reset: bool = False) -> int:
        """Index documents. Use reset=True when the source corpus changed substantially."""
        records = read_documents(documents_path)
        chunks = chunk_records(records)
        if reset:
            self.client.delete_collection(self.COLLECTION_NAME)
            self.collection = self.client.get_or_create_collection(
                self.COLLECTION_NAME,
                metadata={"hnsw:space": "l2"},
            )
        if not chunks:
            return 0

        texts = [c["text"] for c in chunks]
        embeddings = self.embedder.encode(texts, normalize_embeddings=True).tolist()
        self.collection.upsert(
            ids=[c["id"] for c in chunks],
            documents=texts,
            metadatas=[c["metadata"] for c in chunks],
            embeddings=embeddings,
        )
        return len(chunks)

    def search(self, question: str, top_k: int = 4, min_score: float = 0.0) -> list[dict]:
        if self.collection.count() == 0:
            return []
        query_embedding = self.embedder.encode([question], normalize_embeddings=True).tolist()
        result = self.collection.query(
            query_embeddings=query_embedding,
            n_results=min(top_k, self.collection.count()),
            include=["documents", "metadatas", "distances"],
        )
        items = []
        for idx, text in enumerate(result["documents"][0]):
            metadata = result["metadatas"][0][idx] or {}
            distance = float(result["distances"][0][idx])
            items.append({
                "text": text,
                "metadata": metadata,
                # Embeddings are normalized, so squared L2 distance d maps to
                # cosine similarity as cos = 1 - d/2. Chroma stores L2 distance here.
                "score": max(0.0, min(1.0, 1.0 - (distance / 2.0))),
            })
        return [item for item in items if item["score"] >= min_score]
