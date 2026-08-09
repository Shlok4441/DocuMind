import streamlit as st

from utils.pdf_loader import extract_text_from_pdf
from utils.chunker import split_text
from utils.vector_store import create_vector_store
from utils.qa_chain import answer_question


# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="DocuMind AI",
    page_icon="📄",
    layout="wide"
)


# ---------------------------------------------------
# Initialize Session State
# ---------------------------------------------------
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "document_name" not in st.session_state:
    st.session_state.document_name = None

if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0


# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------
with st.sidebar:

    st.title("📂 Upload Documents")

    uploaded_files = st.file_uploader(
        "Choose PDF file(s)",
        type=["pdf"],
        accept_multiple_files=True
    )

    st.markdown("---")

    st.info("Supported Format: PDF")

    # Document information
    if st.session_state.vector_store:

        st.markdown("### 📊 Document Information")

        st.write(
            f"**Document:** "
            f"{st.session_state.document_name}"
        )

        st.write(
            f"**Chunks:** "
            f"{st.session_state.chunk_count}"
        )

        if st.button("🗑️ Clear Document"):

            st.session_state.vector_store = None
            st.session_state.document_name = None
            st.session_state.chunk_count = 0

            st.rerun()


# ---------------------------------------------------
# Main Page
# ---------------------------------------------------
st.title("📄 DocuMind AI")

st.subheader(
    "Intelligent Document Question Answering System"
)

st.write(
    """
    Upload a PDF document and ask questions about its
    contents. DocuMind AI uses semantic search and
    generative AI to find and explain relevant information.
    """
)

st.markdown("---")


# ---------------------------------------------------
# Process Uploaded Documents
# ---------------------------------------------------
if uploaded_files:

    # Currently we process the first document.
    # Multi-document retrieval will be added later.
    file = uploaded_files[0]

    # Only process if this is a new document
    if (
        st.session_state.document_name != file.name
        or st.session_state.vector_store is None
    ):

        with st.spinner("📚 Processing document..."):

            # -----------------------------------------
            # Extract Text
            # -----------------------------------------
            text = extract_text_from_pdf(file)

            if not text.strip():

                st.error(
                    "❌ No text could be extracted from this PDF."
                )

                st.stop()

            # -----------------------------------------
            # Split Text
            # -----------------------------------------
            chunks = split_text(text)

            # -----------------------------------------
            # Create FAISS Vector Store
            # -----------------------------------------
            vector_store = create_vector_store(chunks)

            # -----------------------------------------
            # Save to Session State
            # -----------------------------------------
            st.session_state.vector_store = vector_store
            st.session_state.document_name = file.name
            st.session_state.chunk_count = len(chunks)

        st.success(
            f"✅ {file.name} processed successfully!"
        )


# ---------------------------------------------------
# Document Status
# ---------------------------------------------------
if st.session_state.vector_store:

    st.markdown("### 📄 Current Document")

    st.success(
        f"**{st.session_state.document_name}** "
        f"• {st.session_state.chunk_count} chunks indexed"
    )

    st.markdown("---")

    # ------------------------------------------------
    # Question Answering
    # ------------------------------------------------
    st.header("💬 Ask Your Document")

    question = st.text_input(
        "Ask a question",
        placeholder="Example: What are the main findings?"
    )

    if st.button("🔍 Ask DocuMind"):

        if not question.strip():

            st.warning("Please enter a question.")

        else:

            with st.spinner("🤔 Searching the document..."):

                try:

                    answer, docs = answer_question(
                        st.session_state.vector_store,
                        question
                    )

                    st.markdown("### 🤖 Answer")

                    st.write(answer)

                    # --------------------------------
                    # Retrieved Sources
                    # --------------------------------
                    st.markdown("### 📚 Retrieved Sources")

                    for i, doc in enumerate(docs):

                        with st.expander(
                            f"Source {i + 1}"
                        ):

                            st.write(
                                doc.page_content
                            )

                except Exception as e:

                    st.error(
                        f"❌ Something went wrong: {e}"
                    )

else:

    st.info(
        "👈 Upload a PDF from the sidebar to get started."
    )