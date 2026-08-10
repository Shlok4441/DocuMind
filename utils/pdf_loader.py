from pypdf import PdfReader
from langchain_core.documents import Document


def extract_documents_from_pdf(uploaded_file):
    """
    Extract text from each PDF page and preserve
    document/page metadata.

    Returns:
        list[Document]
    """

    reader = PdfReader(uploaded_file)

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):

        page_text = page.extract_text()

        if page_text and page_text.strip():

            document = Document(
                page_content=page_text,
                metadata={
                    "source": uploaded_file.name,
                    "page": page_number
                }
            )

            documents.append(document)

    return documents