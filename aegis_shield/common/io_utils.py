# common/io_utils.py
from pathlib import Path

import pandas as pd
import json

def read_data(source):
    """
    Reads data from the specified source.
    Supports: JSON, CSV, database connections, etc.
    :param source: Dictionary specifying the source type and path/connection details.
    :return: Data as a dictionary or DataFrame.
    """
    source_type = source.get("type")
    path = source.get("path")
    connection_details = source.get("connection")

    if source_type == "json":
        with open(path, "r") as file:
            return json.load(file)
    elif source_type == "csv":
        return pd.read_csv(path)
    elif source_type == "db":
        query = source.get("query")
        return pd.read_sql(query, connection_details)
    else:
        raise ValueError(f"Unsupported source type: {source_type}")

def write_data(data, destination):
    """
    Writes data to the specified destination.
    Supports: JSON, CSV, etc.
    :param data: Data to write (dictionary or DataFrame).
    :param destination: Dictionary specifying the destination type and path.
    """
    destination_type = destination.get("type")
    output_path = Path(destination.get("path"))

    # Ensure the directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if destination_type == "json":
        data.to_json(output_path, orient="records", lines=False, indent=4)
    elif destination_type == "csv":
        if isinstance(data, pd.DataFrame):
            data.to_csv(output_path, index=False)
        else:
            raise ValueError("Data must be a DataFrame to write to CSV.")
    else:
        raise ValueError(f"Unsupported destination type: {destination_type}")
