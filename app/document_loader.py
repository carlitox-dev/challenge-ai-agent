from pathlib import Path
from typing import List

import pandas as pd
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader


def load_documents(file_paths: List[Path]) -> List[Document]:
    """
    Carga los documentos desde el path de archivos definido.

    Args:
        file_paths (List[Path]): Lista de path/ruta de archivos desde donde cargar los documentos.

    Returns:
        List[Document]: Lista de documentos cargados.
    """
    documents = []

    for file_path in file_paths:
        if file_path.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(file_path))
            documents.extend(loader.load())
        elif file_path.suffix.lower() == ".csv":
            df = pd.read_csv(file_path)
            for _, row in df.iterrows():
                content = " ".join(str(value) for value in row.values)
                metadata = {"source": str(file_path)}
                documents.append(Document(page_content=content, metadata=metadata))
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
    return documents


def load_pdf(file_path: str) -> List[Document]:
    """
    Lee archivos en formato PDF página por página y devuelve documentos LangChain.
    """
    loader = PyPDFLoader(file_path)
    return loader.load()


def load_csv(file_path: str) -> List[Document]:
    """
    Lee los archivos en formato CSV y convierte cada fila en un Document.
    """
    df = pd.read_csv(file_path)
    documents: List[Document] = []

    for index, row in df.iterrows():
        content = " | ".join([f"{column}: {row[column]}" for column in df.columns])
        documents.append(
            Document(
                page_content=content,
                metadata={
                    "source": Path(file_path).name,
                    "row": int(index),
                    "columns": list(df.columns),
                },
            )
        )
    return documents