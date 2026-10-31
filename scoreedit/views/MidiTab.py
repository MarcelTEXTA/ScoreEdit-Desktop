from PyQt5.QtWidgets import QVBoxLayout, QWidget
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

        self.setLayout(main_layout)
