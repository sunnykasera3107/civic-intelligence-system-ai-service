import json
import logging
import os

import yaml

_logger = logging.getLogger(__name__)


def load_json(relative_path: str) -> dict:
    base_path = os.getcwd() + '/'
    full_path = os.path.join(base_path, relative_path)
    _logger.info(f"Reading file: {full_path}")
    try:
        with open(full_path, "r") as file:
            return json.load(file)
    except Exception as e:
        _logger.error(f"Exception: {str(e)}")


def load_yaml(relative_path: str) -> dict:
    base_path = os.getcwd() + '/'
    full_path = os.path.join(base_path, relative_path)
    _logger.info(f"Reading file: {full_path}")
    try:
        with open(full_path, "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        _logger.error(f"Exception: {str(e)}")