# aegis_shield/evaluation/base_evaluator.py

from abc import ABC, abstractmethod

import pandas as pd


class BaseEvaluator(ABC):
    """
    Abstract base class for all evaluation methods.
    """

    def __init__(self, name: str):
        """
        Initialize the evaluator with a name.
        :param name: Name of the evaluation method.
        """
        self.name = name

    @abstractmethod
    def evaluate(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Abstract method to evaluate similarity or other metrics.
        :param: Dataframe with relevant columns
        :return: DataFrame with evaluation results.
        """
        pass
