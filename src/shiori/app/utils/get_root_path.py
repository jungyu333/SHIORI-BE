from pathlib import Path


def get_root_path(start: Path) -> Path:
    for path in [start] + list(start.parents):
        if (path / "pyproject.toml").exists():
            return path
    raise FileNotFoundError
