FROM python:3.11-slim

WORKDIR /app

# System deps needed by sentence-transformers / chromadb wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# App code + the data the retriever ingests/serves
COPY backend/app ./app
COPY data ./data

ENV PYTHONUNBUFFERED=1 \
    VECTOR_STORE_PATH=/app/data/vector_store \
    DOCS_PATH=/app/data/documents

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
