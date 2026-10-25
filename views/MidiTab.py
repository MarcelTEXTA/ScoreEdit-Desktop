from PyQt5.QtWidgets import QVBoxLayout, QWidget, QScrollArea
from PyQt5.QtCore import Qt
from .MidiGridEditor import MidiGridEditor

class MidiTab(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("TabItem")

        # Layout principal
        main_layout = QVBoxLayout()

        # Ajouter l'éditeur MIDI sur grille
        self.midi_grid_editor = MidiGridEditor()
        main_layout.addWidget(self.midi_grid_editor)

        # scroll_area = QScrollArea()
        # scroll_area.setWidget(self.midi_grid_editor)
        # scroll_area.setWidgetResizable(True)
        # main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)
