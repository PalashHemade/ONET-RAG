from pypdf import PdfReader

def parse_pdf_resume(file_path: str) -> str:
    reader = PdfReader(file_path)

    text_pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            text_pages.append(text)

    return "\n".join(text_pages)
