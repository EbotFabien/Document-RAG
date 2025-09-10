from __future__ import annotations
from typing import List
import os

# For PDF and DOCX parsing



def chunk_text(text: str, size: int = 2048) -> List[str]:
    """Split text into fixed-size chunks."""
    return [text[i:i + size] for i in range(0, len(text), size)]

def parse_txt(file_path: str) -> List[str]:
    with open(file_path, "r", errors="ignore") as f:
        text = f.read()
    return chunk_text(text)




def parse_file(file_path: str) -> List[str]:
    """Auto-detect file type and parse into chunks."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        return parse_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
