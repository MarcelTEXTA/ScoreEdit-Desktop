from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget,  QHBoxLayout, QScrollArea
from PyQt5.QtCore import Qt
from .Grid import Grid

class MidiGridEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.grid_size = 20  # Taille de chaque case de la grille (en pixels)
        self.columns = 100  # Nombre de colonnes (représentant le temps)
        self.rows = 36  # Nombre de lignes (représentant les hauteurs de note)
        self.notes = []  # Liste pour stocker les notes ajoutées

        # Layout principal
        main_layout = QVBoxLayout()

        # Créer la grille d'édition
        self.grid_widget = Grid(self.grid_size, self.columns, self.rows)
        # main_layout.addWidget(self.grid_widget)

        scroll_area = QScrollArea()
        scroll_area.setWidget(self.grid_widget)
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        # Boutons pour effacer les notes
        controls_layout = QHBoxLayout()
        self.clear_button = QPushButton(self.tr("Delete notes"))
        self.clear_button.clicked.connect(self.clear_notes)
        controls_layout.addWidget(self.clear_button)

        main_layout.addLayout(controls_layout)

        self.setLayout(main_layout)

    def clear_notes(self):
        """Efface toutes les notes de la grille."""
        self.grid_widget.clear_grid()
