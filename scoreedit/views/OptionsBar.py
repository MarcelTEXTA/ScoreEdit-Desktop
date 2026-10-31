from pathlib import Path

from PyQt5.QtCore import QPoint, QStandardPaths, QUrl, Qt
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import (
    QInputDialog,
    QMenu,
    QMessageBox,
    QPushButton,
    QShortcut,
    QHBoxLayout,
    QWidget,
)

from .PreferencesDialog import PreferencesDialog
from .PrintDialog import PrintDialog
from ..midi_io import export_midi


class OptionsBar(QWidget):
    def __init__(self, canvas, parent=None, main_window=None):
        super().__init__(parent)
        self.setObjectName("OptionsBar")
        self.canvas = canvas
        self.main_window = main_window
        self._playback_file = None

        assert self.main_window is not None
        
        layout = QHBoxLayout(self)
        self.menu_button = QPushButton(self.tr("Options"), self)
        self.menu_button.clicked.connect(self.show_menu)
        layout.addWidget(self.menu_button)

        self.save_button = QPushButton(self.tr("Save"))
        self.save_button.setShortcut("Ctrl+S")
        self.save_button.clicked.connect(self.save_file)
        layout.addWidget(self.save_button)

        self.open_file_button = QPushButton(self.tr("Open"))
        self.open_file_button.setShortcut("Ctrl+O")
        self.open_file_button.clicked.connect(self.open_file)
        layout.addWidget(self.open_file_button)

        self.new_project_button = QPushButton(self.tr("New project"))
        self.new_project_button.setShortcut("Ctrl+N")
        self.new_project_button.clicked.connect(self.new_project)
        layout.addWidget(self.new_project_button)

        self.print_button = QPushButton(self.tr("Print"))
        self.print_button.setShortcut("Ctrl+P")
        self.print_button.clicked.connect(self.print_score)
        layout.addWidget(self.print_button)
        layout.addStretch()

        help_button = QPushButton(self.tr("Help"))
        help_button.setShortcut("F1")
        help_button.clicked.connect(self.main_window.toggle_help_sidebar)
        layout.addWidget(help_button)
        account_button = QPushButton(self.tr("Account"))
        account_button.clicked.connect(self.main_window.toggle_account_sidebar)
        layout.addWidget(account_button)
        self.play_button = QPushButton(self.tr("Read score"))
        self.play_button.setShortcut("F5")
        self.play_button.clicked.connect(self.ScorePlayer)
        layout.addWidget(self.play_button)
        for key, callback in (
            ("Ctrl+Z", self.canvas.undo),
            ("Ctrl+Y", self.canvas.redo),
            ("Ctrl+X", self.canvas.cut_selected),
            ("Ctrl+C", self.canvas.copy_selected),
            ("Ctrl+V", self.canvas.paste),
            ("Ctrl+A", self.canvas.select_all),
        ):
            shortcut = QShortcut(key, self.main_window)
            shortcut.activated.connect(callback)

    def show_menu(self):
        menu = QMenu(self)

        file_menu = menu.addMenu(self.tr("File"))
        assert file_menu is not None
        file_menu.addAction(self.tr("New project"), self.new_project)
        file_menu.addAction(self.tr("Open score"), self.open_file)
        file_menu.addAction(self.tr("Save"), self.save_file)
        file_menu.addAction(self.tr("Save as"), self.save_at)
        file_menu.addAction(self.tr("Export PDF"), self.export_pdf)
        file_menu.addAction(self.tr("Print score"), self.print_score)
        file_menu.addAction(self.tr("Preferences"), self.preferences)
        file_menu.addSeparator()
        file_menu.addAction(self.tr("Quit"), self.exit_app)

        edit_menu = menu.addMenu(self.tr("Edit"))
        assert edit_menu is not None
        edit_menu.addAction(self.tr("Undo"), self.canvas.undo)
        edit_menu.addAction(self.tr("Redo"), self.canvas.redo)
        edit_menu.addSeparator()
        edit_menu.addAction(self.tr("Cut"), self.canvas.cut_selected)
        edit_menu.addAction(self.tr("Copy"), self.canvas.copy_selected)
        edit_menu.addAction(self.tr("Paste"), self.canvas.paste)
        edit_menu.addAction(self.tr("Select all"), self.canvas.select_all)

        midi_menu = menu.addMenu(self.tr("MIDI"))
        assert midi_menu is not None
        midi_menu.addAction(self.tr("Open MIDI editor"), self.open_midi_editor)
        midi_menu.addAction(self.tr("Import MIDI"), self.import_midi)
        midi_menu.addAction(self.tr("Export MIDI"), self.export_midi)

        score_menu = menu.addMenu(self.tr("Score"))
        assert score_menu is not None
        score_menu.addAction(
            self.tr("Add note"),
            lambda: self.canvas.add_note(self.canvas.note_type, QPoint(100, 100)),
        )
        score_menu.addAction(
            self.tr("Add rest"),
            lambda: self.canvas.add_rest(QPoint(100, 100)),
        )
        score_menu.addAction(
            self.tr("Add chord"),
            lambda: self.canvas.add_chord(QPoint(100, 100)),
        )
        score_menu.addAction(self.tr("Add text"), self.add_text)

        decrypt_menu = menu.addMenu(self.tr("Decrypter"))
        assert decrypt_menu is not None
        for label in (
            "Decrypte audio file",
            "Decrypte MIDI live",
            "Decrypte MIDI file",
            "Decrypte audio recorder",
            "Harmonic analysis",
            "Tonnage analysis",
            "Scan score decryption",
            "Height corrector",
        ):
            decrypt_menu.addAction(self.tr(label))

        help_menu = menu.addMenu(self.tr("Help"))
        assert help_menu is not None
        assert self.main_window is not None
        help_menu.addAction(self.tr("Documentation"), self.main_window.toggle_help_sidebar)
        help_menu.addAction(self.tr("About TEXTA Score Edit"), self.about)
        menu.exec_(self.menu_button.mapToGlobal(self.menu_button.rect().bottomLeft()))

    def open_file(self):
        assert self.main_window is not None
        self.main_window.open_file()

    def new_project(self):
        assert self.main_window is not None
        self.main_window.new_project()

    def save_file(self):
        assert self.main_window is not None
        self.main_window.save_file()

    def save_at(self):
        assert self.main_window is not None
        self.main_window.save_file(save_as=True)

    def print_score(self):
        PrintDialog(self.main_window, canvas=self.canvas).exec_()

    def export_pdf(self):
        dialog = PrintDialog(self.main_window, canvas=self.canvas)
        dialog.export_pdf()

    def ScorePlayer(self):
        if not self.canvas.notes:
            QMessageBox.information(
                self, self.tr("Read score"), self.tr("Add notes before playback.")
            )
            return
        temp_directory = Path(
            QStandardPaths.writableLocation(QStandardPaths.TempLocation)
        )
        temp_directory.mkdir(parents=True, exist_ok=True)
        playback_file = temp_directory / "texta-score-preview.mid"
        notes = []
        for note in self.canvas.notes:
            column = max(0, note["position"].x() // 20)
            pitch = max(
                48,
                min(83, 60 + round((90 - note["position"].y()) / 5)),
            )
            row = 35 - (pitch - 48)
            duration = max(
                1,
                round(self.canvas.get_note_value(note["type"]) * 4),
            )
            if note["type"].startswith("pause_"):
                continue
            notes.append((column, row, duration))
        try:
            assert self.main_window is not None
            export_midi(
                playback_file,
                notes,
                rows=36,
                tempo_bpm=self.main_window.config.get("midi_tempo", 120),
                velocity=self.main_window.config.get("midi_velocity", 96),
            )
        except (OSError, ValueError) as error:
            QMessageBox.critical(self, self.tr("Playback error"), str(error))
            return
        self._playback_file = playback_file
        if not QDesktopServices.openUrl(QUrl.fromLocalFile(str(playback_file))):
            QMessageBox.warning(
                self,
                self.tr("Playback unavailable"),
                self.tr("No MIDI player is associated with this file: {path}").format(
                    path=playback_file
                ),
            )

    def preferences(self):
        dialog = PreferencesDialog(self)
        if dialog.exec_() == PreferencesDialog.Accepted:
            assert self.main_window is not None
            self.main_window.load()

    def add_text(self):
        text, accepted = QInputDialog.getText(
            self, self.tr("Add text"), self.tr("Text")
        )
        if accepted:
            self.canvas.add_text(text, QPoint(100, 120))

    def open_midi_editor(self):
        assert self.main_window is not None
        self.main_window.tabs.setCurrentIndex(1)

    def import_midi(self):
        self.open_midi_editor()
        assert self.main_window is not None
        self.main_window.tabs.widget(1).midi_grid_editor.import_file()

    def export_midi(self):
        self.open_midi_editor()
        assert self.main_window is not None
        self.main_window.tabs.widget(1).midi_grid_editor.export_file()

    def exit_app(self):
        assert self.main_window is not None
        self.main_window.close()

    def annule(self):
        self.canvas.undo()

    def about(self):
        QMessageBox.about(
            self,
            self.tr("About TEXTA Score Edit"),
            self.tr("TEXTA Score Edit — desktop music score editor"),
        )
