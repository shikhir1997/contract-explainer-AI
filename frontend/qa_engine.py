from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def build_vector_index(chunks):
    embeddings = embedding_model.encode(chunks)
    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings))
    return index, embeddings

def get_top_chunks(question, chunks, index, embeddings, top_k=3):
    question_vec = embedding_model.encode([question])
    D, I = index.search(question_vec, top_k)
    return [chunks[i] for i in I[0]]

def answer_question(question, chunks, index, embeddings):
    top_chunks = get_top_chunks(question, chunks, index, embeddings)
    context = "\n\n".join(top_chunks)

    prompt = f"""
You are a helpful assistant. Based on the contract text below, answer the question clearly and accurately.

Contract Chunks:
\"\"\"
{context}
\"\"\"

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()

def generate_faqs_from_contract(clauses, num_questions=10):
    contract_text = "\n\n".join(clauses)

    prompt = f"""
You are a legal assistant AI. Based on the contract below, generate {num_questions} important and relevant questions a person might ask to better understand their rights, obligations, and risks. Then answer each question clearly and concisely.

Respond in this format:

Q1: ...
A1: ...
Q2: ...
A2: ...
...
answer should be in the next line
Contract:
\"\"\"
{contract_text}
\"\"\"
"""

    response = client.chat.completions.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()
