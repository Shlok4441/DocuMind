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

if "document_name" not in st.session_state:
    st.session_state.document_name = None

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
        "Upload a PDF",
        type=["pdf"],
        accept_multiple_files=False
    )

    st.markdown("---")

    if st.session_state.vector_store:

        st.markdown("### 📄 Current Document")

        st.markdown(
            f"""
            <div class="document-card">
                <strong>📄 {st.session_state.document_name}</strong>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Chunks",
                st.session_state.chunk_count
            )

        with col2:
            st.metric(
                "Status",
                "Ready"
            )

        st.markdown("---")

        if st.button(
            "🗑️ Clear Document",
            use_container_width=True
        ):

            st.session_state.vector_store = None
            st.session_state.document_name = None
            st.session_state.chunk_count = 0
            st.session_state.chat_history = []

            st.rerun()

    else:

        st.info(
            "Upload a PDF to start asking questions."
        )


# ---------------------------------------------------
# Main Header
# ---------------------------------------------------

st.title("📄 DocuMind AI")

st.caption(
    "Chat with your documents using AI-powered semantic search and RAG."
)


# ---------------------------------------------------
# Process Document
# ---------------------------------------------------

if uploaded_files:

    file = uploaded_files

    if (
        st.session_state.document_name != file.name
        or st.session_state.vector_store is None
    ):

        with st.spinner(
            "📚 Processing your document..."
        ):

            try:

                # Extract text
                text = extract_text_from_pdf(file)

                if not text.strip():

                    st.error(
                        "❌ No readable text was found in this PDF."
                    )

                    st.stop()

                # Split text
                chunks = split_text(text)

                if not chunks:

                    st.error(
                        "❌ Could not create document chunks."
                    )

                    st.stop()

                # Create FAISS vector store
                vector_store = create_vector_store(
                    chunks
                )

                # Save to session state
                st.session_state.vector_store = vector_store
                st.session_state.document_name = file.name
                st.session_state.chunk_count = len(chunks)
                st.session_state.chat_history = []

                st.success(
                    "✅ Document processed successfully!"
                )

            except Exception as e:

                st.error(
                    f"❌ Error processing document: {e}"
                )

                st.stop()


# ---------------------------------------------------
# Main Q&A Interface
# ---------------------------------------------------

if st.session_state.vector_store:

    st.markdown("---")

    st.header("💬 Ask Your Document")

    question = st.text_input(
        "Your question",
        placeholder=(
            "Example: What are the main findings "
            "of this document?"
        ),
        label_visibility="collapsed"
    )

    ask_button = st.button(
        "🔍 Ask DocuMind",
        type="primary",
        use_container_width=True
    )

    if ask_button:

        if not question.strip():

            st.warning(
                "Please enter a question first."
            )

        else:

            with st.spinner(
                "🤔 Searching the document..."
            ):

                try:

                    answer, docs = answer_question(
                        st.session_state.vector_store,
                        question
                    )

                    # Save conversation
                    st.session_state.chat_history.append(
                        {
                            "question": question,
                            "answer": answer,
                            "docs": docs
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

            st.markdown(
                f"**🧑 You:** {chat['question']}"
            )

            st.markdown(
                f"""
                <div class="answer-card">
                    <strong>🤖 DocuMind AI</strong>
                    <br><br>
                    {chat['answer']}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("#### 📚 Sources")

            for i, doc in enumerate(
                chat["docs"]
            ):

                with st.expander(
                    f"Source {i + 1}"
                ):

                    st.write(
                        doc.page_content
                    )

            st.markdown("---")


# ---------------------------------------------------
# Empty State
# ---------------------------------------------------

else:

    st.markdown("---")

    st.subheader("Get started")

    st.write(
        """
        Upload a PDF using the sidebar. Once your document is
        processed, you can ask questions and DocuMind AI will
        retrieve the most relevant information from it.
        """
    )

    st.info(
        "👈 Upload a PDF from the sidebar to begin."
    )