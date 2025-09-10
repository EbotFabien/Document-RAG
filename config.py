import os

class Config:
    SECRET_KEY = "supersecretkey"
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
    PRELOAD_FOLDER= os.path.join(os.path.dirname(__file__), "preloaded_docs")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB upload limit
    ALLOWED_EXTENSIONS = {"txt"}
    MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")

