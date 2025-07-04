import pdfplumber
import pytesseract
import docx2txt
from PIL import Image
from docx import Document
import textract  # for handling .doc (older MS Word)

def extract_text(filepath: str) -> str:
    ext = filepath.lower().split('.')[-1]

    if ext == "pdf":
        text = ""
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    if ext in ("png", "jpg", "jpeg", "tiff"):
        return pytesseract.image_to_string(Image.open(filepath))

    if ext == "docx":
        try:
            return docx2txt.process(filepath)
        except:
            doc = Document(filepath)
            return "\n".join(p.text for p in doc.paragraphs)

    if ext == "doc":
        try:
            return textract.process(filepath).decode("utf-8")
        except Exception as e:
            raise ValueError(f"Failed to extract text from .doc file: {str(e)}")

    raise ValueError(f"Unsupported file type: {ext}")
