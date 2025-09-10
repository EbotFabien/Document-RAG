import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from config import Config
from app.parsers import parse_file
from app.rag import load_db, create_question_embedding, search, run_mistral
import shutil


app = Flask(__name__)
app.config.from_object(Config)

# Ensure uploads folder exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Per-document storage
DOCUMENTS = {}  # filename -> list of chunks
INDEXES = {}    # filename -> FAISS index

PRELOADED_FILES = [
    "Mistral AI Overview.txt",
    "RAG & Vector Search Guide.txt",
    "Mistral SDK Python Examples.txt",
    "LLM Benchmarks & Research Notes.txt",
    "Practical AI Use Cases & Tutorials.txt",
    "Internal FAQ Dataset.txt"
]

PRELOAD_FOLDER = app.config["PRELOAD_FOLDER"]
os.makedirs(PRELOAD_FOLDER, exist_ok=True)

def preload_documents():
    """Load preloaded documents into memory and build FAISS indexes."""
    print("Loading docs wait please")
    for filename in PRELOADED_FILES:
       
            path = os.path.join(PRELOAD_FOLDER, filename)
            if os.path.exists(path):
                destination = os.path.join(app.config["UPLOAD_FOLDER"],filename)
                shutil.copy(path, destination)
                
                try:
                    chunks = parse_file(path)
                except Exception as e:
                    flash(f"Error parsing file: {str(e)}")
                    return redirect(request.url)
                
                DOCUMENTS[filename] = chunks
                INDEXES[filename], _ = load_db(chunks)
    print("DONE,APP STARTING")
            


# Preload on startup
preload_documents()

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]



@app.route("/")
def index():
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("index.html", files=files)

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            # Parse file into chunks 
            try:
                chunks = parse_file(filepath)
            except Exception as e:
                flash(f"Error parsing file: {str(e)}")
                return redirect(request.url)

            # Store per-document
            DOCUMENTS[file.filename] = chunks
            INDEXES[file.filename], _ = load_db(chunks)

            flash("File uploaded and indexed successfully!")
            # Redirect to chat for this document
            return redirect(url_for("chat", doc=file.filename))
        else:
            flash("Invalid file type")
            return redirect(request.url)
    return render_template("upload.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    doc = request.args.get("doc")
    if not doc or doc not in DOCUMENTS:
        flash("Document not found!")
        return redirect(url_for("index"))

    chunks = DOCUMENTS[doc]
    index = INDEXES[doc]

    answer = None
    retrieved = []
    question = None

    if request.method == "POST":
        question = request.form.get("question")
        q_embedding = create_question_embedding(question)
        retrieved, _ = search(index, q_embedding, chunks, k=2)

        context = " ".join(retrieved)
        prompt = f"Your Name is Jarvis,Fabien's Personal AI.Answer the following question based only on the provided context,give precise and concised answers only to the provided question.\n\nContext:\n{context}\n\nQuestion: {question}"
        answer = run_mistral(prompt)

    return render_template("chat.html", answer=answer, retrieved=retrieved, question=question, doc=doc)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
