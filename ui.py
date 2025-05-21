# ui.py
import streamlit as st
import os
from app import process_file

INPUT_DIR = 'input'
os.makedirs(INPUT_DIR, exist_ok=True)

st.set_page_config(page_title="AI File Classifier", layout="centered")
st.title("AI-Based File Classifier & Renamer")
st.markdown("Upload files to the `input/` folder and click **Process Files**.")

# Session state for results
if "temp_results" not in st.session_state:
    st.session_state.temp_results = []

# Input fields
company_name = st.text_input("Company Name")
full_name = st.text_input("Full Name")

# Process files
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
                        result = process_file(file_path, file, company_name, full_name)
                        if result:
                            st.session_state.temp_results.append(result)
            st.success("✅ All files processed!")

# Display results
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
        """, unsafe_allow_html=True)
