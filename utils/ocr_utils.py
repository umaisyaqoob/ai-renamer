import subprocess
import tempfile
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os

def ocr_pdf_file(file_path):
    try:
        with tempfile.TemporaryDirectory() as tempdir:
            images = convert_from_path(file_path, output_folder=tempdir)
            text = ''
            for img in images:
                text += pytesseract.image_to_string(img)
            return text
    except Exception as e:
        return f"[ERROR in OCR PDF]: {e}"

def ocr_image_file(file_path):
    try:
        img = Image.open(file_path)
        return pytesseract.image_to_string(img)
    except Exception as e:
        return f"[ERROR in OCR Image]: {e}"
