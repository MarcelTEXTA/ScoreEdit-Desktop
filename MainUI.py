"""Compatibility import for older code using ``MainUI``."""

from scoreedit.app import MainWindow


class MainUI(MainWindow):
    """Backward-compatible name for the main application window."""

    def __init__(self, main_window=None):
        super().__init__()
