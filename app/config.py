"""
Archivo de configuración de la aplicación
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    embeddings_model: str = os.getenv("EMBEDDINGS_MODEL", "models/embedding-001")
    data_path: str = os.getenv("DATA_PATH", "data/documento.pdf")
    vector_dir: str = os.getenv("VECTOR_DIR", "vectorstore")
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1000"))

    # =========================
    # config OCI // ToDo

settings = Settings()