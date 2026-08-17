import os
import json
import hashlib


REGISTRY_PATH = "vectorstore/document_registry.json"


# ============================================================
# Calculate PDF Hash
# ============================================================

def calculate_file_hash(file_bytes):

    return hashlib.sha256(
        file_bytes
    ).hexdigest()


# ============================================================
# Load Registry
# ============================================================

def load_registry():

    if not os.path.exists(
        REGISTRY_PATH
    ):

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

    registry = load_registry()


    registry[file_hash] = {

        "filename": filename,

        "chunks": chunks

    }


    save_registry(
        registry
    )


# ============================================================
# Get Registered Documents
# ============================================================

def get_registered_documents():

    registry = load_registry()

    return registry