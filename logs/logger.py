import json
import logging
import logging.config
from pathlib import Path


def setup_logging() -> None:
    config_path = Path(__file__).with_name("logging_config.json")
    with config_path.open("r", encoding="utf-8") as f:
        config = json.load(f)
    logging.config.dictConfig(config)


logger = logging.getLogger("aiomax")


