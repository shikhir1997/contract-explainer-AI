import streamlit as st
import pdfplumber
import docx

st.set_page_config(page_title="Contract Explainer AI")

st.title("📄 Contract Explainer AI")
st.caption("Upload a contract or policy (PDF/DOCX) and extract its content")

def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join(p.text for p in doc.paragraphs)

uploaded_file = st.file_uploader("Upload a contract (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    st.success("✅ File uploaded: " + uploaded_file.name)

    if uploaded_file.name.endswith(".pdf"):
        content = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        content = extract_text_from_docx(uploaded_file)
    else:
        content = "Unsupported file type."

    st.subheader("📜 Extracted Text")
    st.text_area("Document Content", content, height=400)
