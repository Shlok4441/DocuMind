import os
import json
import hashlib

REGISTRY_PATH = "vectorstore/document_registry.json"


# ============================================================
# Calculate PDF Hash
# ============================================================

def calculate_file_hash(file_bytes):
    """
    Calculate a unique SHA-256 hash for a PDF file.
    """

    return hashlib.sha256(
        file_bytes
    ).hexdigest()


# ============================================================
# Load Registry
# ============================================================

def load_registry():
    """
    Load the document registry from disk.
    """

    if not os.path.exists(REGISTRY_PATH):
        return {}

    try:

        with open(
            REGISTRY_PATH,
            "r"
        ) as file:

            return json.load(file)

    except Exception:

        return {}


# ============================================================
# Save Registry
# ============================================================

def save_registry(registry):
    """
    Save the document registry to disk.
    """

    os.makedirs(
        "vectorstore",
        exist_ok=True
    )

    with open(
        REGISTRY_PATH,
        "w"
    ) as file:

        json.dump(
            registry,
            file,
            indent=4
        )


# ============================================================
# Check if Document Exists
# ============================================================

def document_exists(file_hash):
    """
    Check whether a document is already registered.
    """

    registry = load_registry()

    return file_hash in registry


# ============================================================
# Register Document
# ============================================================

def register_document(
    file_hash,
    filename,
    chunks
):
    """
    Register a newly indexed document.
    """

    registry = load_registry()

    registry[file_hash] = {

        "filename": filename,

        "chunks": chunks

    }

    save_registry(
        registry
    )


# ============================================================
# Delete Document
# ============================================================

def delete_document(file_hash):
    """
    Remove a document from the registry.
    """

    registry = load_registry()

    if file_hash in registry:

        del registry[file_hash]

        save_registry(
            registry
        )

        return True

    return False


# ============================================================
# Clear All Documents
# ============================================================

def clear_registry():
    """
    Remove all registered documents.
    """

    save_registry({})


# ============================================================
# Get Registered Documents
# ============================================================

def get_registered_documents():
    """
    Return all registered documents.
    """

    return load_registry()