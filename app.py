import streamlit as st

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="DocuMind AI",
    page_icon="📄",
    layout="wide"
)

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.title("📂 Upload Documents")

    uploaded_files = st.file_uploader(
        "Choose PDF file(s)",
        type=["pdf"],
        accept_multiple_files=True
    )

    st.markdown("---")
    st.info("Supported Format: PDF")

# ----------------------------
# Main Page
# ----------------------------
st.title("📄 DocuMind AI")

st.subheader("Intelligent Document Question Answering System")

st.write(
    """
    Upload one or more PDF documents and ask questions about their contents.
    The AI will search the documents and answer based on the uploaded information.
    """
)

st.markdown("---")

# ----------------------------
# Uploaded Files
# ----------------------------
if uploaded_files:

    st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully!")

    st.subheader("Uploaded Documents")

    for file in uploaded_files:

        file_size = round(file.size / (1024 * 1024), 2)

        st.write(f"📄 **{file.name}**")
        st.write(f"Size: {file_size} MB")
        st.write("---")

else:

    st.info("Please upload one or more PDF documents.")