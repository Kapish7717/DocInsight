import os
from dotenv import load_dotenv

load_dotenv()

# ------------------
# Environment
# ------------------
ENV = os.getenv("ENV", "dev")

# ------------------
# Models
# ------------------
LLM_MODEL_NAME = "llama-3.1-8b-instant"
EMBEDDING_MODEL = "models/gemini-embedding-001"

# ------------------
# Paths
# ------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
CHROMA_PATH = os.path.join(DATA_DIR, "chroma_db")

# ------------------
# Retrieval
# ------------------
TOP_K = 3
SCORE_THRESHOLD = 0.3

# ------------------
# Context / Tokens
# ------------------
MAX_CONTEXT_CHARS = 3000
