import re
from typing import List

def legal_clause_chunk(text: str) -> List[str]:
    """
    Splits a contract into legal-style clauses using regex patterns based on section headers.
    """
    # Normalize whitespace
    text = re.sub(r'\r\n|\r', '\n', text)
    text = re.sub(r'\n{2,}', '\n\n', text)

    # Split on typical legal clause formats (e.g., "1.", "A)", "Definitions:", etc.)
    pattern = re.compile(r"(?=\n(?:\d{1,2}[\.\)]|[A-Z][a-zA-Z\s]{2,40}:))")
    raw_chunks = pattern.split(text)

    # Clean and filter out small junk chunks
    cleaned = [chunk.strip() for chunk in raw_chunks if len(chunk.strip().split()) > 25]
    return cleaned
