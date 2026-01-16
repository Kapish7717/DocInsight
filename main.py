from ingestion.github_loader import documents
from processing.cleaner import clean_docs
from processing.chunker import chunk_docs
from embedding_and_storage import create_embedding_model

docs = documents
cleaned_docs = clean_docs(docs)

chunked_docs = chunk_docs(cleaned_docs)

embedding_model = create_embedding_model()
