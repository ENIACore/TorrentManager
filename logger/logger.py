import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import ClassVar
from config.settings import MANAGER_PATH


class Logger:
    """Thread-safe singleton logger with file and console output."""
    
    _instance: ClassVar[Logger | None] = None
    _initialized: ClassVar[bool] = False
    
    def __new__(cls, manager_path: Path | None = None) -> Logger:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, manager_path: Path | None = None) -> None:

        if Logger._initialized:
            return
        
        Logger._initialized = True

        # Path that TorrentManager program can use for files/logs/etc
        self.manager_path = manager_path or Path(MANAGER_PATH)
        self.log_dir = self.manager_path / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._logger = self._create_logger(timestamp)

    def _create_logger(self, timestamp: str) -> logging.Logger:
        logger = logging.getLogger(f"torrent_manager_{timestamp}")
        logger.setLevel(logging.DEBUG)
        logger.handlers.clear()  # Prevent duplicate handlers on re-init
        
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # File handler for all logs (INFO and above)
        file_handler = logging.FileHandler(
            self.log_dir / f"{timestamp}.log",
            encoding="utf-8"
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Separate file handler for errors only
        error_handler = logging.FileHandler(
            self.log_dir / f"{timestamp}.error.log",
            encoding="utf-8"
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        logger.addHandler(error_handler)
        
        # Console handler for DEBUG messages only
        debug_console_handler = logging.StreamHandler(sys.stdout)
        debug_console_handler.setLevel(logging.DEBUG)
        debug_console_handler.addFilter(lambda record: record.levelno == logging.DEBUG)
        debug_console_handler.setFormatter(formatter)
        logger.addHandler(debug_console_handler)
        
        # Console handler for INFO and above (excluding DEBUG)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.addFilter(lambda record: record.levelno >= logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def debug(self, message: str) -> None:
        self._logger.debug(message)
    
    def info(self, message: str) -> None:
        self._logger.info(message)
    
    def warning(self, message: str) -> None:
        self._logger.warning(message)
    
    def error(self, message: str, exc_info: bool = False) -> None:
        self._logger.error(message, exc_info=exc_info)
    
    def critical(self, message: str, exc_info: bool = False) -> None:
        self._logger.critical(message, exc_info=exc_info)

    @classmethod
    def get_logger(cls, manager_path: Path | None = None) -> 'Logger':
        """Get the singleton Logger instance."""
        return cls(manager_path)
    
    @classmethod
    def reset(cls) -> None:
        if cls._instance and hasattr(cls._instance, "_logger"):
            for handler in cls._instance._logger.handlers[:]:
                handler.close()
                cls._instance._logger.removeHandler(handler)
        cls._instance = None
