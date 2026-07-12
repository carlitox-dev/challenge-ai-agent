"""
Archivo de configuración de la aplicación
"""
"""
Archivo de configuración de la aplicación
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:

    def _resolver_valor(env_var: str, ocid_env_var: str | None = None) -> str | None:
        """
        Resuelve un valor de configuración con la siguiente prioridad:

        1. Variable de entorno "plana" (uso típico en desarrollo local, vía .env).
        2. Secreto en OCI Vault, referenciado por el OCID guardado en la variable
        de entorno indicada en `ocid_env_var` (uso típico al desplegar en una
        instancia OCI, donde el valor sensible no viaja en texto plano).

        Args:
            env_var (str): Nombre de la variable de entorno con el valor directo.
            ocid_env_var (str | None): Nombre de la variable de entorno que
                contiene el OCID del secreto en OCI Vault, si aplica.

        Returns:
            str | None: El valor resuelto, o None si no se encontró en ninguna fuente.
        """
        valor = os.getenv(env_var)
        if valor:
            return valor

        if ocid_env_var:
            secret_ocid = os.getenv(ocid_env_var)
            if secret_ocid:
                from secrets_manager import obtener_secreto
                return obtener_secreto(secret_ocid)

        return None

   
    gemini_api_key: str | None = _resolver_valor("GEMINI_API_KEY", "GEMINI_API_KEY_OCID")
    gemini_model: str | None = os.getenv("GEMINI_MODEL")
    gemini_embedding_model: str | None = os.getenv("GEMINI_EMBEDDING_MODEL")

    groq_api_key: str | None = _resolver_valor("GROQ_API_KEY", "GROQ_API_KEY_OCID")
    groq_model: str | None = os.getenv("GROQ_MODEL")
    groq_embedding_model: str | None = os.getenv("GROQ_EMBEDDING_MODEL")

    file_path: str = 'data/documento.pdf'
    data_path: str = 'data'
    vector_dir: str ='vectorstore'

    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1000"))

settings = Settings()