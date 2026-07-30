import os
from pypdf import PdfReader
from docx import Document


def extract_text_from_pdf(pdf_path):
    """
    Extracts all text from a PDF file.
    """
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def extract_text_from_docx(docx_path):
    """
    Extracts all text from a Word (.docx) file.
    """
    document = Document(docx_path)
    text = "\n".join(paragraph.text for paragraph in document.paragraphs if paragraph.text)
    return text


def extract_text_from_txt(txt_path):
    """
    Extracts all text from a plain text (.txt) file.
    """
    with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def extract_text_from_file(file_path):
    """
    Detects the file type by extension and extracts text accordingly.
    Supports .pdf, .docx, and .txt files.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".txt":
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(
            f"Unsupported file type: '{ext}'. Supported formats are .pdf, .docx, and .txt"
        )