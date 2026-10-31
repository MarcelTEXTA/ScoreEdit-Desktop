import os
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtWidgets import QApplication

from scoreedit.views.Canvas import Canvas
from scoreedit.views.Grid import Grid


class CanvasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.application = QApplication.instance() or QApplication([])

    def test_note_split_undo_redo(self):
        canvas = Canvas()
        position = QPoint(80, 80)
        canvas.add_note("ronde", position)
        canvas.cut_note_at_position(position)
        self.assertEqual([note["type"] for note in canvas.notes], ["blanche", "blanche"])
        canvas.undo()
        self.assertEqual([note["type"] for note in canvas.notes], ["ronde"])
        canvas.redo()
        self.assertEqual([note["type"] for note in canvas.notes], ["blanche", "blanche"])

    def test_canvas_data_round_trip_includes_annotations(self):
        canvas = Canvas()
        canvas.add_note("noire", QPoint(80, 80))
        canvas.add_text("Allegro", QPoint(70, 40))
        data = canvas.get_canvas_data()

        restored = Canvas()
        restored.load_canvas_data(data)
        self.assertEqual(restored.get_canvas_data(), data)

    def test_piano_roll_round_trip_preserves_note_lengths(self):
        grid = Grid(20, 100, 36)
        notes = [(0, 10, 4), (8, 12, 1)]
        grid.set_notes(notes)
        self.assertEqual(grid.get_notes(), notes)

    def test_note_grid_slot_count_uses_note_value_and_time_signature(self):
        canvas = Canvas()
        self.assertEqual(canvas._note_slots_per_measure("noire"), 4)
        self.assertEqual(canvas._note_slots_per_measure("croche"), 8)

        canvas.set_time_signature(3, 8)
        self.assertEqual(canvas._note_slots_per_measure("croche"), 3)
        self.assertEqual(canvas._note_slots_per_measure("doubleCroche"), 6)

    def test_note_positions_snap_to_rhythm_and_staff_steps(self):
        canvas = Canvas()
        note_positions, _ = canvas._note_grid(0, "noire")
        self.assertEqual(
            canvas._snap_note_x(note_positions[2] + 2, 0, "noire"),
            note_positions[2],
        )
        self.assertEqual(canvas.get_closest_line(83, 50), 85)

    def test_editing_tool_displays_the_rhythm_grid(self):
        canvas = Canvas()
        hidden_grid = QImage(250, 120, QImage.Format_ARGB32)
        hidden_grid.fill(0xFFFFFFFF)
        painter = QPainter(hidden_grid)
        canvas.draw_staff(painter, 50, 50)
        painter.end()

        canvas.set_tool("insertion")
        visible_grid = QImage(250, 120, QImage.Format_ARGB32)
        visible_grid.fill(0xFFFFFFFF)
        painter = QPainter(visible_grid)
        canvas.draw_staff(painter, 50, 50)
        painter.end()

        self.assertEqual(hidden_grid.pixelColor(50, 55).red(), 255)
        self.assertLess(visible_grid.pixelColor(50, 55).red(), 255)

    def test_low_treble_note_draws_a_ledger_line(self):
        canvas = Canvas()
        canvas.notes = [{"position": QPoint(120, 100), "type": "noire"}]
        image = QImage(250, 140, QImage.Format_ARGB32)
        image.fill(0xFFFFFFFF)

        painter = QPainter(image)
        canvas.draw_notes(painter)
        painter.end()

        self.assertEqual(image.pixelColor(110, 100).red(), 0)


if __name__ == "__main__":
    unittest.main()
