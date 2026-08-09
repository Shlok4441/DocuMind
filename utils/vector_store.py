from dotenv import load_dotenv
import os

from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)


def create_vector_store(chunks):
    """
    Creates a FAISS vector store from text chunks.

    Args:
        chunks (list): List of text chunks

    Returns:
        FAISS vector store
    """

    vector_store = FAISS.from_texts(
        texts=chunks,
        embedding=embeddings
    )

    return vector_store