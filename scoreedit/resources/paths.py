"""Helpers for resolving resources bundled with the application."""

from pathlib import Path


_RESOURCE_ROOT = Path(__file__).parent


def resource_path(*parts: str) -> Path:
    return _RESOURCE_ROOT.joinpath(*parts)
