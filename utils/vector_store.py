import os

from langchain_community.vectorstores import FAISS

from utils.embeddings import embeddings


# ---------------------------------------------------
# Create Vector Store
# ---------------------------------------------------

def create_vector_store(documents):
    """
    Creates a FAISS vector store from documents
    using local embeddings.
    """

    if not documents:
        return None

    vector_store = FAISS.from_documents(
        documents=documents,
        embedding=embeddings
    )

    return vector_store


# ---------------------------------------------------
# Add Documents to Existing Vector Store
# ---------------------------------------------------

def add_documents_to_vector_store(
    vector_store,
    documents
):
    """
    Adds new document chunks to an existing
    FAISS vector store.
    """

    if not documents:
        return vector_store

    vector_store.add_documents(
        documents
    )

    return vector_store


# ---------------------------------------------------
# Save Vector Store
# ---------------------------------------------------

def save_vector_store(
    vector_store,
    path="vectorstore"
):

    os.makedirs(
        path,
        exist_ok=True
    )

    vector_store.save_local(
        path
    )


# ---------------------------------------------------
# Load Vector Store
# ---------------------------------------------------

def load_vector_store(
    path="vectorstore"
):

    if not os.path.exists(path):
        return None

    try:

        vector_store = FAISS.load_local(
            path,
            embeddings,
            allow_dangerous_deserialization=True
        )

        return vector_store

    except Exception as e:

        print(
            f"Could not load vector store: {e}"
        )

        return None