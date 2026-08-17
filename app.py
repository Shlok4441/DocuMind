import streamlit as st

from utils.pdf_loader import extract_text_from_pdf
from utils.chunker import split_text

from utils.vector_store import (
    load_vector_store,
    create_vector_store,
    add_documents_to_vector_store,
    save_vector_store
)

from utils.document_registry import (
    calculate_file_hash,
    document_exists,
    register_document,
    get_registered_documents
)

from utils.qa_chain import answer_question

from langchain_core.documents import Document


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="📄",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "vector_store" not in st.session_state:
    st.session_state.vector_store = load_vector_store()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("📂 Documents")

    st.markdown("### Upload PDF documents")

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

    # --------------------------------------------------------
    # Current Documents
    # --------------------------------------------------------

    registry = get_registered_documents()

    if registry:

        st.markdown("### 📄 Current Documents")

        for item in registry.values():

            st.caption(
                f"📄 {item.get('filename', 'Unknown')}"
            )

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    total_documents = len(registry)

    total_chunks = sum(
        item.get("chunks", 0)
        for item in registry.values()
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Documents",
            total_documents
        )

    with col2:

        st.metric(
            "Chunks",
            total_chunks
        )


# ============================================================
# MAIN PAGE
# ============================================================

st.title("📄 DocuMind AI")

st.write(
    "Chat with your documents using "
    "AI-powered semantic search and RAG."
)


# ============================================================
# PROCESS UPLOADED DOCUMENTS
# ============================================================

if uploaded_files:

    new_documents = []

    documents_to_register = []

    skipped_documents = []

    processed_documents = []

    # --------------------------------------------------------
    # Process files
    # --------------------------------------------------------

    with st.spinner("Processing new documents..."):

        for uploaded_file in uploaded_files:

            try:

                # ------------------------------------------------
                # Read PDF bytes
                # ------------------------------------------------

                file_bytes = uploaded_file.getvalue()

                # ------------------------------------------------
                # Calculate unique document hash
                # ------------------------------------------------

                file_hash = calculate_file_hash(
                    file_bytes
                )

                # ------------------------------------------------
                # Check whether already indexed
                # ------------------------------------------------

                if document_exists(file_hash):

                    skipped_documents.append(
                        uploaded_file.name
                    )

                    continue

                # ------------------------------------------------
                # Extract text WITH page information
                # ------------------------------------------------

                pages = extract_text_from_pdf(
                    uploaded_file
                )

                if not pages:

                    st.warning(
                        f"⚠️ Could not extract text "
                        f"from {uploaded_file.name}."
                    )

                    continue

                # ------------------------------------------------
                # Split into chunks WITH page information
                # ------------------------------------------------

                chunks = split_text(
                    pages
                )

                if not chunks:

                    st.warning(
                        f"⚠️ No chunks created for "
                        f"{uploaded_file.name}."
                    )

                    continue

                # ------------------------------------------------
                # Convert chunks to LangChain Documents
                # ------------------------------------------------

                documents = []

                for index, chunk in enumerate(chunks):

                    documents.append(

                        Document(

                            page_content=chunk["text"],

                            metadata={

                                "source":
                                    uploaded_file.name,

                                "page":
                                    chunk["page"],

                                "chunk":
                                    index + 1,

                                "file_hash":
                                    file_hash

                            }

                        )

                    )

                # ------------------------------------------------
                # Add documents to processing list
                # ------------------------------------------------

                new_documents.extend(
                    documents
                )

                # ------------------------------------------------
                # Prepare registry information
                # ------------------------------------------------

                documents_to_register.append({

                    "hash":
                        file_hash,

                    "filename":
                        uploaded_file.name,

                    "chunks":
                        len(documents)

                })

                processed_documents.append(
                    uploaded_file.name
                )

            except Exception as e:

                st.error(
                    f"❌ Error reading "
                    f"{uploaded_file.name}: {e}"
                )


    # ========================================================
    # CREATE / UPDATE VECTOR STORE
    # ========================================================

    if new_documents:

        try:

            with st.spinner(
                "Creating vector embeddings..."
            ):

                # ------------------------------------------------
                # Existing FAISS store
                # ------------------------------------------------

                if (
                    st.session_state.vector_store
                    is not None
                ):

                    st.session_state.vector_store = (
                        add_documents_to_vector_store(
                            st.session_state.vector_store,
                            new_documents
                        )
                    )

                # ------------------------------------------------
                # First vector store
                # ------------------------------------------------

                else:

                    st.session_state.vector_store = (
                        create_vector_store(
                            new_documents
                        )
                    )

                # ------------------------------------------------
                # Save FAISS
                # ------------------------------------------------

                save_vector_store(
                    st.session_state.vector_store
                )


            # ====================================================
            # REGISTER DOCUMENTS
            # ====================================================

            for item in documents_to_register:

                register_document(

                    item["hash"],

                    item["filename"],

                    item["chunks"]

                )


            st.success(
                f"✅ {len(processed_documents)} "
                f"document(s) processed successfully!"
            )

            st.success(
                f"📚 {len(new_documents)} "
                f"chunks indexed."
            )

        except Exception as e:

            st.error(
                f"❌ Error processing documents: {e}"
            )


    # ========================================================
    # DUPLICATE DOCUMENT MESSAGE
    # ========================================================

    if skipped_documents:

        for filename in skipped_documents:

            st.info(
                f"ℹ️ **{filename}** is already indexed. "
                f"Skipped embedding."
            )


# ============================================================
# REFRESH REGISTRY / STATISTICS
# ============================================================

registry = get_registered_documents()

total_documents = len(registry)

total_chunks = sum(
    item.get("chunks", 0)
    for item in registry.values()
)


# ============================================================
# STATUS
# ============================================================

if total_documents > 0:

    st.success(
        f"📚 {total_documents} document(s) indexed "
        f"• {total_chunks} chunks"
    )


# ============================================================
# CHAT SECTION
# ============================================================

st.markdown("---")

st.header("💬 Chat with Your Documents")


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.chat_history:

    if message["role"] == "user":

        st.markdown(
            f"**👤 You:** {message['content']}"
        )

    else:

        st.markdown(
            f"**🤖 DocuMind:** {message['content']}"
        )

        # ------------------------------------------------
        # Sources
        # ------------------------------------------------

        if message.get("sources"):

            st.markdown("### 📚 Sources")

            for source in message["sources"]:

                filename = source.metadata.get(
                    "source",
                    "Unknown document"
                )

                page = source.metadata.get(
                    "page",
                    "Unknown"
                )

                chunk = source.metadata.get(
                    "chunk",
                    "Unknown"
                )

                with st.expander(
                    f"📄 {filename} "
                    f"• Page {page} "
                    f"• Chunk {chunk}"
                ):

                    st.write(
                        source.page_content
                    )


# ============================================================
# QUESTION INPUT
# ============================================================

question = st.chat_input(
    "Ask a question about your documents..."
)


# ============================================================
# HANDLE QUESTION
# ============================================================

if question:

    # --------------------------------------------------------
    # Check vector store
    # --------------------------------------------------------

    if st.session_state.vector_store is None:

        st.warning(
            "⚠️ Please upload a PDF document "
            "before asking questions."
        )

        st.stop()


    # --------------------------------------------------------
    # Display user question
    # --------------------------------------------------------

    st.session_state.chat_history.append({

        "role":
            "user",

        "content":
            question

    })


    # --------------------------------------------------------
    # Generate answer
    # --------------------------------------------------------

    with st.spinner(
        "🔎 Searching your documents..."
    ):

        try:

            answer, docs, search_query = (
                answer_question(

                    st.session_state.vector_store,

                    question,

                    st.session_state.chat_history[:-1]

                )
            )


            # ------------------------------------------------
            # Save assistant response
            # ------------------------------------------------

            st.session_state.chat_history.append({

                "role":
                    "assistant",

                "content":
                    answer,

                "sources":
                    docs,

                "search_query":
                    search_query

            })


            # ------------------------------------------------
            # Rerun to display clean chat
            # ------------------------------------------------

            st.rerun()


        except Exception as e:

            st.error(
                f"❌ Unable to answer question: {e}"
            )