# 📚 Flask RAG Demo with Mistral SDK

This project is a **Flask-based Retrieval-Augmented Generation (RAG)** demo built.  
It lets you **upload documents**, indexes them with **FAISS**, and enables **chatting with the document content in context only** via the **Mistral AI SDK**.

---

## ✨ Features

- 🔹 Upload `.txt` files into the knowledge base  
- 🔹 Automatic text chunking & FAISS vector indexing  
- 🔹 Chat with your uploaded documents (context-aware answers)  
- 🔹 Temporary file storage for clean demo runs  
- 🔹 Simple and beautiful UI (HTML + CSS, Jinja templates)  

---

## 📂 Project Structure

```bash
.
├── app/
│   ├── templates/         # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── upload.html
│   │   └── chat.html
│   ├── static/            # CSS / JS / images
│   │   └── styles.css
│   ├── parsers.py         # File parsing & chunking
│   ├── rag.py             # FAISS, embeddings, Mistral chat
│   └── utils.py           # Helpers
├── uploads/               # Uploaded docs (only in persistent mode)
├── preloaded_docs/        # Preloaded docs (only in persistent mode)
├── config.py              # App configuration
├── main.py                # Flask entrypoint
├── requirements.txt       # Dependencies
└── README.md              # Project documentation
```
---
## ⚙️ Installation

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/EbotFabien/Document-RAG.git
cd Document-RAG
python3 -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)
pip install -r requirements.txt 
```
---
## 🔑 Configuration

Set your Mistral API key as an environment variable:

```bash
export MISTRAL_API_KEY="your_api_key_here"   # Mac/Linux
set MISTRAL_API_KEY="your_api_key_here"      # Windows (Powershell)
```
---
## 🚀 Run the App
```bash
python main.py
```

👉 Now open: [http://127.0.0.1:5000](http://127.0.0.1:5000)

> ⚠️ **NB:** Make sure port **5000** is free before running the app.  
> If another service is using it, stop that service or change the port in `main.py`.

---
## 🗂️ Knowledge Base

The demo includes preloaded documents (in `uploads/`) to showcase Mistral RAG capabilities:

```text
1 Mistral AI Overview.txt.txt        → Overview of Mistral AI and models
2 RAG & Vector Search Guide.txt     → RAG concepts with FAISS examples
3 Mistral SDK Python Examples.txt.txt               → Mistral SDK usage (chat, embeddings, streaming)
4 LLM Benchmarks & Research Notes.txt       → Summaries of LLM benchmarks
5 Practical AI Use Cases & Tutorials.txt               → AI applications and practical demos
6 Internal FAQ Dataset.txt             → FAQ-style notes for demos and API testing
```

---
## 📝 License

This project is licensed under the **MIT License** © 2025 Fabien Ebot.

