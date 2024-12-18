# aegis_shield/evaluation/embedding_scorers.py

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from aegis_shield.evaluation.base import BaseEvaluator
from aegis_shield.utils.embeddings import EmbeddingGenerator
from aegis_shield.utils.registry import Registry


@Registry.register("embedding_evaluator")
class EmbeddingEvaluator(BaseEvaluator):
    """
    Computes cosine similarity between query embeddings and document embeddings.
    """

    def __init__(self, model_name: str, similarity_threshold: float = 0.7):
        """
        Initialize the evaluator with the model and backend.
        :param model_name: Name of the embedding model.
        :param backend: Library to use ('sentence-transformers' or 'fastembed').
        """
        super().__init__(name="Cosine Similarity")
        self.embedding_generator = EmbeddingGenerator(model_name)
        self.similarity_threshold = similarity_threshold

    def evaluate(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Optimized evaluation of the search API performance.

        :param data: DataFrame with 'question', 'correct_answer', and 'search_api_results'.
        :return: DataFrame with evaluation results.
        """
        # Step 1: Normalize correct_answer and search_api_results to lists
        data["correct_answer"] = data["correct_answer"].apply(
            lambda x: [x] if isinstance(x, str) else x
        )
        data["actual_answers"] = data["actual_answers"].apply(
            lambda x: x if isinstance(x, list) else [x]
        )

        # Step 2: Flatten correct_answer and search_api_results for batch embedding generation
        all_correct_answers = data["correct_answer"].explode().tolist()
        all_search_results = data["search_api_results"].explode().tolist()

        # Step 3: Generate embeddings for all correct answers and search results at once
        print("Generating embeddings for correct answers and search results...")
        correct_embeddings = self.embedding_generator.generate_embeddings(
            all_correct_answers
        )
        search_embeddings = self.embedding_generator.generate_embeddings(
            all_search_results
        )

        # Step 4: Compute cosine similarity between all correct and search embeddings
        print("Computing cosine similarity...")
        similarity_matrix = cosine_similarity(correct_embeddings, search_embeddings)

        # Step 5: Calculate metrics using precomputed similarity matrix
        results = []

        correct_idx = 0  # Starting index for correct answers
        search_idx = 0  # Starting index for search results

        # Vectorized slicing of the similarity matrix and metric computation
        num_correct_answers_list = data["correct_answer"].apply(len).tolist()
        num_search_results_list = data["search_api_results"].apply(len).tolist()

        for i, (num_correct, num_search) in enumerate(
            zip(num_correct_answers_list, num_search_results_list)
        ):
            # Slice the similarity matrix for this question
            correct_slice = similarity_matrix[correct_idx : correct_idx + num_correct]
            search_slice = correct_slice[:, search_idx : search_idx + num_search]

            # Metrics
            max_similarity = np.max(search_slice)
            avg_similarity = np.mean(search_slice)
            coverage = np.sum(search_slice >= self.similarity_threshold) / num_search

            results.append(
                {
                    "question": data.loc[i, "question"],
                    "correct_answer": data.loc[i, "correct_answer"],
                    "actual_answer": data.loc[i, "correct_answer"],
                    "max_similarity": max_similarity,
                    "average_similarity": avg_similarity,
                    "coverage": coverage,
                }
            )

            # Update indices for the next slice
            correct_idx += num_correct
            search_idx += num_search

        return pd.DataFrame(results)
