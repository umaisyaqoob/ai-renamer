# app.py
import os
import shutil
import pandas as pd
from dotenv import load_dotenv
from utils.file_parser import extract_text_from_file
from utils.gpt_handler import get_gpt_response
import re

# Load .env variables
load_dotenv()

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'
RESULTS_FILE = 'results.xlsx'
DELETE_AFTER = os.getenv("DELETE_ORIGINAL_FILE_AFTER_PROCESSING", "false").lower() == "true"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def sanitize_filename(name):
    # Replace newlines and tabs with a space
    name = name.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    # Remove or replace characters not allowed in Windows filenames
    return re.sub(r'[<>:"/\\|?*\']+', '', name).strip()

def process_file(file_path, filename, company_name, full_name):
    text = extract_text_from_file(file_path)
    if not text.strip():
        return None

    gpt_result = get_gpt_response(text, company_name, full_name)

    year = gpt_result["year"]
    document_code = gpt_result["code"]
    suggested_filename = sanitize_filename(gpt_result["filename"])
    warnings = gpt_result["warnings"]

    # Add file extension
    original_ext = os.path.splitext(filename)[1]
    final_filename = f"{suggested_filename}{original_ext}"
    dest_path = os.path.join(OUTPUT_DIR, final_filename)

    shutil.copy2(file_path, dest_path)
    if DELETE_AFTER:
        os.remove(file_path)

    # Log results
    if os.path.exists(RESULTS_FILE):
        df_log = pd.read_excel(RESULTS_FILE)
    else:
        df_log = pd.DataFrame(columns=[
            "File", "Company Name", "Initials", "First Name",
            "Year", "Code", "New Filename", "Warnings", "GPT Output"
        ])

    df_log.loc[len(df_log)] = {
        "File": filename,
        "Company Name": company_name,
        "Initials": 'W',
        "First Name": full_name,
        "Year": year,
        "Code": document_code,
        "New Filename": final_filename,
        "Warnings": warnings,
        "GPT Output": str(gpt_result)
    }
    df_log.to_excel(RESULTS_FILE, index=False)

    return {
        "filename": filename,
        "code": document_code,
        "year": year,
        "new_filename": final_filename,
        "warnings": warnings,
        "gpt_output": str(gpt_result)
    }
