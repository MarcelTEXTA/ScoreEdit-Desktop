"""Point d'entrée avec la fenêtre principale"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from PyQt5.QtCore import QPoint, QPropertyAnimation, QTranslator, QUrl, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from .config import config_path, load_config
from .resources import resource_path
from .score_io import load_score, save_score
from .views import FirstWelcomeDialog, OptionsBar, ScoreEditor, Sidebar, Tabs, WelcomeDialog


LOGGER = logging.getLogger(__name__)
THEMES = {
    "light": "style.css",
    "dark": "style2.css",
}
TRANSLATIONS = {
    "fr": "fr_FR.qm",
    "français": "fr_FR.qm",
}


class MainWindow(QMainWindow):
    def __init__(self, main_window: QMainWindow | None = None):
        super().__init__(main_window)
        self.setWindowTitle(self.tr("TEXTA Score Edit"))
        self.setWindowIcon(QIcon(str(resource_path("IconApp", "app", "app_icon.png"))))
        self.current_file: Path | None = None
        self.config = load_config()
        self.translator: QTranslator | None = None

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        content_layout = QHBoxLayout()
        right_layout = QVBoxLayout()
        self.score_editor = ScoreEditor.ScoreEditor()
        self.sidebar = Sidebar.Sidebar(self.score_editor.canvas)
        content_layout.addWidget(self.sidebar)
        self.tabs = Tabs.Tabs(self, main_window=self)
        self._saved_score = self.score_editor.canvas.get_canvas_data()

        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(self.score_editor)
        splitter.addWidget(self.tabs)
        splitter.setSizes([600, 200])
        right_layout.addWidget(splitter)
        content_layout.addLayout(right_layout)

        self.h_sidebar = QWebEngineView()
        self.h_sidebar.setFixedWidth(350)
        self.h_sidebar.hide()
        content_layout.addWidget(self.h_sidebar)

        self.title_bar = OptionsBar.OptionsBar(
            self.score_editor.canvas,
            main_window=self,
        )
        main_layout.addWidget(self.title_bar)
        main_layout.addLayout(content_layout)

        self.init_animation()

    def load(self) -> None:
        """Appliquer les tests"""
        self.config = load_config()
        theme_name = str(self.config.get("theme", "light")).lower()
        theme_file = THEMES.get(theme_name)
        if theme_file is None:
            LOGGER.warning("Theme %r is unavailable; using the light theme.", theme_name)
            theme_file = THEMES["light"]
        self.setStyleSheet(resource_path("styles", theme_file).read_text(encoding="utf-8"))
        self.apply_language(str(self.config.get("language", "en")))
        self.init_animation()

    def apply_language(self, language: str) -> None:
        app = QApplication.instance()
        if app is None:
            raise RuntimeError("A QApplication must exist before loading translations.")

        translation_file = TRANSLATIONS.get(language.strip().lower())
        if translation_file is None:
            if language.strip().lower() not in {"en", "english"}:
                LOGGER.warning("No translation is bundled for language %r.", language)
            if self.translator is not None:
                app.removeTranslator(self.translator)
                self.translator = None
            return

        translator = QTranslator(self)
        translation_path = resource_path("locales", translation_file)
        if not translator.load(str(translation_path)):
            LOGGER.warning("Unable to load translation file: %s", translation_path)
            return

        if self.translator is not None:
            app.removeTranslator(self.translator)
        self.translator = translator
        app.installTranslator(translator)

    def first_open(self) -> bool:
        if config_path().is_file():
            return True
        dialog = FirstWelcomeDialog.FirstWelcomeDialog(self)
        return dialog.exec_() == QDialog.Accepted

    def OpenApp(self, score_path: str | None = None) -> None:
        if score_path is not None:
            self.open_file(score_path)
            return

        welcome_dialog = WelcomeDialog.WelcomeDialog(self)
        if (
            welcome_dialog.exec_() == QDialog.Accepted
            and welcome_dialog.selected_file
        ):
            self.open_file(welcome_dialog.selected_file)

    def toggle_help_sidebar(self) -> None:
        self._toggle_sidebar("help.html")

    def toggle_account_sidebar(self) -> None:
        self._toggle_sidebar("account.html")

    def toggle_acount_sidebar(self) -> None:
        self.toggle_account_sidebar()

    def _toggle_sidebar(self, page: str) -> None:
        page_path = resource_path("url", page)
        page_url = QUrl.fromLocalFile(str(page_path))
        if self.h_sidebar.isVisible():
            self.h_sidebar.hide()
        else:
            if self.h_sidebar.url() != page_url:
                self.h_sidebar.setUrl(page_url)
            self.h_sidebar.show()

    def open_file(self, file_path: str | None = None) -> None:
        if file_path is None:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                self.tr("Open file"),
                str(self.config.get("default_directory", "")),
                self.tr("TEXTA scores (*.score)"),
            )
        if not file_path:
            return

        path = Path(file_path)
        if path.suffix.lower() not in {".score"}:
            QMessageBox.warning(
                self,
                self.tr("Unsupported file"),
                self.tr("Only TEXTA score files are supported at this time. Try type .score."),
            )
            return
        if not self.confirm_unsaved_changes():
            return

        try:
            score = load_score(path)
            self.score_editor.canvas.load_canvas_data(score)
        except (OSError, ValueError, TypeError) as error:
            LOGGER.exception("Unable to open score file %s", path)
            QMessageBox.critical(self, self.tr("Open error"), str(error))
            return

        self.current_file = path
        self._saved_score = self.score_editor.canvas.get_canvas_data()
        recent_files = self.config.get("recent_files", [])
        if not isinstance(recent_files, list):
            recent_files = []
        self.config["recent_files"] = [
            str(path),
            *[item for item in recent_files if item != str(path)],
        ][:10]
        try:
            from .config import save_config

            save_config(self.config)
        except OSError:
            LOGGER.exception("Unable to save recent score history.")
        self.setWindowTitle(f"{self.tr('TEXTA Score Edit')} — {path.name}")

    def save_file(self, save_as: bool = False) -> None:
        path = None if save_as else self.current_file
        if path is None:
            selected_path, _ = QFileDialog.getSaveFileName(
                self,
                self.tr("Save score"),
                str(self.config.get("default_directory", "")),
                self.tr("TEXTA scores (*.score)"),
            )
            if not selected_path:
                return
            path = Path(selected_path)
            if path.suffix.lower() != ".score":
                path = path.with_suffix(".score")

        try:
            save_score(path, self.score_editor.canvas.get_canvas_data())
        except OSError as error:
            LOGGER.exception("Unable to save score file %s", path)
            QMessageBox.critical(self, self.tr("Save error"), str(error))
            return

        self.current_file = path
        self._saved_score = self.score_editor.canvas.get_canvas_data()
        self.setWindowTitle(f"{self.tr('TEXTA Score Edit')} — {path.name}")

    def new_project(self) -> None:
        if not self.confirm_unsaved_changes():
            return
        canvas = self.score_editor.canvas
        canvas.clear_score()
        self.current_file = None
        self._saved_score = canvas.get_canvas_data()
        self.setWindowTitle(self.tr("TEXTA Score Edit"))

    def confirm_unsaved_changes(self) -> bool:
        if self.score_editor.canvas.get_canvas_data() == self._saved_score:
            return True
        answer = QMessageBox.warning(
            self,
            self.tr("Unsaved changes"),
            self.tr("Save changes before continuing?"),
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
            QMessageBox.Save,
        )
        if answer == QMessageBox.Save:
            self.save_file()
            return self.score_editor.canvas.get_canvas_data() == self._saved_score
        return answer == QMessageBox.Discard

    def closeEvent(self, event):
        if self.confirm_unsaved_changes():
            event.accept()
        else:
            event.ignore()

    def init_animation(self) -> None:
        if not self.config.get("animation", True):
            if hasattr(self, "window_animation"):
                self.window_animation.stop()
            self.setWindowOpacity(1)
            return
        if hasattr(self, "window_animation"):
            self.window_animation.stop()
        self.window_animation = QPropertyAnimation(self, b"windowOpacity")
        self.window_animation.setStartValue(0)
        self.window_animation.setEndValue(1)
        self.window_animation.setDuration(500)
        self.window_animation.start()


def main() -> int:
    arguments = sys.argv[1:]
    app = QApplication([sys.argv[0], *arguments])
    app.setOrganizationName("TEXTA")
    app.setApplicationName("ScoreEdit")

    window = MainWindow()
    if not window.first_open():
        return 0
    window.load()

    score_path = next((arg for arg in arguments if not arg.startswith("-")), None)
    if score_path is not None and Path(score_path).suffix.lower() == ".score":
        window.OpenApp(score_path)
    else:
        window.OpenApp()

    window.show()
    return app.exec_()


if __name__ == "__main__":
    raise SystemExit(main())
