from utils.prompts import SYSTEM_PROMPT
from utils.llm import generate_answer


def answer_question(vector_store, question):
    """
    Retrieve relevant document chunks and generate
    an answer using Gemini.
    """

    docs = vector_store.similarity_search(
        question,
        k=4
    )

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

    context = "\n\n".join(context_parts)

    prompt = SYSTEM_PROMPT.format(
        context=context,
        question=question
    )

    answer = generate_answer(prompt)

    return answer, docs