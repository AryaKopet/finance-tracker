import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join('static', 'uploads', 'proofs')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # Maksimal 5 MB

class Config:
    SECRET_KEY = "supersecretkey"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'finance.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
