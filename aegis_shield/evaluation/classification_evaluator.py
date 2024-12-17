# aegis_shield/evaluation/classification_evaluator.py

from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score
import pandas as pd
from aegis_shield.evaluation.base import BaseEvaluator
from aegis_shield.utils.registry import Registry

@Registry.register("classification_evaluator")
class ClassificationEvaluator(BaseEvaluator):
    """
    Evaluator to compute classification metrics: Precision, Recall, F1-Score, Accuracy, and Confusion Matrix.
    """

    def __init__(self):
        """
        Initialize the classification evaluator.
        """
        super().__init__(name="Classification Evaluator")

    def evaluate(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Evaluate classification metrics.

        :param data: DataFrame with 'correct_labels' (ground truth) and 'predicted_labels' (predictions).
        :return: DataFrame with classification metrics and confusion matrix.
        """
        # Step 1: Validate inputs
        if "correct_labels" not in data.columns or "predicted_labels" not in data.columns:
            raise ValueError("Input DataFrame must contain 'correct_labels' and 'predicted_labels' columns.")

        correct_labels = data["correct_labels"]
        predicted_labels = data["predicted_labels"]

        # Step 2: Compute metrics
        conf_matrix = confusion_matrix(correct_labels, predicted_labels)
        precision = precision_score(correct_labels, predicted_labels, average="weighted", zero_division=0)
        recall = recall_score(correct_labels, predicted_labels, average="weighted", zero_division=0)
        f1 = f1_score(correct_labels, predicted_labels, average="weighted", zero_division=0)
        accuracy = accuracy_score(correct_labels, predicted_labels)

        # Step 3: Prepare metrics
        metrics_summary = {
            "Metric": ["Precision", "Recall", "F1-Score", "Accuracy"],
            "Value": [round(precision, 4), round(recall, 4), round(f1, 4), round(accuracy, 4)],
        }

        # Step 4: Convert confusion matrix to DataFrame
        labels = sorted(set(correct_labels).union(set(predicted_labels)))  # Get all unique class labels
        conf_matrix_df = pd.DataFrame(conf_matrix, index=labels, columns=labels)
        conf_matrix_df.index.name = "True_Label"
        conf_matrix_df.columns.name = "Predicted_Label"

        # Step 5: Combine results
        metrics_df = pd.DataFrame(metrics_summary)
        combined_results = {"metrics": metrics_df, "confusion_matrix": conf_matrix_df}

        return combined_results
