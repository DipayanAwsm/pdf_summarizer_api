from transformers import pipeline
from PyPDF2 import PdfReader
import torch

device = 0 if torch.cuda.is_available() else -1
# Initialize summarizer model
#summarizer = pipeline("summarization")

# Force to CPU even if MPS is available (to avoid error)
summarizer = pipeline("summarization", device=device,model="knkarthick/MEETING_SUMMARY")


def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.strip()
    except Exception:
        return ""

def summarize_text(text):
    max_tokens = 1000
    chunks = [text[i:i+max_tokens] for i in range(0, len(text), max_tokens)]

    final_summary = ""
    for chunk in chunks:
        summary = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
        final_summary += summary[0]['summary_text'] + "\n"
    return final_summary.strip()
