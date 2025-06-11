from langchain.vectorstores import Chroma
from .embeddings import get_embeddings

def get_chroma():
    embeddings = get_embeddings()
    
    return Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )