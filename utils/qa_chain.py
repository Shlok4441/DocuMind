import re

from utils.prompts import SYSTEM_PROMPT
from utils.llm import generate_answer
from utils.query_rewriter import rewrite_query


def extract_filename(question):
    """
    Detect a PDF filename mentioned in the user's question.
    Example:
        'According to 1706.03762v7.pdf, what problem...'
    """

    match = re.search(
        r'[\w.\-]+\.pdf',
        question,
        re.IGNORECASE
    )

    if match:
        return match.group(0)

    return None


def answer_question(
    vector_store,
    question,
    chat_history=None
):
    """
    Retrieve relevant document chunks and generate
    a source-grounded answer using Gemini.

    If the user specifies a PDF filename, retrieval
    is prioritized toward that document.
    """

    # ------------------------------------------------
    # Initialize chat history
    # ------------------------------------------------

    if chat_history is None:
        chat_history = []


    # ------------------------------------------------
    # Detect requested document
    # ------------------------------------------------

    target_filename = extract_filename(question)


    # ------------------------------------------------
    # Remove filename from semantic search question
    # ------------------------------------------------

    semantic_question = question

    if target_filename:
        semantic_question = re.sub(
            re.escape(target_filename),
            "",
            semantic_question,
            flags=re.IGNORECASE
        )


    # ------------------------------------------------
    # Rewrite query
    # ------------------------------------------------

    search_query = rewrite_query(
        semantic_question,
        chat_history
    )


    # ------------------------------------------------
    # Search FAISS
    # ------------------------------------------------

    # Retrieve more candidates initially.
    # This gives us enough candidates to prioritize
    # the requested PDF.

    docs = vector_store.similarity_search(
        search_query,
        k=20
    )


    # ------------------------------------------------
    # Prioritize requested document
    # ------------------------------------------------

    if target_filename:

        target_docs = []
        other_docs = []

        for doc in docs:

            source = str(
                doc.metadata.get(
                    "source",
                    ""
                )
            )

            source_name = source.split("/")[-1]

            if source_name.lower() == target_filename.lower():

                target_docs.append(doc)

            else:

                other_docs.append(doc)


        # If matching document chunks were found,
        # use them first.

        if target_docs:

            docs = target_docs[:6]

        else:

            # Fall back to normal semantic retrieval
            docs = docs[:6]

    else:

        docs = docs[:6]


    # ------------------------------------------------
    # Build context
    # ------------------------------------------------

    context_parts = []


    for i, doc in enumerate(
        docs,
        start=1
    ):

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
SOURCE [{i}]
Document: {source}
Page: {page}

{doc.page_content}
"""
        )


    context = "\n\n".join(
        context_parts
    )


    # ------------------------------------------------
    # Build RAG prompt
    # ------------------------------------------------

    prompt = SYSTEM_PROMPT.format(
        context=context,
        question=question
    )


    # ------------------------------------------------
    # Generate answer
    # ------------------------------------------------

    answer = generate_answer(
        prompt
    )


    # ------------------------------------------------
    # Return
    # ------------------------------------------------

    return (
        answer,
        docs,
        search_query
    )