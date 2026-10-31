"""Persistent application configuration."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from PyQt5.QtCore import QCoreApplication, QStandardPaths

from .resources import resource_path


def config_path() -> Path:
    """Return the per-user configuration path."""
    app = QCoreApplication.instance()
    if app is not None:
        directory = Path(QStandardPaths.writableLocation(QStandardPaths.AppConfigLocation))
    else:
        directory = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
        directory /= "TEXTA" / "ScoreEdit"
    return directory / "config.json"


def _read_config(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as config_file:
        data = json.load(config_file)
    if not isinstance(data, dict):
        raise ValueError(f"Configuration must contain a JSON object: {path}")
    return data


def load_config() -> dict[str, Any]:
    """Load packaged defaults and overlay the user's saved settings."""
    defaults = _read_config(resource_path("config.json"))
    path = config_path()
    if path.is_file():
        defaults.update(_read_config(path))
        return defaults

    legacy_path = Path.cwd() / "config.json"
    if legacy_path.is_file() and legacy_path.resolve() != path.resolve():
        defaults.update(_read_config(legacy_path))
        save_config(defaults)
    return defaults


def save_config(config: dict[str, Any]) -> None:
    """Atomically save the user's configuration."""
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as config_file:
            temporary_path = Path(config_file.name)
            json.dump(config, config_file, ensure_ascii=False, indent=2)
            config_file.write("\n")
        temporary_path.replace(path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()
