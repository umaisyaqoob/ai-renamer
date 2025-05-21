import os
import openai
from dotenv import load_dotenv
import re


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def load_prompt():
    with open("prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

def validate_response(response: str, company_name: str, full_name: str) -> dict:
    """
    Parses GPT response and returns structured values.
    Expected format: YEAR:<year>,CODE:<code>,New Filename:<filename>,WARNINGS:<warnings>
    """
    match = re.match(r"YEAR:(.*?),CODE:(.*?),New Filename:(.*?),WARNINGS:(.*)", response)
    if match:
        year, code, filename, warnings = match.groups()
        year_p = year.strip() or "N_A"
        code_p = code.strip() or "N_A"
        return {
            "year": year_p,
            "code": code_p,
            "filename": filename.strip() if filename.strip() != "N_A" else f"{code_p} {company_name} - {full_name} {year_p}",
            "warnings": warnings.strip() or "No warnings provided"
        }
    
    # If not matched at all
    return {
        "year": "N_A",
        "code": "N_A",
        "filename": f"N_A {company_name} - {full_name} N_A",
        "warnings": "Response format invalid or missing expected fields"
    }


def get_gpt_response(text: str, company_name: str, full_name: str) -> dict:
    """
    Sends the combined prompt to GPT-4o and returns parsed structured response.
    """
    base_prompt = load_prompt()
    
    header = (
        f"COMPANY_NAME → {company_name}\n"
        f"FULL_NAME    → {full_name}\n\n"
    )
    
    strict_format_instruction = """
    RESPONSE FORMAT (strictly follow this structure without any explanation):
    YEAR:<year>,CODE:<code>,New Filename:<new_filename>,WARNINGS:<warnings>

    - WARNINGS should reflect any inconsistencies, unusual patterns, missing values, conflicting data, or anything worth notifying the user.
    - If everything is fine, simply write: WARNINGS:None
    - Do NOT explain anything outside the strict format.

    EXAMPLE:
    YEAR:2024,CODE:E7,New Filename:E7 Test Company - W Verheul Voorlopige Aanslag ZVW 2024.pdf,WARNINGS:Document refers to 2023 values but mentions 2024 in title
    """


    full_prompt = header + strict_format_instruction + "\n\n" + base_prompt + "\n\n" + text

    try:
        resp = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": full_prompt}],
            temperature=0.3,
        )
        gpt_raw = resp.choices[0].message.content.strip()
        print(gpt_raw)
        return validate_response(gpt_raw, company_name, full_name)
    except Exception as e:
        print(f"GPT Error: {e}")
        return {
            "year": "N_A",
            "code": "N_A",
            "filename": f"N_A {company_name} - {full_name} N_A",
            "warnings": f"GPT Error: {e}"
        }
