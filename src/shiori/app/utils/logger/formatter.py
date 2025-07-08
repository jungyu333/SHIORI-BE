import json
import logging
from datetime import datetime

from shiori.app.core.schema import LogResult


class ColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[94m",
        "INFO": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "CRITICAL": "\033[91m",
        "RESET": "\033[0m",
    }

    def format(self, record):
        color = self.COLORS.get(record.levelname, "")
        reset = self.COLORS["RESET"]
        msg = super().format(record)
        return f"{color}{msg}{reset}"


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.fromtimestamp(record.created).isoformat()

        log_result = LogResult(
            timestamp=timestamp,
            level=record.levelname,
            type="service",
            message=record.getMessage(),
        )

        return json.dumps(log_result.dict(), ensure_ascii=False)
