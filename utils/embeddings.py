from sentence_transformers import SentenceTransformer
from langchain_core.embeddings import Embeddings


class LocalEmbeddings(Embeddings):

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        print("Loading local embedding model...")
        self.model = SentenceTransformer(model_name)
        print("Local embedding model loaded.")

    # ------------------------------------------------
    # Embed Documents
    # ------------------------------------------------

    def embed_documents(self, texts):

        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False
        )

        return embeddings.tolist()

    # ------------------------------------------------
    # Embed Query
    # ------------------------------------------------

    def embed_query(self, text):

        embedding = self.model.encode(
            text,
            normalize_embeddings=True
        )

        return embedding.tolist()


# ----------------------------------------------------
# Embedding Model
# ----------------------------------------------------

embeddings = LocalEmbeddings(
    model_name="all-MiniLM-L6-v2"
)