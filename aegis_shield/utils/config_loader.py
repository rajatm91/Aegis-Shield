import os
from pathlib import Path

import yaml

# class EnvVarLoader(yaml.SafeLoader):
#     """
#     Custom YAML loader that resolves environment variables in the format ${ENV_VAR}.
#     """
#
#     def __init__(self, stream):
#         super().__init__(stream)
#
#         # Add a custom resolver for environment variables
#         self.add_implicit_resolver(
#             "!env",  # Custom tag for environment variables
#             pattern=r"\$\{([^}]+)\}",  # Matches ${VAR_NAME}
#             first=None,
#         )
#         self.add_constructor("!env", self._env_var_constructor)
#
#     @staticmethod
#     def _env_var_constructor(loader, node):
#         """
#         Resolve the environment variable from the !env tag or ${VAR_NAME} format.
#         """
#         value = loader.construct_scalar(node)
#         env_var = value.strip("${}")
#         resolved_value = os.getenv(env_var)
#
#         if resolved_value is None:
#             raise ValueError(f"Environment variable '{env_var}' is not set.")
#         return resolved_value

def load_config_with_env_vars(config_path: Path):
    """
    Load a YAML configuration file and resolve environment variables.
    :param config_path: Path to the YAML file.
    :return: Parsed YAML with environment variables resolved.
    """
    with open(config_path, "r") as file:
        return yaml.safe_load(file)
