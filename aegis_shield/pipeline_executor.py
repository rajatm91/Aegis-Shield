import traceback
from functools import reduce
from typing import Dict

from pandas import DataFrame

from aegis_shield.common.io_utils import read_data, write_data
from aegis_shield.utils.registry import Registry


def execute_step(accumulated_result: DataFrame, step: Dict):
    """
    Execute a single pipeline step
    """

    try:
        func_name = step["task"]
        inputs = step.get("inputs", {})
        outputs = step.get("outputs", {})
        extra_params = step.get("extra_args", {})

        input_data = read_data(inputs.get("source"))
        print(f"Input data : {input_data}")
        task = Registry.get_function(func_name)

        print(
            f"Running step: {step.get('name', 'Unnamed Step')} using function: {func_name}"
        )

        if extra_params:
            result = task(input_data, **extra_params)
        else:
            result = task(input_data)

        print("#" * 30)
        print(result)

        unique_result = result.drop_duplicates()

        if outputs:
            write_data(unique_result, outputs.get("destination"))

        print(f"Step '{step.get('name', 'Unnamed Step')}' completed.")

        return unique_result

    except Exception as e:
        print(f"Error in step '{step.get('name', 'Unnamed Step')}': {e}")
        traceback.print_exc()
        raise RuntimeError(
            f"Pipeline execution stopped due to error in step '{step.get('name')}'."
        )


def run_pipeline(config: Dict):
    """
    Execute a pipeline using reduce with error handling.
    """
    print(f"Executing task: {config['task_name']}")
    try:
        reduce(execute_step, config["pipelines"], None)
        print(f"Task '{config['task_name']}' completed successfully.")
    except RuntimeError as e:
        print(f"Pipeline execution terminated: {e}")
