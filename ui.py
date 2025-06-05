import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
from app import process_file
from streamlit.web import bootstrap
script_path = os.path.abspath("ui.py")

# INPUT_DIR = 'input'
INPUT_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "input")
os.makedirs(INPUT_DIR, exist_ok=True)

st.set_page_config(page_title="AI File Classifier", layout="centered")

st.markdown("""
<style>
/* Upload button ko full width aur green color dein */
.css-1emrehy.edgvbvh3 {  /* Streamlit button class, yeh har version mein change hota hai */
    width: 100% !important;
    background-color: #4CAF50 !important;
    color: white !important;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)

st.title("AI-Based File Classifier & Renamer")
st.markdown("Upload files below. They will be saved to the `input/` folder and processed.")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
results_path = os.path.join(BASE_DIR, "results.xlsx")

# Agar results.xlsx file exist nahi karti to blank file create kar do
if not os.path.exists(results_path):
    df = pd.DataFrame(columns=[
    "File",
    "Company Name",
    "Initials",
    "First Name",
    "Year",
    "Code",
    "New Filename",
    "Warnings",
    "GPT Output",
    "Status",
    "OCR"
])

    df.to_excel(results_path, index=False)

# Ab download button show karo (file guaranteed exist karti hai)
with open(results_path, "rb") as f:
    st.download_button(
        label="Download results.xlsx",
        data=f,
        file_name="results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if "temp_results" not in st.session_state:
    st.session_state.temp_results = []

company_name = st.text_input("Company Name")
full_name = st.text_input("Full Name")
preview_only = st.checkbox("Preview only (don’t move/rename files)")

# File upload form with label hidden
with st.form("upload_form", clear_on_submit=True):
    uploaded_files = st.file_uploader("", accept_multiple_files=True, label_visibility="collapsed")
    upload_submit = st.form_submit_button("Upload Files")

if upload_submit and uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join(INPUT_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    st.success(f"{len(uploaded_files)} file(s) uploaded successfully!")

if st.button("🔄 Process Files"):
    if not company_name.strip() or not full_name.strip():
        st.error("Please fill in both Company Name and Full Name.")
    else:
        files = os.listdir(INPUT_DIR)
        if not files:
            st.warning("No files found in the input folder.")
        else:
            st.session_state.temp_results.clear()
            with st.spinner("Processing..."):
                for file in files:
                    file_path = os.path.join(INPUT_DIR, file)
                    if os.path.isfile(file_path):
                        # result = process_file(file_path, file, company_name, full_name)
                        result = process_file(file_path, file, company_name, full_name, preview_only)
                        if result:
                            st.session_state.temp_results.append(result)
            st.success("✅ All files processed!")

if st.session_state.temp_results:
    st.subheader("Current Session Results")
    for res in st.session_state.temp_results:
        st.markdown(f"""
        ---
        **Original File:** `{res['filename']}`  
        **Year:** `{res['year']}`  
        **Document Code:** `{res['code']}`  
        **Suggested Filename:** `{res['new_filename']}`  
        **Warnings:** `{res['warnings']}`
        **Status:** `{res['status']}`  
        **OCR:** `{res['ocr']}`  
        """, unsafe_allow_html=True)
