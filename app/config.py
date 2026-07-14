"""
Archivo de configuración de la aplicación
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:

    groq_api_key: str | None = os.getenv("GROQ_API_KEY")
    groq_model: str = os.getenv("GROQ_MODEL")

    embedding_model: str = os.getenv("EMBEDDING_MODEL")
    embedding_device: str = "cpu"
    embedding_normalize: bool = "true"

    file_path: str = "data/documento.pdf"
    data_path: str = "data"
    vector_dir: str = "vectorstore"

    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1000"))

settings = Settings()