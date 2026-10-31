from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QFileDialog

from ..config import load_config

class WelcomeDialog(QDialog):
    def __init__(self, parent=None, flags=None):
        super().__init__(parent)

        self.setWindowTitle(self.tr("Welcome !"))
        self.setGeometry(100, 100, 400, 300)
        self.selected_file = None

        layout = QVBoxLayout(self)

        self.list_widget = QListWidget()
        for file_path in load_config().get("recent_files", []):
            self.list_widget.addItem(file_path)
        self.list_widget.itemDoubleClicked.connect(self.open_recent_file)
        layout.addWidget(self.list_widget)

        button_layout = QHBoxLayout()

        self.open_button = QPushButton(self.tr("Open"))
        self.open_button.clicked.connect(self.open_file)
        button_layout.addWidget(self.open_button)

        self.new_button = QPushButton(self.tr("New file"))
        self.new_button.clicked.connect(self.new)
        button_layout.addWidget(self.new_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def new(self):
        self.accept()

    def open_file(self):
        current_item = self.list_widget.currentItem()
        if current_item is not None:
            self.selected_file = current_item.text()
            self.accept()
            return
        # Ouvrir un fichier via un QFileDialog
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            self.tr("Open a project"),
            "",
            self.tr("TEXTA scores (*.score)"),
        )
        if file_name:
            self.selected_file = file_name
            self.accept()

    def open_recent_file(self, item):
        self.selected_file = item.text()
        self.accept()
