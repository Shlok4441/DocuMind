from dotenv import load_dotenv
from google import genai
import os

# Load environment variables
load_dotenv()

# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


def generate_embeddings(chunks):
    """
    Generate embeddings for a list of text chunks.

    Args:
        chunks (list): List of text chunks

    Returns:
        list: List of embeddings
    """

    embeddings = []

    for chunk in chunks:

        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=chunk
        )

        embeddings.append(response.embeddings[0].values)

    return embeddings