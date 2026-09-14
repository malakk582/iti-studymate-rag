
import streamlit as st

from api_client import API_BASE_URL, BackendError, ask_question

st.set_page_config(page_title="ITI StudyMate", page_icon="📚", layout="centered")
st.title("📚 ITI StudyMate")
st.caption("Document-grounded RAG assistant for ITI training materials")

with st.sidebar:
    st.subheader("Settings")
    top_k = st.slider("Retrieved sources", min_value=1, max_value=10, value=4)
    st.caption(f"Backend: {API_BASE_URL}")

question = st.text_area(
    "Ask a question",
    placeholder="What is the purpose of chunking in RAG?",
    height=120,
)

if st.button("Ask StudyMate", type="primary", disabled=not question.strip(), use_container_width=True):
    with st.spinner("Searching documents and generating an answer…"):
        try:
            data = ask_question(question.strip(), top_k=top_k)
        except BackendError as exc:
            st.error(str(exc))
        else:
            st.subheader("Answer")
            st.write(data["answer"])

            sources = data.get("sources", [])
            st.subheader(f"Sources ({len(sources)})")
            if not sources:
                st.info("No supporting document chunks were retrieved.")
            for source in sources:
                page = f" · page {source['page']}" if source.get("page") else ""
                label = f"{source['source']} · chunk {source['chunk_id']}{page} · score {source['score']:.4f}"
                with st.expander(label):
                    st.write(source["text"])
