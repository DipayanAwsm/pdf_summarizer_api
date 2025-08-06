pdf_summarizer_api/
├── app/
│   ├── main.py                ← FastAPI backend
│   └── summarizer.py          ← (optional) helper for text extraction & summary
│
├── static/                    ← (optional) for styling or JS
│
├── templates/
│   └── index.html             ← Frontend: file upload + summary viewer
│
├── requirements.txt           ← All dependencies
├── README.md                  ← Project documentation
└── .gitignore                 ← Ignore virtual env, cache, etc.