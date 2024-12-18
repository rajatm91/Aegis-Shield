# aegis_shield/utils/embedding_generator.py

import numpy as np
from fastembed import TextEmbedding
from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:
    """
    Utility to load a model and generate embeddings for input text.
    Supports: Sentence Transformers and FastEmbed.
    """

    def __init__(self, model_name: str):
        """
        Initialize the embedding generator.

        :param model_name: Name of the pre-trained model to load.
        :param backend: Backend library to use ('sentence-transformers' or 'fastembed').
        """
        self.embedding_model = TextEmbedding(
            model_name=model_name,
        )

    def generate_embeddings(self, texts: list) -> list[np.ndarray]:
        """
        Generate embeddings for a list of texts.
        :param texts: List of input text strings.
        :return: Numpy array of embeddings.
        """

        return self.embedding_model.embed(texts)
