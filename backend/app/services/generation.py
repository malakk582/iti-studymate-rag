SYSTEM_PROMPT = """You are ITI StudyMate, a careful document-grounded assistant.
Answer the question using the supplied context below. The context may state facts
directly or imply them — if a reasonable person reading the context would consider
the question answered, give that answer clearly and directly.
Only say "I don't have enough information in the provided documents" if the context
truly contains nothing relevant to the question.
Do not use outside knowledge beyond what is in the context.
Do not invent sources, page numbers, chunk IDs, or citations.
Keep answers concise and factual.
When you use a retrieved passage, cite it inline as [source: <filename>, chunk: <chunk_id>].
"""


class Generator:
    def __init__(self, host: str, model: str):
        import ollama
        self.client = ollama.Client(host=host)
        self.model = model

    def answer(self, question: str, retrieved: list[dict]) -> str:
        context = "\n\n".join(
            f"[{i + 1}] source={item['metadata'].get('source')}, chunk={item['metadata'].get('chunk_id')}: {item['text']}"
            for i, item in enumerate(retrieved)
        )
        response = self.client.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Question: {question}\n\nContext:\n{context}"},
            ],
        )
        return response["message"]["content"].strip()