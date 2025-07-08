import json
import os
from datetime import datetime
from pathlib import Path

import aiofiles

from shiori.app.core.schema import LogResult

BASE_LOG_DIR = Path("log")
BASE_LOG_DIR.mkdir(exist_ok=True)

LEVEL_PRIORITY = {
    "DEBUG": 0,
    "INFO": 1,
    "WARNING": 2,
    "ERROR": 3,
    "EXCEPTION": 3,
    "CRITICAL": 4,
}


def passes_log_level_filter(level: str) -> bool:
    is_debug = os.environ.get("DEBUG", "false").lower() == "true"

    current_log_level = LEVEL_PRIORITY.get(level.upper(), 1)
    min_log_level = 1 if is_debug else 2

    return current_log_level >= min_log_level


def get_log_level_for_request(path: str) -> str:
    if path.startswith(("/admin", "/internal", "/debug")):
        return "DEBUG"
    return "INFO"


def get_log_level_for_response(status_code: int) -> str:
    if status_code >= 500:
        return "ERROR"
    elif status_code >= 400:
        return "WARNING"
    return "INFO"


def get_today_log_file_path() -> Path:
    today = datetime.utcnow().strftime("%Y-%m-%d")
    today_dir = BASE_LOG_DIR / today
    today_dir.mkdir(parents=True, exist_ok=True)
    return today_dir / f"{today}.log"


async def save_log_to_file(log_data: LogResult):
    log_level = log_data.level if log_data.level else "INFO"

    if not passes_log_level_filter(log_level):
        return

    log_file_path = get_today_log_file_path()

    async with aiofiles.open(log_file_path, "a", encoding="utf-8") as f:
        await f.write(json.dumps(log_data.dict(), ensure_ascii=False) + "\n")
