import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


VECTOR_STORE_PATH = os.path.join(os.path.dirname(__file__), "vector_store")

_store = None

def get_store():
    global _store
    if _store is None:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        _store = FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)
    return _store

def retrieve_context(query: str, k: int = 3) -> str:
    docs = get_store().similarity_search(query, k=k)
    return "\n".join(doc.page_content for doc in docs)
