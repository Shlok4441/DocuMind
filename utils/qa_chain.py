from utils.prompts import SYSTEM_PROMPT
from utils.llm import generate_answer
from utils.query_rewriter import rewrite_query


def answer_question(
    vector_store,
    question,
    chat_history=None
):
    """
    Retrieves relevant document chunks and generates
    an answer using Gemini.

    Supports conversation-aware question rewriting.
    """

    if chat_history is None:
        chat_history = []

    # -----------------------------------------------
    # Rewrite question using conversation history
    # -----------------------------------------------

    search_query = rewrite_query(
        question,
        chat_history
    )

    # -----------------------------------------------
    # Search FAISS
    # -----------------------------------------------

    docs = vector_store.similarity_search(
        search_query,
        k=4
    )

    # -----------------------------------------------
    # Build Context
    # -----------------------------------------------

    context_parts = []

    for doc in docs:

        source = doc.metadata.get(
            "source",
            "Unknown document"
        )

        page = doc.metadata.get(
            "page",
            "Unknown"
        )

        context_parts.append(
            f"""
Source: {source}
Page: {page}

{doc.page_content}
"""
        )

    context = "\n\n".join(
        context_parts
    )

    # -----------------------------------------------
    # Generate Final Answer
    # -----------------------------------------------

    prompt = SYSTEM_PROMPT.format(
        context=context,
        question=question
    )

    answer = generate_answer(prompt)

    return answer, docs, search_query