from PyQt5.QtWidgets import QFileDialog, QMessageBox, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QScrollArea
from .Grid import Grid
from ..config import load_config
from ..midi_io import export_midi, import_midi

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
        self.grid_widget.setToolTip(
            self.tr("Click to add a note, drag its right edge to change its length, right-click to delete.")
        )
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

        self.import_button = QPushButton(self.tr("Import MIDI"))
        self.import_button.clicked.connect(self.import_file)
        controls_layout.addWidget(self.import_button)
        self.export_button = QPushButton(self.tr("Export MIDI"))
        self.export_button.clicked.connect(self.export_file)
        controls_layout.addWidget(self.export_button)

        main_layout.addLayout(controls_layout)

        self.setLayout(main_layout)

    def clear_notes(self):
        """Efface toutes les notes de la grille."""
        self.grid_widget.clear_grid()

    def import_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, self.tr("Import MIDI"), "", self.tr("MIDI files (*.mid *.midi)")
        )
        if not file_name:
            return
        try:
            notes = import_midi(file_name, self.grid_widget.columns, self.grid_widget.rows)
        except (OSError, ValueError) as error:
            QMessageBox.critical(self, self.tr("MIDI import error"), str(error))
            return
        self.grid_widget.set_notes(notes)

    def export_file(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, self.tr("Export MIDI"), "", self.tr("MIDI files (*.mid)")
        )
        if not file_name:
            return
        if not file_name.lower().endswith((".mid", ".midi")):
            file_name += ".mid"
        try:
            config = load_config()
            export_midi(
                file_name,
                self.grid_widget.get_notes(),
                self.grid_widget.rows,
                tempo_bpm=config.get("midi_tempo", 120),
                velocity=config.get("midi_velocity", 96),
            )
        except (OSError, ValueError) as error:
            QMessageBox.critical(self, self.tr("MIDI export error"), str(error))
