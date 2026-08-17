import os
import shutil

from langchain_community.vectorstores import FAISS

from utils.embeddings import embeddings


# ============================================================
# Create Vector Store
# ============================================================

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


# ============================================================
# Add Documents to Existing Vector Store
# ============================================================

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


# ============================================================
# Save Vector Store
# ============================================================

def save_vector_store(
    vector_store,
    path="vectorstore"
):
    """
    Save FAISS vector store locally.
    """

    if vector_store is None:
        return

    os.makedirs(
        path,
        exist_ok=True
    )

    vector_store.save_local(
        path
    )


# ============================================================
# Load Vector Store
# ============================================================

def load_vector_store(
    path="vectorstore"
):
    """
    Load an existing FAISS vector store.
    """

    if not os.path.exists(path):
        return None

    # Check whether FAISS files actually exist
    index_file = os.path.join(
        path,
        "index.faiss"
    )

    store_file = os.path.join(
        path,
        "index.pkl"
    )

    if not os.path.exists(index_file) or not os.path.exists(store_file):
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


# ============================================================
# Delete Document From Vector Store
# ============================================================

def delete_document_from_vector_store(
    vector_store,
    file_hash
):
    """
    Removes all chunks belonging to a specific
    document from the FAISS vector store.

    Returns:
        Updated vector store
        or None if no documents remain.
    """

    if vector_store is None:
        return None

    ids_to_delete = []

    # --------------------------------------------------------
    # Find FAISS document IDs belonging to this file
    # --------------------------------------------------------

    for doc_id, document in vector_store.docstore._dict.items():

        if document.metadata.get("file_hash") == file_hash:

            ids_to_delete.append(
                doc_id
            )

    # --------------------------------------------------------
    # Nothing found
    # --------------------------------------------------------

    if not ids_to_delete:

        print(
            f"No chunks found for document hash: {file_hash}"
        )

        return vector_store

    # --------------------------------------------------------
    # Delete chunks
    # --------------------------------------------------------

    vector_store.delete(
        ids=ids_to_delete
    )

    # --------------------------------------------------------
    # Check if vector store is now empty
    # --------------------------------------------------------

    if len(vector_store.index_to_docstore_id) == 0:

        return None

    return vector_store


# ============================================================
# Delete Entire Vector Store
# ============================================================

def delete_entire_vector_store(
    path="vectorstore"
):
    """
    Completely removes the local FAISS vector store.
    """

    if os.path.exists(path):

        shutil.rmtree(
            path
        )