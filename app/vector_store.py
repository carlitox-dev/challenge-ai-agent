import os
from typing import List

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from config import settings

def split_documents(documents: List[Document]) -> List[Document]:
    """
    Divide los documentos largos en fragmentos más pequeñps manejables.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    return splitter.split_documents(documents)


def build_vector_store(documents: List[Document]) -> FAISS:
    """Crea un índice vectorial FAISS para búsqueda semántica de la información."""
    chunks = split_documents(documents)
    embedding_model = settings.embeddings_model
    embeddings = GoogleGenerativeAIEmbeddings(
        model = embedding_model,
        google_api_key = settings.gemini_api_key,
    )
    return FAISS.from_documents(chunks, embeddings)