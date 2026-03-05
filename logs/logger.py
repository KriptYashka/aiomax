import json
import logging
import logging.config
from pathlib import Path

class Logger:
    logger: logging.Logger = None

    @classmethod
    def setup_logging(cls) -> None:
        if not cls.logger:
            cls.logger = logging.getLogger("aiomax")
        config_path = Path(__file__).with_name("logging_config.json")
        with config_path.open("r", encoding="utf-8") as f:
            config = json.load(f)
        logging.config.dictConfig(config)





