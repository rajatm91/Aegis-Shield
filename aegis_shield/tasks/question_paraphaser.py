# common/transformation.py
import pandas as pd
import torch
from parrot import Parrot

from aegis_shield.utils.registry import Registry


@Registry.register("paraphase_questions")
class QuestionParaphaser:
    def __init__(self):
        print("Loading Parrot Paraphraser model...")
        self.model_name = "prithivida/parrot_paraphraser_on_T5"
        self.model = Parrot(
            model_tag=self.model_name, use_gpu=torch.cuda.is_available()
        )
        print("Model loaded successfully.")

    def generate_paraphase(self, row):
        question = row["questions"]
        label = row["label"]

        print(f"Paraphrasing question : {question}")

        para_phases = self.model.augment(
            input_phrase=question,
            diversity_ranker="euclidean",
            do_diverse=True,
            max_return_phrases=10,
            max_length=64,
            adequacy_threshold=0.70,
            fluency_threshold=0.50,
        )

        return [
            {"question": question, "label": label, "paraphrase": phase[0]}
            for phase in para_phases
        ]

    def __call__(self, data: pd.DataFrame | str) -> pd.DataFrame:
        if isinstance(data, str):  # If a file path is provided
            if data.endswith(".csv"):
                data = pd.read_csv(data)
            elif data.endswith(".json"):
                data = pd.read_json(data)
            else:
                raise ValueError(f"Unsupported file format for: {data}")
        elif not isinstance(data, pd.DataFrame):
            raise ValueError(
                "Input must be a DataFrame or a valid file path (CSV/JSON)."
            )

            # Ensure the DataFrame contains a 'questions' column
        if "questions" not in data.columns:
            raise ValueError("DataFrame must contain a 'questions' column.")

        exploded_data = pd.DataFrame(
            data.apply(self.generate_paraphase, axis=1).explode().tolist()
        )

        print(exploded_data)

        return exploded_data
