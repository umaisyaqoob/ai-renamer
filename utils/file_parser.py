import os
import mimetypes
from PyPDF2 import PdfReader
import docx
from .ocr_utils import ocr_image_file, ocr_pdf_file

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return '\n'.join([p.text for p in doc.paragraphs])

def extract_text_from_pdf(file_path):
    text = ''
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ''
        if text.strip():
            return text
        else:
            return ocr_pdf_file(file_path)
    except Exception:
        return ocr_pdf_file(file_path)

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext in ['.txt']:
        return extract_text_from_txt(file_path)
    elif ext in ['.docx', '.doc']:
        return extract_text_from_docx(file_path)
    elif ext in ['.pdf']:
        return extract_text_from_pdf(file_path)
    elif ext in ['.jpeg', '.jpg', '.png', '.tiff']:
        return ocr_image_file(file_path)
    else:
        # Try OCR as fallback
        return ocr_image_file(file_path)
