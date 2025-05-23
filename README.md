# 📄 GPT-4o Document Metadata Extractor

This project uses OpenAI's GPT-4o to process document text and extract structured metadata like year, code, generated filename, and any warnings based on document content and formatting rules.

---

## 🔍 Purpose

The purpose of this project is to automate the extraction and validation of key information from document content using GPT-4o. By feeding in a structured prompt and the content of a document, the system returns:

- The **year** related to the document  
- A **code** derived from the content  
- A **new filename** based on company name and full name  
- Any **warnings** about missing, conflicting, or suspicious content  

This is particularly useful for companies dealing with high volumes of tax or official documents that need to be organized, named consistently, and validated for content accuracy.

---

## 🚀 How to Run This Project

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
pip install -r requirements.txt
streamlit run app.py
visit ---> http://localhost:8501

 
============ Dependencies ============
Tesseract-OCR
poppler-24.08.0 # ai-renamer
# ai-renamer
