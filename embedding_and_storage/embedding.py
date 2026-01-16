from dotenv import load_dotenv
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")


_embeddings =None

def create_embedding_model():
    global _embeddings
    if _embeddings is None:
        _embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=api_key
        )
    return _embeddings