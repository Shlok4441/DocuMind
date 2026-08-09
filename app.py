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

# ---------------------------------------------------
# Main Page
# ---------------------------------------------------
st.title("📄 DocuMind AI")

st.subheader("Intelligent Document Question Answering System")

st.write(
    """
    Upload one or more PDF documents and ask questions about their contents.
    The AI will search the uploaded documents and answer based on their content.
    """
)

st.markdown("---")

# ---------------------------------------------------
# Process Uploaded Files
# ---------------------------------------------------
if uploaded_files:

    st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully!")

    for file in uploaded_files:

        # -----------------------------------------
        # File Information
        # -----------------------------------------
        st.subheader(f"📄 {file.name}")

        file_size = round(file.size / (1024 * 1024), 2)

        st.write(f"**Size:** {file_size} MB")

        st.markdown("---")

        # -----------------------------------------
        # Extract Text
        # -----------------------------------------
        text = extract_text_from_pdf(file)

        st.markdown("## 📄 Extracted Text")

        st.text_area(
            label="",
            value=text,
            height=250,
            key=f"text_{file.name}"
        )

        # -----------------------------------------
        # Chunk Text
        # -----------------------------------------
        chunks = split_text(text)

        st.markdown("## ✂️ Document Chunks")

        st.write(f"**Total Chunks:** {len(chunks)}")

        for i, chunk in enumerate(chunks):

            with st.expander(f"Chunk {i+1}"):

                st.write(chunk)
        

        # -----------------------------------------
        # Create Vector Store
        # -----------------------------------------
        vector_store = create_vector_store(chunks)

        st.success("✅ Vector database created successfully!")

        st.write(f"Indexed **{len(chunks)}** chunks.")

        # Store vector store for future use
        st.session_state["vector_store"] = vector_store

        st.markdown("---")

    st.markdown("---")
st.header("💬 Ask Questions")

question = st.text_input(
    "Ask something about the uploaded document",
    placeholder="Example: What is Machine Learning?"
)

if question:

    with st.spinner("Searching document..."):

        answer, docs = answer_question(
            vector_store,
            question
        )

    st.success("Answer")

    st.write(answer)

    st.markdown("### Retrieved Context")

    for i, doc in enumerate(docs):

        with st.expander(f"Chunk {i+1}"):

            st.write(doc.page_content)

else:

    st.info("👈 Upload one or more PDF documents to get started.")
