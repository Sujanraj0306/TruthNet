from sentence_transformers import SentenceTransformer
from chromadb.utils.embedding_functions import EmbeddingFunction
import torch


class SemanticEmbeddingFunction(EmbeddingFunction):
    def __init__(self):
        device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
        self.embedder = SentenceTransformer("BAAI/bge-base-en-v1.5", device=device)

    def __call__(self, input):
        return self.embedder.encode(input)
