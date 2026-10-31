"""Read and write native score files."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
from typing import Any


def _decode_legacy_score(content: str) -> dict[str, Any]:
    decoder = json.JSONDecoder()
    objects: list[Any] = []
    position = 0
    while position < len(content):
        while position < len(content) and content[position].isspace():
            position += 1
        if position == len(content):
            break
        value, position = decoder.raw_decode(content, position)
        objects.append(value)

    if objects and all(
        isinstance(item, dict) and "position" in item and "type" in item
        for item in objects
    ):
        return {
            "clef": "sol",
            "accidentals": [],
            "time_signature": [4, 4],
            "measures": [
                {
                    "position": {"x": 50, "y": 50},
                    "notes": objects,
                }
            ],
        }
    raise ValueError("The file is not a supported TEXTA Score Edit score.")


def load_score(path: str | Path) -> dict[str, Any]:
    score_path = Path(path)
    content = score_path.read_text(encoding="utf-8")
    try:
        score = json.loads(content)
    except json.JSONDecodeError:
        score = _decode_legacy_score(content)

    if not isinstance(score, dict) or not isinstance(score.get("measures"), list):
        raise ValueError("The score file must contain a measures list.")
    return score


def save_score(path: str | Path, score: dict[str, Any]) -> None:
    score_path = Path(path)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=score_path.parent,
            prefix=f".{score_path.name}.",
            suffix=".tmp",
            delete=False,
        ) as score_file:
            temporary_path = Path(score_file.name)
            json.dump(score, score_file, ensure_ascii=False, indent=2)
            score_file.write("\n")
        temporary_path.replace(score_path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()
