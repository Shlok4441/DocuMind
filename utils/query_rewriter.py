from utils.llm import generate_answer


def rewrite_query(question, chat_history):
    """
    Rewrites a follow-up question into a standalone
    question using previous conversation context.
    """

    if not chat_history:
        return question

    conversation = ""

    # Use the most recent conversations
    recent_history = chat_history[-5:]

    for chat in recent_history:

        conversation += (
            f"User: {chat['question']}\n"
            f"Assistant: {chat['answer']}\n\n"
        )

    prompt = f"""
You are a query rewriting assistant for a document
question-answering system.

Your task is to rewrite the user's latest question into
a standalone question that can be understood without
the previous conversation.

Rules:

1. Preserve the original meaning.
2. Resolve pronouns such as "it", "they", "this", "that",
   and "their" using the conversation.
3. Do not answer the question.
4. Do not add information that is not present in the
   conversation.
5. If the question is already standalone, return it
   unchanged.
6. Return ONLY the rewritten question.

Conversation:

{conversation}

Latest question:

{question}

Standalone question:
"""

    rewritten_question = generate_answer(prompt)

    return rewritten_question.strip()