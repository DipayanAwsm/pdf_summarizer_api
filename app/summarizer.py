from typing import List
from transformers import pipeline, AutoTokenizer
from PyPDF2 import PdfReader

# ✅ Use a lightweight model that fits Render free tier memory.
MODEL_NAME = "knkarthick/MEETING_SUMMARY"

# Force CPU usage to avoid MPS/Long dtype issues on macOS and keep memory small on Render
summarizer = pipeline("summarization", model=MODEL_NAME, device=-1)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts text from a PDF using PyPDF2 (works for digital PDFs)."""
    try:
        reader = PdfReader(pdf_path)
        parts: List[str] = []
        for page in reader.pages:
            parts.append(page.extract_text() or "")
        return "\n".join(parts).strip()
    except Exception:
        return ""

def summarize_text(text: str) -> str:
    """
    Summarize with token-safe truncation.
    Most encoder-decoder models have ~1024 token context; we truncate safely.
    """
    if not text:
        return "No text to summarize."

    # Tokenize and truncate safely to the model's max length
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=1024
    )
    # Decode back to string so pipeline handles batching/strings nicely
    safe_text = tokenizer.decode(inputs["input_ids"][0], skip_special_tokens=True)

    result = summarizer(
        safe_text,
        max_length=130,
        min_length=30,
        do_sample=False
    )
    return result[0]["summary_text"]
