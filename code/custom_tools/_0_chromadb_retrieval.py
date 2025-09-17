import chromadb
from custom_tools._1_custom_embedding import (
    SemanticEmbeddingFunction,
)
import os

base = os.getcwd()
folder_path = os.path.join(base, "knowledge_base", "chroma_db")
print(folder_path)


def retrieve_chromadb_authentic(collection_name):
    hf_embedding_model = SemanticEmbeddingFunction()

    chroma_client = chromadb.PersistentClient(path=f"{folder_path}/{collection_name}")
    collection = chroma_client.get_or_create_collection(
        name="authentic",
        embedding_function=hf_embedding_model,
    )

    return collection


def retrieve_chromadb_user(collection_name):
    hf_embedding_model = SemanticEmbeddingFunction()

    chroma_client = chromadb.PersistentClient(path=f"{folder_path}/{collection_name}")
    collection = chroma_client.get_or_create_collection(
        name="user",
        embedding_function=hf_embedding_model,
    )

    return collection
