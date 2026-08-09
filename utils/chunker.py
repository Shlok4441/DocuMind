from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text(text):
    """
    Splits extracted text into overlapping chunks.

    Args:
        text (str): Extracted document text

    Returns:
        list: List of text chunks
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    chunks = text_splitter.split_text(text)

    return chunks