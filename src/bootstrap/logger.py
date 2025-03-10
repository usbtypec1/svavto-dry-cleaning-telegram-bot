import json
import pathlib
import logging.config
from typing import Final


LOGGING_CONFIG_FILE_PATH: Final[pathlib.Path] = (
        pathlib.Path(__file__).parent.parent.parent
        / 'logging_config.json'
)


def load_logging_config_from_file() -> dict:
    config_json = LOGGING_CONFIG_FILE_PATH.read_text(encoding='utf-8')
    return json.loads(config_json)


def setup_logging():
    config = load_logging_config_from_file()
    logging.config.dictConfig(config)
