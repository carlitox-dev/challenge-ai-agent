
from pathlib import Path
from typing import Any

#from langchain.chains import RetrievalQA
from langchain_classic.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from document_loader import cargar_documentos
from vector_store import construir_vector_store

from config import settings

def crear_agente() -> RetrievalQA:
    """Construye un agente RAG con Google Gemini para análisis de documentos.

    Flujo principal:
    1. Cargar los archivos y documentos fuente.
    2. Convertirlos en chunks semánticos.
    3. Crear un índice vectorial FAISS.
    4. Conectar Gemini con un retriever para responder preguntas.
    """
    data_path = 'data/documento.pdf'

    documentos = cargar_documentos([Path(data_path)])
    vector_store = construir_vector_store(documentos)
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})


    gemini_model = 'gemini-3.1-pro-preview'
    groq_model = 'llama-3.3-70b-versatile'

    llm = ChatGroq(
        model = groq_model,  # ToDo cambiar luego con settings.groq_model
        temperature=0,
        groq_api_key = settings.groq_api_key,
    ) 

    llm_2 = ChatGoogleGenerativeAI(
        model = gemini_model,   # ToDo cambiar luego con settings.gemini_model
        temperature = 0,
        google_api_key = settings.gemini_api_key,
    )

    return RetrievalQA.from_chain_type(
        llm = llm,
        chain_type = "stuff",
        retriever = retriever,
        return_source_documents = True,
    )

def preguntar_agente(agent: RetrievalQA, question: str) -> dict[str, Any]:
    """Ejecuta la consulta y devuelve respuesta junto con metadatos fuente."""
    result = agent.invoke({"query": question})
    return {
        "answer": result["result"],
        "sources": [doc.metadata for doc in result.get("source_documents", [])],
    }
