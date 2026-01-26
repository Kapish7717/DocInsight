from dotenv import load_dotenv
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from app.config import LLM_MODEL_NAME, EMBEDDING_MODEL
from app.schemas import QueryVariations
load_dotenv()   
api_key = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = api_key

def get_embedding():
    return GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)

def chat_model():
    return ChatGroq(model_name=LLM_MODEL_NAME)



llm_with_tools = chat_model().with_structured_output(QueryVariations)


