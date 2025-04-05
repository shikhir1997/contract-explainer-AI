import re
import streamlit as st
import pdfplumber
import docx
import os
from qa_engine import build_vector_index, answer_question
from qa_engine import generate_faqs_from_contract
from chunker import legal_clause_chunk
# from chunker import embed_chunking
from ai_utils import explain_clause
from dotenv import load_dotenv

# Load OpenAI key from .env
load_dotenv()

st.set_page_config(page_title="Contract Explainer AI")

st.title("📄 Contract Explainer AI")
st.caption("Upload a contract or policy (PDF/DOCX) and get clause-by-clause explanations.")

# --- File Parsing Logic ---
def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join(p.text for p in doc.paragraphs)

# --- File Upload UI ---
uploaded_file = st.file_uploader("📤 Upload a contract (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    st.success("✅ File uploaded: " + uploaded_file.name)

    if uploaded_file.name.endswith(".pdf"):
        content = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        content = extract_text_from_docx(uploaded_file)
    else:
        st.error("❌ Unsupported file type.")
        content = ""

    if content:
        # --- Chunk the contract text ---
        clauses = legal_clause_chunk(content)

        st.subheader("📑 Semantic Clauses")
        for i, clause in enumerate(clauses):
            st.markdown(f"**Clause {i+1}:**")
            st.text_area(f"Clause {i+1}", clause, height=150)

        st.subheader("💡 AI-Powered Explanations")

        if st.button("🔍 Generate Explanations"):
            for i, clause in enumerate(clauses):
                st.markdown(f"**Clause {i+1}:**")
                st.text_area(f"Original Clause {i+1}", clause, height=150)
                with st.spinner("Explaining..."):
                    explanation = explain_clause(clause)
                    st.text_area(f"Explanation {i+1}", explanation, height=150)
        # ✅ Add Q&A + FAQ section here
        index, embeddings = build_vector_index(clauses)

        tab1, tab2 = st.tabs(["❓ Ask a Question", "💡 Auto-generated FAQs"])

        with tab1:
            st.subheader("❓ Ask anything about the contract")
            user_question = st.text_input("Type your question here...")

            if user_question:
                with st.spinner("Generating answer..."):
                    answer = answer_question(user_question, clauses, index, embeddings)
                    st.markdown(f"**Answer:** {answer}")

        with tab2:
            st.subheader("💡 AI-Generated FAQs")

            with tab2:
                st.subheader("Smart FAQs about this document")
                if st.button("✨ Generate FAQs from this contract"):
                    with st.spinner("Analyzing and generating FAQs..."):
                        faq_output = generate_faqs_from_contract(clauses, num_questions=10)

                    # Display Q/A pairs
                    faq_pairs = re.findall(r"(Q\d+:.*?)(?=(Q\d+:|$))", faq_output, re.DOTALL)
                    for q_and_a, _ in faq_pairs:
                        st.markdown(q_and_a.strip())


