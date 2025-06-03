import os
from box.exceptions import BoxValueError
import yaml
from src.Text_Summarizer.logging import logger
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a YAML file and returns the content as a ConfigBox.
    Args:
        path_to_yaml (Path): Path to the YAML file.
    Returns:
        ConfigBox: The content of the YAML file as a ConfigBox.
    Raises:
        ValueError: If the YAML file is empty.
        BoxValueError: If the YAML file is not a valid YAML file.
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e

@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")
        