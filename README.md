# 📄 GPT-4o Document Metadata Extractor

This Python-based project utilizes **OpenAI's GPT-4o** to process document content and intelligently extract structured metadata, such as:

- 📅 **Year**
- 🧾 **Code**
- 📁 **Generated Filename**
- ⚠️ **Warnings** (e.g., missing, conflicting, or suspicious content)

This tool is ideal for automating the classification and validation of official or tax-related documents.

---

## 🔍 Purpose

The goal of this project is to **automate metadata extraction** and **validate key content** from documents using GPT-4o, improving the efficiency and accuracy of document management.

---

## ⚙️ Requirements

Ensure the following are installed:

- ✅ Python **3.9.5**  
  👉 [Download Python 3.9.5](https://www.python.org/downloads/release/python-395/)
- ✅ **Tesseract OCR**  
  👉 [Download Tesseract OCR](https://digi.bib.uni-mannheim.de/tesseract/)
- ✅ **Poppler for Windows**  
  👉 [Download Poppler](https://github.com/oschwartz10612/poppler-windows/releases)
- ✅ **Internet Connection** (Required for GPT-4o API)
- ✅ **Streamlit** (Python package)

---

## 🚀 Installation Guide

### 🔧 Step 1: Install Python 3.9.5

- Download from the link above.
- During installation, **check the box** that says: `Add Python to PATH`.

---

### 📁 Step 2: Clone Project & Install Dependencies

In your terminal (Command Prompt), navigate to the root directory of the project and run:

```bash
pip install -r requirements.txt
```

---

### 🔤 Step 3: Install Tesseract OCR

1. Download the setup file:  
   [tesseract-ocr-w64-setup-v5.3.0.20221214.exe](https://digi.bib.uni-mannheim.de/tesseract/)

2. Install it and note the install path (usually:  
   `C:\Program Files\Tesseract-OCR`)

3. Add this path to your system’s **Environment Variables → Path**.

---

### 🖼️ Step 4: Install Poppler for Windows

1. Download the latest version from:  
   [Poppler Releases](https://github.com/oschwartz10612/poppler-windows/releases)

2. Extract the ZIP and move the folder to your `C:` drive.  
   For example: `C:\Release-24.08.0-0`

3. Add this path to Environment Variables:  
   `C:\Release-24.08.0-0\poppler-24.08.0\Library\bin`

---

### 🌐 Step 5: Install Streamlit

```bash
pip install streamlit
```

Then verify installation:

```bash
pip show streamlit
```

Copy the **Location path** from the output (e.g.,  
`C:\Users\YourName\AppData\Local\Programs\Python\Python39\Lib\site-packages`)  
and add it to your **Environment Variables → Path**.

---

### 🔁 Step 6: Restart Your System

After setting all environment variables, **restart your PC** to ensure all changes take effect.

---

## ▶️ How to Run the Application

1. Navigate to the project’s **root directory**.
2. Open the **dist** folder.
3. Double-click the `.exe` file inside.
4. The application will launch and start automatically.

---



