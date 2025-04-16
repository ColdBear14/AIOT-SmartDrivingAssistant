import logging

from rich.console import Console
from rich.logging import RichHandler

class CustomLogger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._init_logger()
        return cls._instance

    def _init_logger(self):
        if not hasattr(self, 'log'):
            self.console = Console()

            logging.basicConfig(
                level=logging.DEBUG,
                format="%(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                handlers=[RichHandler(rich_tracebacks=True)]
            )

            logging.getLogger("rich").setLevel(logging.WARNING)
            logging.getLogger("concurrent").setLevel(logging.WARNING)
            logging.getLogger("asyncio").setLevel(logging.WARNING)
            logging.getLogger("fastapi").setLevel(logging.WARNING)
            logging.getLogger("passlib").setLevel(logging.WARNING)
            logging.getLogger("rich").setLevel(logging.WARNING)
            logging.getLogger("pymongo").setLevel(logging.WARNING)

            self.log = logging.getLogger()

    def _get_logger(self):
        return CustomLogger()._instance.log
