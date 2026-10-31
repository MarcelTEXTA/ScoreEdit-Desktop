from PyQt5.QtWidgets import QVBoxLayout, QWidget
from .Canvas import Canvas
from .VirtualKeyboard import VirtualKeyboard

class ManualScoreEditor(QWidget):
    def __init__(self, main_window=None):
        super().__init__()

        self.setObjectName("TabItem")

        main_window = main_window

        # Layout principal
        main_layout = QVBoxLayout()

        # Zone d'édition de la partition
        self.canvas = Canvas()

        # Clavier virtuel pour saisir les notes
        self.virtual_keyboard = VirtualKeyboard(self, main_window=self)

        # Ajouter les widgets au layout
        main_layout.addWidget(self.virtual_keyboard)
        main_layout.addWidget(self.canvas)

        self.setLayout(main_layout)

    def add_note_to_score(self, note):
        """Ajoute la note correspondante à la partition."""
        # Par exemple, la position pourrait être calculée automatiquement
        # en fonction de la dernière note ou une position par défaut
        self.canvas.add_note(note)
