# ITI StudyMate — Presentation and Demo Script

## Slide 1 — Title
ITI StudyMate: A Grounded RAG Assistant for Training Materials.

## Slide 2 — Problem
Learners often search long training documents manually. A normal chatbot may hallucinate or answer without evidence. This project connects retrieval to generation so answers remain tied to a document collection.

## Slide 3 — Solution
The user asks a question. The system embeds the question, retrieves the most similar chunks from Chroma, gives those chunks to Ollama, and shows the answer with source metadata.

## Slide 4 — Pipeline
Document loading → cleaning → chunking with overlap → embeddings → persistent vector store → retrieval → grounded generation → cited UI response.

## Slide 5 — Backend and Frontend
FastAPI exposes `/health` and `/query`. Streamlit provides the chat-style interface and source cards. The API URL is configured through an environment variable.

## Slide 6 — Evaluation
The notebook tests at least ten representative questions. For each question, we inspect the retrieved source and mark retrieval relevance and answer grounding. Failure cases are discussed instead of hidden.

## Slide 7 — Demo
1. Start Ollama and run the API.
2. Start Streamlit.
3. Ask: “Why is chunk overlap useful in a RAG system?”
4. Show the grounded answer.
5. Expand Sources and point out the source, chunk ID, and similarity score.
6. Ask an unrelated question and show the safe insufficient-evidence response.

## Short spoken introduction
“ITI StudyMate is a document-grounded assistant. Its main purpose is not just to generate fluent text; it first retrieves evidence from the training materials, then asks the local model to answer only from that evidence. This makes the answer traceable and reduces hallucination.”
