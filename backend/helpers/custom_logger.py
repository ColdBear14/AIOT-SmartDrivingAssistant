import logging

from rich.console import Console
from rich.logging import RichHandler

class CustomLogger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.init_logger()
        return cls._instance

    def init_logger(self):
        if not hasattr(self, 'log'):
            self.console = Console()

            logging.basicConfig(
                level=logging.DEBUG,
                format="%(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                handlers=[RichHandler(rich_tracebacks=True)]
            )

            self.log = logging.getLogger()

    def get_logger(self):
        return self.log

# logger = CustomLogger().get_logger()
# logger.info("This is a test message")
# logger.debug("This is a debug message")
# logger.warning("This is a warning message")
# logger.error("This is an error message")
# logger.critical("This is a critical message")
