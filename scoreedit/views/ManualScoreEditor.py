from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QPoint
from .Canvas import Canvas
from .VirtualKeyboard import VirtualKeyboard

class ManualScoreEditor(QWidget):
    def __init__(self, main_window=None):
        super().__init__(main_window if isinstance(main_window, QWidget) else None)

        self.setObjectName("TabItem")

        # Layout principal
        main_layout = QVBoxLayout()

        self.main_window = main_window
        if main_window is not None and hasattr(main_window, "score_editor"):
            self.canvas = main_window.score_editor.canvas
            self.shares_score_canvas = True
        else:
            self.canvas = Canvas()
            self.shares_score_canvas = False

        # Clavier virtuel pour saisir les notes
        self.virtual_keyboard = VirtualKeyboard(self, main_window=self)

        # Ajouter les widgets au layout
        main_layout.addWidget(self.virtual_keyboard)
        if self.shares_score_canvas:
            main_layout.addWidget(
                QLabel(self.tr("Keyboard notes are added to the score canvas."))
            )
        else:
            main_layout.addWidget(self.canvas)

        self.setLayout(main_layout)

    def add_note_to_score(self, note):
        """Add a virtual-keyboard pitch to the shared score canvas."""
        pitch_order = {
            "C": 0,
            "C#": 1,
            "D": 2,
            "D#": 3,
            "E": 4,
            "F": 5,
            "F#": 6,
            "G": 7,
            "G#": 8,
            "A": 9,
            "A#": 10,
            "B": 11,
        }
        if note not in pitch_order:
            return
        x = max(
            100,
            self.canvas.notes[-1]["position"].x() + 20 if self.canvas.notes else 100,
        )
        y = 100 - pitch_order[note] * 5
        self.canvas.add_note(self.canvas.note_type, QPoint(x, y))
