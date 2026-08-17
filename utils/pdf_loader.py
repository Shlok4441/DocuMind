import PyPDF2


def extract_text_from_pdf(uploaded_file):
    """
    Extract text from an uploaded PDF while preserving
    the page number.

    Returns:
        list: Each item contains page text and page number.
    """

    reader = PyPDF2.PdfReader(uploaded_file)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        page_text = page.extract_text()

        if page_text and page_text.strip():

            pages.append({
                "text": page_text.strip(),
                "page": page_number
            })

    return pages