from pathlib import Path

from PyQt5.QtWidgets import (
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..config import save_config


class FirstWelcomeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Welcome to TEXTA Score Edit"))
        self.resize(420, 260)

        self.selected_theme = "light"
        self.language = "English"
        self.default_directory = str(Path.home() / "Music" / "TextaScores")

        layout = QVBoxLayout(self)
        self.stacked_layout = QStackedWidget(self)
        layout.addWidget(self.stacked_layout)
        self.stacked_layout.addWidget(self.create_language_page())
        self.stacked_layout.addWidget(self.create_theme_page())
        self.stacked_layout.addWidget(self.create_finish_page())

    def create_language_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(
            QLabel(
                self.tr(
                    "Welcome to TEXTA Score Edit. Choose a language to configure "
                    "your local music score editor."
                )
            )
        )
        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "Français"])
        self.language_combo.currentTextChanged.connect(self.set_language)
        layout.addWidget(self.language_combo)
        next_button = QPushButton(self.tr("Next"))
        next_button.clicked.connect(lambda: self.stacked_layout.setCurrentIndex(1))
        layout.addWidget(next_button)
        return page

    def create_theme_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel(self.tr("Choose your default theme:")))
        self.light_button = QRadioButton(self.tr("Light"))
        self.dark_button = QRadioButton(self.tr("Dark"))
        self.light_button.setChecked(True)
        self.light_button.toggled.connect(
            lambda checked: checked and self.set_theme("light")
        )
        self.dark_button.toggled.connect(
            lambda checked: checked and self.set_theme("dark")
        )
        layout.addWidget(self.light_button)
        layout.addWidget(self.dark_button)

        buttons = QHBoxLayout()
        back_button = QPushButton(self.tr("Back"))
        back_button.clicked.connect(lambda: self.stacked_layout.setCurrentIndex(0))
        next_button = QPushButton(self.tr("Next"))
        next_button.clicked.connect(lambda: self.stacked_layout.setCurrentIndex(2))
        buttons.addWidget(back_button)
        buttons.addWidget(next_button)
        layout.addLayout(buttons)
        return page

    def create_finish_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(
            QLabel(
                self.tr(
                    "Your preferences are stored locally. MIDI playback uses your "
                    "system's associated MIDI player; online accounts are not required."
                )
            )
        )
        buttons = QHBoxLayout()
        back_button = QPushButton(self.tr("Back"))
        back_button.clicked.connect(lambda: self.stacked_layout.setCurrentIndex(1))
        finish_button = QPushButton(self.tr("Finish"))
        finish_button.clicked.connect(self.accept)
        buttons.addWidget(back_button)
        buttons.addWidget(finish_button)
        layout.addLayout(buttons)
        return page

    def set_theme(self, theme):
        self.selected_theme = theme

    def set_language(self, language):
        self.language = language

    def accept(self):
        data = {
            "first_open": False,
            "theme": self.selected_theme,
            "language": self.language,
            "default_directory": self.default_directory,
            "default_format": "score",
            "animation": True,
            "midi_tempo": 120,
            "midi_velocity": 96,
            "recent_files": [],
        }
        try:
            save_config(data)
        except OSError as error:
            QMessageBox.critical(self, self.tr("Configuration error"), str(error))
            return
        super().accept()
