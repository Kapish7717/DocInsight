import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from app.models import get_embedding
# from app.config import CHROMA_PATH
from app.config import CHROMA_PATH



# loader = PyPDFLoader(r"C:\Kapish\RAG_project\data\2502.18845v1.pdf")
# docs = loader.load()
# print(len(docs))

def load_document(path):
    if path.endswith(".pdf"):
        return PyPDFLoader(path).load()
    else:
        return TextLoader(path).load()

def ingest_pdfs(data_dir):
    """
    Loads PDFs from data/raw/, chunks them, embeds them,
    and stores them in Chroma vector DB.
    """

    docs = load_document(data_dir)
    if not docs:
        print("⚠️ No PDFs found in data/raw/")
        return

    # Chunking
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True, 
    )
    chunks = splitter.split_documents(docs)

    # Store in vector DB
    db = Chroma.from_documents(
        # collection_name=session_id,
        documents=chunks,
        embedding=get_embedding(),
        persist_directory=CHROMA_PATH
    )

    print(f"✅ Ingested {len(chunks)} chunks into Chroma")


if __name__ == "__main__":
    ingest_pdfs()
