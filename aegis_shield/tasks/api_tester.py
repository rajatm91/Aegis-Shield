# aegis_shield/tasks/api_uploader.py

import pandas as pd
import requests

from aegis_shield.utils.registry import Registry


@Registry.register("service_validator")
class ServiceValidator:
    """
    Task to read input data, make API calls with static and dynamic payloads, and capture the output.
    """

    def __init__(self):
        """
        Initialize the API Uploader.
        """
        print("Initializing API Uploader...")

    def make_api_call(self, row: pd.Series, api_details: dict) -> dict:
        """
        Makes an API call for a given row of data.

        :param row: Single row of input data.
        :param api_details: Dictionary with API details (URL, request type, payload).
        :return: API response or error details.
        """
        url = api_details.get("url")
        request_type = api_details.get("request_type", "POST").upper()
        payload_template = api_details.get("payload", {})

        # Construct the payload by combining static values and dynamic row values
        payload = {
            key: (row[val] if isinstance(val, str) and val in row else val)
            for key, val in payload_template.items()
        }

        print(f"Making {request_type} request to {url} with payload: {payload}")

        try:
            if request_type == "POST":
                response = requests.post(url, json=payload)
            elif request_type == "GET":
                response = requests.get(url, params=payload)
            else:
                raise ValueError(f"Unsupported request type: {request_type}")

            response.raise_for_status()  # Raise an error for HTTP errors
            return {"status": "success", "response": response.json()}
        except requests.RequestException as e:
            print(f"API call failed: {e}")
            return {"status": "error", "error": str(e)}

    def process_row(self, row: pd.Series, api_details: dict) -> dict:
        """
        Processes a single row by making an API call.

        :param row: Row of input data as a pandas Series.
        :param api_details: API details from the configuration.
        :return: Result with original row and API response.
        """
        result = self.make_api_call(row, api_details)
        return {**row.to_dict(), **result}

    def __call__(self, data: pd.DataFrame | str, **kwargs) -> pd.DataFrame:
        """
        Entry point to process the input data, make API calls, and capture results.

        :param data: Input file path (CSV/JSON) or pandas DataFrame.
        :param kwargs: Additional parameters like 'api_details'.
        :return: Processed DataFrame with API responses.
        """
        api_details = kwargs.get("extra_args", {})

        # Step 1: Read Input Data
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

        # Step 2: Ensure required columns exist
        required_columns = set(api_details.get("required_columns", []))
        if not required_columns.issubset(data.columns):
            raise ValueError(
                f"Input data is missing required columns: {required_columns - set(data.columns)}"
            )

        # Step 3: Process Each Row
        results = pd.DataFrame(
            data.apply(self.process_row, axis=1, api_details=api_details).tolist()
        )

        print("API upload task completed successfully.")
        print(results)

        return results
