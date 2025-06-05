import os
import openai
from dotenv import load_dotenv
import re
import json



load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def load_prompt():
    with open("prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

def validate_response(response: str, company_name: str, full_name: str) -> dict:
    try:
        parsed = json.loads(response)
        return {
            "year": parsed.get("year", "N_A").strip() or "N_A",
            "code": parsed.get("code", "N_A").strip() or "N_A",
            "filename": parsed.get("filename", f"N_A {company_name} - {full_name} N_A").strip() or "N_A",
            "warnings": parsed.get("warnings", "No warnings provided").strip() or "No warnings provided",
            "status": "Success"
        }
    except Exception as e:
        return {
            "year": "N_A",
            "code": "N_A",
            "filename": f"N_A {company_name} - {full_name} N_A",
            "warnings": "Response was not valid JSON",
            "status": f"JSON parse error: {e}"
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
    You must respond ONLY with a valid JSON object — no markdown, no ```json, no explanation, no extra text.

    RESPONSE FORMAT (strictly follow this structure):

    {
    "year": "<year>",
    "code": "<code>",
    "filename": "<new_filename>",
    "warnings": "<warnings>"
    }

    Guidelines:
    - All values must be strings.
    - Do NOT add any extra fields or repeat keys.
    - Do NOT wrap the JSON in triple backticks (```) or anything else.
    - If there are no warnings, use: "warnings": "None"
    - Output must be a clean, parsable JSON object — no additional text before or after.
    """



    full_prompt = header + strict_format_instruction + "\n\n" + base_prompt + "\n\n" + text

    try:
        resp = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": full_prompt}],
            temperature=0.3,
        )
        gpt_raw = resp.choices[0].message.content.strip()
        return validate_response(gpt_raw, company_name, full_name)
    except Exception as e:
        print(f"GPT Error: {e}")
        return {
            "year": "N_A",
            "code": "N_A",
            "filename": f"N_A {company_name} - {full_name} N_A",
            "warnings": f"GPT Error: {e}"
        }
