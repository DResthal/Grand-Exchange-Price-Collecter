# Provide an easy way to setup multiple loggers (only for remaining DRY)
import logging


class CustomLogger:
    def __init__(
        self,
        name: str,
        log_file: str,
        level: int = logging.WARNING,
        formatter=logging.Formatter("%(asctime)s %(levelname)s %(message)s"),
    ):
        self.name = name
        self.log_file = log_file
        self.level = level
        self.formatter = formatter

    def create_logger(self):
        handler = logging.FileHandler(self.log_file)
        handler.setFormatter(self.formatter)
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        logger.addHandler(handler)

        return logger
