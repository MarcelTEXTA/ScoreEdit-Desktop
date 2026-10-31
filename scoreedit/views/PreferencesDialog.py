from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..config import load_config, save_config
from .PlugInsTab import PluginLoader


class PreferencesDialog(QDialog):
    def __init__(self, parent=None, flags=None):
        if flags is None:
            super().__init__(parent)
        else:
            super().__init__(parent, flags)
        self.config = load_config()
        self.setWindowTitle(self.tr("Preferences"))
        self.setModal(True)

        main_layout = QVBoxLayout(self)
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        self.list_widget = QListWidget()
        self.list_widget.addItems(
            [
                self.tr("General"),
                self.tr("Display"),
                self.tr("MIDI"),
                self.tr("Audio"),
                self.tr("Shortcuts and gestures"),
                self.tr("Plugins"),
            ]
        )
        self.list_widget.setMaximumWidth(300)
        content_layout.addWidget(self.list_widget)

        self.stacked_widget = QStackedWidget()
        scroller = QScrollArea()
        scroller.setWidget(self.stacked_widget)
        scroller.setWidgetResizable(True)
        scroller.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        content_layout.addWidget(scroller)

        self.stacked_widget.addWidget(self.create_general_preferences())
        self.stacked_widget.addWidget(self.create_display_preferences())
        self.stacked_widget.addWidget(self.create_midi_preferences())
        self.stacked_widget.addWidget(self.create_audio_preferences())
        self.stacked_widget.addWidget(self.create_shortcut_preferences())
        self.stacked_widget.addWidget(self.create_plugin_preferences())
        self.list_widget.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)
        self.list_widget.setCurrentRow(0)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        ok_button = QPushButton(self.tr("OK"))
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton(self.tr("Cancel"))
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        main_layout.addLayout(button_layout)

    def create_general_preferences(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        language_group = QGroupBox(self.tr("Languages"))
        language_layout = QVBoxLayout(language_group)
        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "Français"])
        self.language_combo.setCurrentText(self.config.get("language", "English"))
        language_layout.addWidget(self.language_combo)
        layout.addWidget(language_group)

        path_group = QGroupBox(self.tr("Paths"))
        path_layout = QHBoxLayout(path_group)
        self.path_edit = QLineEdit(
            self.config.get("default_directory")
            or str(Path.home() / "Music" / "TextaScores")
        )
        self.path_edit.setPlaceholderText(
            self.tr("Path to the folder where the scores are saved")
        )
        browse_button = QPushButton(self.tr("Browse"))
        browse_button.clicked.connect(self.browse_path)
        path_layout.addWidget(self.path_edit)
        path_layout.addWidget(browse_button)
        layout.addWidget(path_group)
        layout.addStretch()
        return widget

    def create_display_preferences(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.theme_combo = QComboBox()
        self.theme_combo.addItem(self.tr("Light theme"), "light")
        self.theme_combo.addItem(self.tr("Dark theme"), "dark")
        theme_index = self.theme_combo.findData(self.config.get("theme", "light"))
        self.theme_combo.setCurrentIndex(max(theme_index, 0))
        layout.addWidget(self.theme_combo)

        animation_group = QGroupBox(self.tr("Animation"))
        animation_layout = QVBoxLayout(animation_group)
        self.animation_check = QCheckBox(self.tr("Enable animations"))
        self.animation_check.setChecked(self.config.get("animation", True))
        animation_layout.addWidget(self.animation_check)
        layout.addWidget(animation_group)
        layout.addStretch()
        return widget

    def create_shortcut_preferences(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        shortcuts = QListWidget()
        shortcuts.addItems(
            [
                self.tr("Ctrl + N : New"),
                self.tr("Ctrl + O : Open"),
                self.tr("Ctrl + S : Save"),
                self.tr("Ctrl + Q : Quit"),
                self.tr("Ctrl + Z : Undo"),
                self.tr("Ctrl + Y : Redo"),
                self.tr("Ctrl + C : Copy"),
                self.tr("Ctrl + V : Paste"),
                self.tr("Ctrl + X : Cut"),
                self.tr("Ctrl + A : Select all"),
                self.tr("Ctrl + P : Print"),
            ]
        )
        layout.addWidget(shortcuts)
        return widget

    def create_midi_preferences(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.tempo_spin = QSpinBox()
        self.tempo_spin.setRange(20, 300)
        self.tempo_spin.setValue(self.config.get("midi_tempo", 120))
        self.tempo_spin.setSuffix(self.tr(" BPM"))
        tempo_group = QGroupBox(self.tr("Default MIDI tempo"))
        tempo_layout = QVBoxLayout(tempo_group)
        tempo_layout.addWidget(self.tempo_spin)
        layout.addWidget(tempo_group)

        self.velocity_spin = QSpinBox()
        self.velocity_spin.setRange(1, 127)
        self.velocity_spin.setValue(self.config.get("midi_velocity", 96))
        velocity_group = QGroupBox(self.tr("Default MIDI note velocity"))
        velocity_layout = QVBoxLayout(velocity_group)
        velocity_layout.addWidget(self.velocity_spin)
        layout.addWidget(velocity_group)
        layout.addStretch()
        return widget

    def create_audio_preferences(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        label = QLabel(
            self.tr(
                "Score playback opens the exported MIDI preview in your system's "
                "associated MIDI player."
            )
        )
        label.setWordWrap(True)
        layout.addWidget(label)
        layout.addStretch()
        return widget

    def create_plugin_preferences(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.plugin_list = QListWidget()
        self.plugin_loader = PluginLoader()
        try:
            self.plugin_loader.load_plugins()
        except (ImportError, OSError) as error:
            self.plugin_list.addItem(self.tr("Unable to load plug-ins: {error}").format(error=error))
        else:
            for plugin in self.plugin_loader.get_plugins():
                name = getattr(plugin, "name", plugin.__name__.rsplit(".", 1)[-1])
                self.plugin_list.addItem(name)
            if not self.plugin_loader.get_plugins():
                self.plugin_list.addItem(self.tr("No plug-ins are installed."))
        layout.addWidget(self.plugin_list)
        run_button = QPushButton(self.tr("Run selected plug-in"))
        run_button.clicked.connect(self.run_selected_plugin)
        layout.addWidget(run_button)
        return widget

    def run_selected_plugin(self):
        index = self.plugin_list.currentRow()
        plugins = self.plugin_loader.get_plugins()
        if not 0 <= index < len(plugins):
            return
        plugin = plugins[index]
        run = getattr(plugin, "run", None)
        if not callable(run):
            QMessageBox.information(
                self, self.tr("Plug-in"), self.tr("This plug-in has no run action.")
            )
            return
        try:
            parent = self.parentWidget()
            run(parent.window() if parent is not None else None)
        except Exception as error:
            QMessageBox.critical(self, self.tr("Plug-in error"), str(error))

    def browse_path(self):
        directory = QFileDialog.getExistingDirectory(
            self, self.tr("Choose score folder"), self.path_edit.text()
        )
        if directory:
            self.path_edit.setText(directory)

    def accept(self):
        self.config.update(
            {
                "first_open": False,
                "theme": self.theme_combo.currentData(),
                "language": self.language_combo.currentText(),
                "default_directory": self.path_edit.text(),
                "animation": self.animation_check.isChecked(),
                "midi_tempo": self.tempo_spin.value(),
                "midi_velocity": self.velocity_spin.value(),
            }
        )
        try:
            save_config(self.config)
        except OSError as error:
            QMessageBox.critical(self, self.tr("Error"), str(error))
            return
        super().accept()
