import os
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# If you host the frontend elsewhere and truly need CORS, uncomment below:
# from fastapi.middleware.cors import CORSMiddleware

from app.summarizer import extract_text_from_pdf, summarize_text

app = FastAPI()

# ❗ Only add CORS if your frontend runs on a different domain.
# For same-origin (your case on Render), you don't need CORS at all.
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["https://pdf-summarizer-api-83l1.onrender.com"],
#     allow_credentials=False,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

templates = Jinja2Templates(directory="templates")

# Paths: summaries/ lives at project root (one level above /app)
APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(APP_DIR)
SUMMARY_DIR = os.path.join(PROJECT_ROOT, "summaries")
os.makedirs(SUMMARY_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/summarize-pdf/")
async def summarize_pdf(file: UploadFile = File(...)):
    try:
        original_filename = file.filename or "uploaded.pdf"
        # Save PDF into summaries/
        pdf_path = os.path.join(SUMMARY_DIR, original_filename)
        with open(pdf_path, "wb") as f:
            f.write(await file.read())

        text = extract_text_from_pdf(pdf_path)
        if not text.strip():
            return {"summary": "No readable text found in PDF."}

        summary = summarize_text(text)

        # Save summary .txt alongside PDF
        summary_path = os.path.join(SUMMARY_DIR, f"{original_filename}_summary.txt")
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)

        # ⚠️ IMPORTANT: Do NOT try to git add/commit/push on Render.
        # That will fail in a read-only ephemeral container.
        # Keep any git-commit logic only for local runs.

        return {"summary": summary}
    except Exception as e:
        return {"summary": f"Error: {str(e)}"}
