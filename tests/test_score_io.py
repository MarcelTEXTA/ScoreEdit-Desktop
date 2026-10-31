import json
import tempfile
import unittest
from pathlib import Path

from scoreedit.midi_io import export_midi, import_midi
from scoreedit.score_io import load_score, save_score


class ScoreIOTests(unittest.TestCase):
    def test_score_round_trip(self):
        score = {
            "clef": "sol",
            "accidentals": [],
            "time_signature": [4, 4],
            "measures": [
                {
                    "position": {"x": 50, "y": 50},
                    "notes": [
                        {"position": {"x": 60, "y": 80}, "type": "noire"}
                    ],
                }
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "score.score"
            save_score(path, score)
            self.assertEqual(load_score(path), score)

    def test_loads_legacy_concatenated_notes(self):
        notes = [
            {"position": {"x": 60, "y": 80}, "type": "noire"},
            {"position": {"x": 80, "y": 70}, "type": "blanche"},
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "legacy.score"
            path.write_text("".join(json.dumps(note) for note in notes), encoding="utf-8")
            score = load_score(path)
        self.assertEqual(score["measures"][0]["notes"], notes)

    def test_rejects_invalid_score_shape(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.score"
            path.write_text('{"notes": []}', encoding="utf-8")
            with self.assertRaises(ValueError):
                load_score(path)

    def test_midi_round_trip(self):
        notes = [(0, 10, 2), (4, 12, 1), (12, 2, 4)]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "notes.mid"
            export_midi(path, notes, rows=36)
            self.assertEqual(import_midi(path, columns=100, rows=36), notes)


if __name__ == "__main__":
    unittest.main()
