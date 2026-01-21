from langchain_chroma import Chroma
from langchain_core.documents import Document
from app.models import chat_model
from app.config import TOP_K
from app.models import get_embedding
from langchain_community.retrievers import BM25Retriever
from sentence_transformers import CrossEncoder


vector_db = Chroma(persist_directory=r"C:\Kapish\RAG_project\data\chroma_db",
            embedding_function=get_embedding(),
            collection_metadata={"hnsw:space":"cosine"})

retriever = vector_db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": TOP_K}
)
data = vector_db.get()
all_docs = [
    Document(page_content=text, metadata=meta)
    for text, meta in zip
        ( data["documents"],
        data["metadatas"]
        ) 
    ]

bm25_retriever = BM25Retriever.from_documents( documents=all_docs, k=TOP_K)
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

model =chat_model()

def manual_hybrid_retrieval(query):
    vector_docs = retriever.invoke(query)
    bm25_docs = bm25_retriever.invoke(query)

    combined_docs = vector_docs + bm25_docs

    # deduplicate by content (ignore scores at this stage)
    seen = set()
    unique_docs = []

    for doc in combined_docs:
        content = doc.page_content.strip()
        if content not in seen:
            seen.add(content)
            unique_docs.append(doc)

    return unique_docs

def rerank_documents(query, docs):
    pairs = [(query, doc.page_content) for doc in docs]
    scores = reranker.predict(pairs)

    scored_docs = list(zip(docs, scores))

    scored_docs.sort(key=lambda x: x[1], reverse=True)

    reranked_docs = [doc for doc, score in scored_docs]
    reranked_scores = [score for doc, score in scored_docs]

    return reranked_docs, reranked_scores

def build_context(docs, max_chars=3000):
    context = ""
    for d in docs:
        if len(context) + len(d.page_content) > max_chars:
            break
        context += d.page_content + "\n\n"
    return context.strip()

def hybrid_retrieve(queries):
    all_docs = []
    for q in queries:
        docs = manual_hybrid_retrieval(q)
        all_docs.extend(docs)

    # Deduplicate
    seen = set()
    unique_docs = []
    for d in all_docs:
        content = d.page_content.strip()
        if content not in seen:
            seen.add(content)
            unique_docs.append(d)

    return unique_docs
