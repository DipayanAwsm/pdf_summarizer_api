from fastapi import FastAPI, UploadFile, File
import fitz  # PyMuPDF
from transformers import pipeline

app = FastAPI()

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

@app.post("/summarize-pdf/")
async def summarize_pdf(file: UploadFile = File(...)):
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    text = extract_text_from_pdf(file_location)
    text = text[:3000]  # Limit for Hugging Face input

    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)

    return {"summary": summary[0]["summary_text"]}
