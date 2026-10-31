import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QApplication

from scoreedit.app import MainWindow


class MainWindowWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.application = QApplication.instance() or QApplication([])

    def test_save_and_reopen_score(self):
        window = MainWindow()
        canvas = window.score_editor.canvas
        canvas.add_note("noire", QPoint(80, 80))

        with tempfile.TemporaryDirectory() as directory:
            score_path = Path(directory) / "workflow.score"
            window.current_file = score_path
            window.save_file()
            self.assertTrue(score_path.is_file())

            canvas.clear_score()
            window._saved_score = canvas.get_canvas_data()
            with patch("scoreedit.config.save_config"):
                window.open_file(str(score_path))

        self.assertEqual(len(canvas.notes), 1)
        self.assertEqual(canvas.notes[0]["type"], "noire")
        self.assertEqual(window.current_file, score_path)
        window._saved_score = canvas.get_canvas_data()


if __name__ == "__main__":
    unittest.main()
