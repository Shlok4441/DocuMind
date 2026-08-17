from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text(
    pages,
    chunk_size=1000,
    chunk_overlap=150
):
    """
    Split PDF pages into chunks while preserving
    page information.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = []

    for page in pages:

        page_text = page["text"]
        page_number = page["page"]

        page_chunks = splitter.split_text(
            page_text
        )

        for chunk in page_chunks:

            chunks.append({
                "text": chunk,
                "page": page_number
            })

    return chunks