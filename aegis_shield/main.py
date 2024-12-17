from pathlib import Path

import typer
from utils.config_loader import load_config_with_env_vars

from aegis_shield.pipeline_executor import run_pipeline

app = typer.Typer()


@app.command()
def execute_task(config_file: Path):
    config = load_config_with_env_vars(config_file)
    run_pipeline(config)
    print("Process complete successfully")


if __name__ == "__main__":
    app()
