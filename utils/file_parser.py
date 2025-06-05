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
    
    try:
        if ext in ['.txt']:
            text = extract_text_from_txt(file_path)
            status = "Success" if text.strip() else "Empty file"
            return text, status, 'No'
        
        elif ext in ['.docx', '.doc']:
            text = extract_text_from_docx(file_path)
            status = "Success" if text.strip() else "Empty file"
            return text, status, 'No'
        
        elif ext in ['.pdf']:
            try:
                text = ''
                reader = PdfReader(file_path)
                for page in reader.pages:
                    text += page.extract_text() or ''
                if text.strip():
                    return text, "Success", 'No'
                else:
                    text = ocr_pdf_file(file_path)
                    if text.strip():
                        return text, "OCR used for empty PDF", 'Yes'
                    else:
                        print(f'[ERROR] Skipped: {os.path.splitext(os.path.basename(file_path))[0]}{os.path.splitext(os.path.basename(file_path))[1]} → OCR failed')
                        return "", "OCR failed on PDF", 'Yes'
            except Exception:
                text = ocr_pdf_file(file_path)
                if text.strip():
                    return text, "OCR used after PDF error", 'Yes'
                else:
                    print(f'[ERROR] Skipped: {os.path.splitext(os.path.basename(file_path))[0]}{os.path.splitext(os.path.basename(file_path))[1]} → OCR failed')
                    return "", "OCR failed on PDF error", 'Yes'
        
        elif ext in ['.jpeg', '.jpg', '.png', '.tiff']:
            text = ocr_image_file(file_path)
            if text.strip():
                return text, "Success", 'Yes'
            else:
                print(f'[ERROR] Skipped: {os.path.splitext(os.path.basename(file_path))[0]}{os.path.splitext(os.path.basename(file_path))[1]} → OCR failed')
                return "", "OCR failed on image", 'Yes'

        else:
            text = ocr_image_file(file_path)
            if text.strip():
                return text, "Unknown format, OCR used", 'Yes'
            else:
                print(f'[ERROR] Skipped: {os.path.splitext(os.path.basename(file_path))[0]}{os.path.splitext(os.path.basename(file_path))[1]} → OCR failed')
                return "", "OCR failed on unknown format", 'Yes'
    
    except Exception as e:
        return "", f"Extraction error: {e}", 'No'
