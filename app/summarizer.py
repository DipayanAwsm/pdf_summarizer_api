import fitz  # PyMuPDF
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def extract_text_from_pdf(path: str) -> str:
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text[:3000]

def summarize_text(text: str) -> str:
    result = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return result[0]["summary_text"]
