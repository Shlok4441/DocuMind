import streamlit as st

from utils.pdf_loader import extract_documents_from_pdf
from utils.chunker import split_documents
from utils.vector_store import create_vector_store
from utils.qa_chain import answer_question


# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------
# Load Custom CSS
# ---------------------------------------------------

def load_css():

    try:

        with open("css/style.css") as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )

    except FileNotFoundError:

        pass


load_css()


# ---------------------------------------------------
# Session State
# ---------------------------------------------------

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "document_names" not in st.session_state:
    st.session_state.document_names = []

if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

with st.sidebar:

    st.title("📂 Documents")

    uploaded_files = st.file_uploader(
        "Upload PDF documents",
        type=["pdf"],
        accept_multiple_files=True
    )

    st.markdown("---")

    st.info(
        "Upload one or more PDF documents "
        "to start asking questions."
    )

    # -----------------------------------------------
    # Current Documents
    # -----------------------------------------------

    if st.session_state.vector_store:

        st.markdown("### 📄 Current Documents")

        for document_name in st.session_state.document_names:

            st.markdown(
                f"📄 `{document_name}`"
            )

        st.markdown("---")

        # -------------------------------------------
        # Document Statistics
        # -------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Documents",
                len(st.session_state.document_names)
            )

        with col2:

            st.metric(
                "Chunks",
                st.session_state.chunk_count
            )

        st.markdown("---")

        # -------------------------------------------
        # Clear Documents
        # -------------------------------------------

        if st.button(
            "🗑️ Clear Documents",
            use_container_width=True
        ):

            st.session_state.vector_store = None
            st.session_state.document_names = []
            st.session_state.chunk_count = 0
            st.session_state.chat_history = []

            st.rerun()


# ---------------------------------------------------
# Main Header
# ---------------------------------------------------

st.title("📄 DocuMind AI")

st.caption(
    "Chat with your documents using AI-powered "
    "semantic search and RAG."
)

st.markdown("---")


# ---------------------------------------------------
# Process Uploaded Documents
# ---------------------------------------------------

if uploaded_files:

    # Get filenames of currently uploaded documents

    current_document_names = [
        file.name
        for file in uploaded_files
    ]

    # -----------------------------------------------
    # Check whether documents need processing
    # -----------------------------------------------

    if (
        current_document_names
        != st.session_state.document_names
        or st.session_state.vector_store is None
    ):

        with st.spinner(
            "📚 Processing your documents..."
        ):

            try:

                # -----------------------------------
                # Extract Documents
                # -----------------------------------

                all_documents = []

                for file in uploaded_files:

                    documents = extract_documents_from_pdf(
                        file
                    )

                    all_documents.extend(
                        documents
                    )

                # -----------------------------------
                # Check Extracted Documents
                # -----------------------------------

                if not all_documents:

                    st.error(
                        "❌ No readable text was found "
                        "in the uploaded PDFs."
                    )

                    st.stop()

                # -----------------------------------
                # Split Documents into Chunks
                # -----------------------------------

                chunks = split_documents(
                    all_documents
                )

                if not chunks:

                    st.error(
                        "❌ Could not create document chunks."
                    )

                    st.stop()

                # -----------------------------------
                # Create Combined FAISS Vector Store
                # -----------------------------------

                vector_store = create_vector_store(
                    chunks
                )

                # -----------------------------------
                # Save to Session State
                # -----------------------------------

                st.session_state.vector_store = (
                    vector_store
                )

                st.session_state.document_names = (
                    current_document_names
                )

                st.session_state.chunk_count = (
                    len(chunks)
                )

                st.session_state.chat_history = []

                st.success(
                    f"✅ {len(uploaded_files)} "
                    "document(s) processed successfully!"
                )

            except Exception as e:

                st.error(
                    f"❌ Error processing documents: {e}"
                )

                st.stop()


# ---------------------------------------------------
# Document Status
# ---------------------------------------------------

if st.session_state.vector_store:

    st.success(
        f"📚 {len(st.session_state.document_names)} "
        f"document(s) indexed • "
        f"{st.session_state.chunk_count} chunks"
    )

    st.markdown("---")

    # ------------------------------------------------
    # Question Answering
    # ------------------------------------------------

    st.header("💬 Ask Your Documents")

    question = st.text_input(
        "Your question",
        placeholder=(
            "Example: What are the main findings "
            "of these documents?"
        ),
        label_visibility="collapsed"
    )

    ask_button = st.button(
        "🔍 Ask DocuMind",
        type="primary",
        use_container_width=True
    )

    # ------------------------------------------------
    # Process Question
    # ------------------------------------------------

    if ask_button:

        if not question.strip():

            st.warning(
                "Please enter a question first."
            )

        else:

            with st.spinner(
                "🤔 Searching your documents..."
            ):

                try:

                    answer, docs, search_query = (
                        answer_question(
                            st.session_state.vector_store,
                            question,
                            st.session_state.chat_history
                        )
                    )

                    # --------------------------------
                    # Save Conversation
                    # --------------------------------

                    st.session_state.chat_history.append(
                        {
                            "question": question,
                            "answer": answer,
                            "docs": docs,
                            "search_query": search_query
                        }
                    )

                except Exception as e:

                    st.error(
                        f"❌ Unable to answer question: {e}"
                    )


    # ------------------------------------------------
    # Conversation History
    # ------------------------------------------------

    if st.session_state.chat_history:

        st.markdown("---")

        st.header("💬 Conversation")

        for chat in reversed(
            st.session_state.chat_history
        ):

            # ----------------------------------------
            # User Question
            # ----------------------------------------

            st.markdown(
                f"**🧑 You:** {chat['question']}"
            )

            # ----------------------------------------
            # AI Answer
            # ----------------------------------------

            st.markdown(
                "#### 🤖 DocuMind AI"
            )

            st.write(
                chat["answer"]
            )

            # ----------------------------------------
            # Retrieval Query
            # ----------------------------------------

            with st.expander(
                "🔍 Retrieval Query"
            ):

                st.write(
                    chat.get(
                        "search_query",
                        chat["question"]
                    )
                )

            # ----------------------------------------
            # Sources
            # ----------------------------------------

            st.markdown(
                "#### 📚 Sources"
            )

            for i, doc in enumerate(
                chat["docs"]
            ):

                source = doc.metadata.get(
                    "source",
                    "Unknown document"
                )

                page = doc.metadata.get(
                    "page",
                    "Unknown"
                )

                with st.expander(
                    f"📄 {source} — Page {page}"
                ):

                    st.write(
                        doc.page_content
                    )

            st.markdown("---")


# ---------------------------------------------------
# Empty State
# ---------------------------------------------------

else:

    st.subheader("Get started")

    st.write(
        """
        Upload one or more PDF documents using the
        sidebar. DocuMind AI will process the documents,
        create a searchable knowledge base, and allow
        you to ask questions about their contents.
        """
    )

    st.info(
        "👈 Upload PDF documents from the sidebar "
        "to begin."
    )