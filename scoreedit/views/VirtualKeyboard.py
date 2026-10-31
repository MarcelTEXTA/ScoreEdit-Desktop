from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QHBoxLayout

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
        keys = ['C', 'D', 'E', 'F', 'G', 'A', 'B']  # Notes de base
        self.buttons = {}  # Dictionnaire pour stocker les boutons

        for key in keys:
            btn = QPushButton(key)
            btn.setFixedSize(50, 100)
            btn.setStyleSheet("background-color: white;")  # Blanche pour les touches naturelles

            # Connecter chaque bouton à la méthode qui gère les clics
            btn.clicked.connect(lambda checked, k=key: self.on_key_pressed(k))

            # Ajouter le bouton au layout du clavier
            self.keyboard_layout.addWidget(btn)
            self.buttons[key] = btn

    def on_key_pressed(self, key):
        """Gère l'ajout d'une note à la partition lorsqu'une touche est pressée."""
        # self.parentWidget().add_note_to_score(key)
        pass