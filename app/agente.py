from pathlib import Path
from typing import Any

from langchain_classic.chains import RetrievalQA
from langchain_groq import ChatGroq

from document_loader import cargar_documentos
from vector_store import obtener_crear_vector_store

from config import settings

BASE_DIR = Path(__file__).resolve().parent.parent

def resolver_file_path() -> Path:
    candidate = Path(settings.file_path)
    if candidate.is_absolute():
        return candidate

    return (BASE_DIR / candidate).resolve()

def crear_agente() -> RetrievalQA:
    """
        Construye un agente para análisis de documentos.

        Flujo principal:
        1. Cargar los archivos y documentos fuente.
        2. Convertirlos en chunks semánticos.
        3. Crear un índice vectorial FAISS.
        4. Conectar el agente con un retriever para responder preguntas.
    """

    file_path = resolver_file_path()
    #file_path = settings.file_path

    if not file_path.exists():
        raise FileNotFoundError(f"No existe el archivo de entrada: {file_path}")

    documentos = cargar_documentos([file_path])
    #documentos = cargar_documentos([Path(file_path)])
    #vector_store = obtener_crear_vector_store(file_path, documentos)
    vector_store = obtener_crear_vector_store(str(file_path), documentos)
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    # llm utilizando Groq para la generación de respuestas
    llm = ChatGroq(
        model=settings.groq_model,
        temperature=0,
        groq_api_key=settings.groq_api_key,
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
    )

def preguntar_agente(agent: RetrievalQA, question: str) -> dict[str, Any]:
    """
    Ejecuta la consulta y devuelve respuesta junto con metadatos fuente.
    
    Args:
        agent (RetrievalQA): Agente inteligente para responder preguntas.
        question (str): Pregunta realizada.
    Returns:
        dict[str, Any]: Diccionario con la respuesta y las fuentes de los documentos consultados.
    """

    resultado = agent.invoke({"query": question})
    fuente_documentos = resultado.get("source_documents", [])
    fuentes_formateadas = []

    for doc in fuente_documentos:
        metadata = doc.metadata or {}
        fuentes_formateadas.append(
            {
                "source": metadata.get("source", "desconocido"),
                "page": metadata.get("page", "N/A"),
            }
        )
    return {
        "answer": resultado["result"],
        "sources": fuentes_formateadas,
    }