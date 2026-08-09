from utils.prompts import SYSTEM_PROMPT
from utils.llm import generate_answer


def answer_question(vector_store, question):
    """
    Retrieve relevant chunks and generate an answer.

    Args:
        vector_store: FAISS vector store
        question (str): User question

    Returns:
        tuple: (answer, retrieved_chunks)
    """

    docs = vector_store.similarity_search(
        question,
        k=3
    )

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    prompt = SYSTEM_PROMPT.format(
        context=context,
        question=question
    )

    answer = generate_answer(prompt)

    return answer, docs