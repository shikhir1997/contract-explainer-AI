from openai import OpenAI
import os
from dotenv import load_dotenv

# ✅ Load .env from the project root (one level up from frontend/)
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Make sure it's in your project root .env file.")

client = OpenAI(api_key=api_key)

def explain_clause(clause_text, simplify_level="basic"):
    prompt = f"""
You are a legal assistant AI. Simplify the following contract clause in plain English.

Clause:
\"\"\"
{clause_text}
\"\"\"

Your explanation (level: {simplify_level}):
- Keep it concise and accurate.
- Use bullet points if needed.
"""

    response = client.chat.completions.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()
