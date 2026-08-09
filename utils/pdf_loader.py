from pypdf import PdfReader


def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from an uploaded PDF file.

    Args:
        uploaded_file: Streamlit UploadedFile object

    Returns:
        str: Combined text from all pages
    """

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text