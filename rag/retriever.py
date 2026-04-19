from rag.ingest import load_vector_store

def retrieve_context(query: str, k: int = 3) -> str:
    store = load_vector_store()
    results = store.similarity_search(query, k=k)
    return "\n".join([doc.page_content for doc in results])
