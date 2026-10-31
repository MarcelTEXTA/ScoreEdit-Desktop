from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import QPoint

class VirtualKeyboard(QWidget):
    def __init__(self, parent, main_window=None):
        super().__init__(parent)
        self.main_window = main_window if main_window is not None else parent

        # Layout principal
        layout = QVBoxLayout()

        # Clavier virtuel (section des touches de piano)
        self.keyboard_layout = QHBoxLayout()

        # Créer les touches du clavier (do, ré, mi, etc.)
        self.create_keyboard()

        # Ajouter le clavier virtuel au layout principal
        layout.addLayout(self.keyboard_layout)

        self.setLayout(layout)

    def create_keyboard(self):
        """Crée des boutons représentant les touches d'un piano."""
        keys = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        self.buttons = {}  # Dictionnaire pour stocker les boutons

        black_keys = {"C#", "D#", "F#", "G#", "A#"}
        for key in keys:
            btn = QPushButton(key)
            btn.setFixedSize(38, 72 if key in black_keys else 100)
            btn.setStyleSheet(
                "background-color: #333; color: white;"
                if key in black_keys
                else "background-color: white; color: black;"
            )

            # Connecter chaque bouton à la méthode qui gère les clics
            btn.clicked.connect(lambda checked, k=key: self.on_key_pressed(k))

            # Ajouter le bouton au layout du clavier
            self.keyboard_layout.addWidget(btn)
            self.buttons[key] = btn

    def on_key_pressed(self, key):
        """Gère l'ajout d'une note à la partition lorsqu'une touche est pressée."""
        target = self.main_window
        if hasattr(target, "add_note_to_score"):
            target.add_note_to_score(key)