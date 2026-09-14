# ITI StudyMate: RAG Notes

## What is Retrieval-Augmented Generation?
Retrieval-Augmented Generation, or RAG, combines information retrieval with text generation. Instead of asking a language model to answer from its parameters alone, the system retrieves relevant passages from a trusted document collection and includes them in the prompt. This helps the answer stay grounded in the available evidence.

## RAG pipeline
A practical RAG pipeline has five stages: document loading, text cleaning and chunking, embedding generation, vector search, and answer generation. Each chunk should keep metadata such as its source filename, page number when available, and a unique chunk identifier.

## Chunking
Chunking divides long documents into smaller passages that fit retrieval and model context limits. Fixed-size chunks are easy to implement, while semantic or section-based chunks can preserve meaning better. A small overlap between neighboring chunks prevents important sentences from being cut at boundaries.

## Embeddings and vector databases
An embedding is a numeric representation of text in a vector space. Texts with related meanings tend to have nearby vectors. A vector database stores embeddings and metadata, then returns the most similar chunks for a query. Cosine similarity is commonly used to compare normalized embeddings.

## Grounded answers and citations
The generation prompt should instruct the model to use only the supplied context. If the context does not contain the answer, the assistant should say that the information is not available. Every answer should cite the retrieved source filename and chunk identifier so the user can verify it.

## API and frontend
FastAPI can expose a health endpoint and a query endpoint for the RAG service. A Streamlit frontend can send a user question to the API and display the answer together with source cards. The API URL should come from an environment variable rather than being hard-coded.

## Evaluation
A small evaluation set should contain representative questions with expected source documents and expected concepts. Retrieval is relevant when the returned chunks contain evidence for the question. The final answer is grounded when it is supported by the retrieved context and does not invent unsupported facts.
