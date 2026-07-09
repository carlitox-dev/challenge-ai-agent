"""
Archivo de configuración de la aplicación
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
   
    gemini_api_key: str | None = os.getenv("GEMINI_API_KEY")
    gemini_model: str | None = os.getenv("GEMINI_MODEL")
    gemini_embedding_model: str | None = os.getenv("GEMINI_EMBEDDING_MODEL")
   
    groq_api_key: str | None = os.getenv("GROQ_API_KEY")
    groq_model: str | None = os.getenv("GROQ_MODEL")
    groq_embedding_model: str | None = os.getenv("GROQ_EMBEDDING_MODEL")

    data_path: str | None = os.getenv("DATA_PATH")
    vector_dir: str | None = os.getenv("VECTOR_DIR")

    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1000"))

    # =========================
    # config OCI // ToDo

settings = Settings()