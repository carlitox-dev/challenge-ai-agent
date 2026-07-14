
from typing import List
from pathlib import Path

from langchain_classic.schema import Document
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from config import settings

INDEX_BASE_DIR = Path("storage/vector_index")

def dividir_documentos(documents: List[Document]) -> List[Document]:
    """
    Divide los documentos largos en fragmentos más pequeños manejables.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    return splitter.split_documents(documents)


def construir_vector_store(documents: List[Document]) -> FAISS:
    """
    Crea un índice vectorial FAISS para búsqueda semántica de la información 
    a partir de documentos en memoria.
    """
    chunks = dividir_documentos(documents)
    embeddings = get_embeddings()
    return FAISS.from_documents(chunks, embeddings)


def get_embeddings() -> HuggingFaceEmbeddings:
    """
    Crea el objeto de embeddings usando variables de entorno.
    """
    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={"device": settings.embedding_device},
        encode_kwargs={"normalize_embeddings": settings.embedding_normalize},
    )


def get_index_path(file_path: str) -> Path:
    """
    Genera una carpeta estable para el índice según el nombre del archivo.
    """
    source_name = Path(file_path).stem.replace(" ", "_").lower()
    return INDEX_BASE_DIR / source_name


def guardar_vector_store(vector_store: FAISS, index_path: Path) -> None:
    """
    Guarda el índice FAISS en disco para ser reutilizado luego.
    """
    index_path.mkdir(parents=True, exist_ok=True)
    vector_store.save_local(str(index_path))


def cargar_vector_store(index_path: Path) -> FAISS:
    """
    Carga un índice FAISS ya persistido en disco.

    Solo debe usarse con índices generados por esta misma aplicación,
    ya que la deserialización local requiere confianza en el origen.
    """
    embeddings = get_embeddings()
    return FAISS.load_local(
        str(index_path),
        embeddings,
        allow_dangerous_deserialization=True,
    )


def obtener_crear_vector_store(file_path: str, documents: List[Document]) -> FAISS:
    """
    Reutiliza un índice existente o lo crea una sola vez si no existe.

    Este método evita reprocesar el documento en cada consulta. 
    Si el archivo ya fue indexado antes, se carga el índice local.
    Si no existe, se crea y guarda para realizar las consultas.
    """
    index_path = get_index_path(file_path)

    if index_path.exists():
        return cargar_vector_store(index_path)

    vector_store = construir_vector_store(documents)
    guardar_vector_store(vector_store, index_path)
    return vector_store
