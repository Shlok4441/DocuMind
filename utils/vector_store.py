from dotenv import load_dotenv
import os

from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()


# ---------------------------------------------------
# Google Embedding Model
# ---------------------------------------------------

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)


# ---------------------------------------------------
# Create Vector Store
# ---------------------------------------------------

def create_vector_store(documents):
    """
    Creates a FAISS vector store from LangChain documents.

    Each document contains:
    - page_content
    - metadata

    Metadata allows us to identify the source PDF later.
    """

    vector_store = FAISS.from_documents(
        documents=documents,
        embedding=embeddings
    )

    return vector_store