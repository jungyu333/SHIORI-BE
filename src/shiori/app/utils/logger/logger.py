import logging
from logging.handlers import TimedRotatingFileHandler

from shiori.app.utils.log_utils import (get_today_log_file_path,
                                        passes_log_level_filter)
from shiori.app.utils.logger.formatter import ColorFormatter, JsonFormatter


class Logger:
    _logger = None

    @classmethod
    def _init_logger(cls, use_file: bool = True):
        if cls._logger is not None:
            return

        logger = logging.getLogger("service")
        logger.setLevel(logging.DEBUG)
        logger.propagate = False

        if use_file:
            log_file_path = get_today_log_file_path()

            file_handler = TimedRotatingFileHandler(
                filename=log_file_path, when="midnight", encoding="utf-8"
            )
            file_handler.addFilter(
                lambda record: passes_log_level_filter(record.levelname)
            )
            file_handler.setFormatter(JsonFormatter(datefmt="%Y-%m-%dT%H:%M:%S"))
            logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(
            ColorFormatter(
                fmt="%(asctime)s [%(levelname)s] - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        stream_handler.addFilter(
            lambda record: passes_log_level_filter(record.levelname)
        )
        logger.addHandler(stream_handler)

        cls._logger = logger

    @classmethod
    def debug(cls, message: str, use_file: bool = True):
        cls._init_logger(use_file)
        cls._logger.debug(message)

    @classmethod
    def info(cls, message: str, use_file: bool = True):
        cls._init_logger(use_file)
        cls._logger.info(message)

    @classmethod
    def warning(cls, message: str, use_file: bool = True):
        cls._init_logger(use_file)
        cls._logger.warning(message)

    @classmethod
    def error(cls, message: str, use_file: bool = True):
        cls._init_logger(use_file)
        cls._logger.error(message)

    @classmethod
    def exception(cls, message: str, use_file: bool = True):
        cls._init_logger(use_file)
        cls._logger.exception(message)
