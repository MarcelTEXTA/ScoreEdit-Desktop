from pathlib import Path

from PyQt5.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

class TextEdit(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("TabItem")
        self.current_file = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        button_layout = QHBoxLayout()
        open_button = QPushButton(self.tr("Open text"))
        open_button.clicked.connect(self.open_file)
        save_button = QPushButton(self.tr("Save text"))
        save_button.clicked.connect(self.save_file)
        save_as_button = QPushButton(self.tr("Save text as"))
        save_as_button.clicked.connect(lambda: self.save_file(save_as=True))
        button_layout.addWidget(open_button)
        button_layout.addWidget(save_button)
        button_layout.addWidget(save_as_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText(self.tr("Enter text or lyrics here..."))
        self.textEdit = self.text_edit
        layout.addWidget(self.text_edit)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, self.tr("Open text"), "", self.tr("Text files (*.txt *.ly);;All files (*)")
        )
        if not file_name:
            return
        try:
            content = Path(file_name).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            QMessageBox.critical(self, self.tr("Open error"), str(error))
            return
        self.text_edit.setPlainText(content)
        self.current_file = Path(file_name)

    def save_file(self, save_as=False):
        path = None if save_as else self.current_file
        if path is None:
            file_name, _ = QFileDialog.getSaveFileName(
                self, self.tr("Save text"), "", self.tr("Text files (*.txt);;All files (*)")
            )
            if not file_name:
                return
            path = Path(file_name)
            if not path.suffix:
                path = path.with_suffix(".txt")
        try:
            path.write_text(self.text_edit.toPlainText(), encoding="utf-8")
        except OSError as error:
            QMessageBox.critical(self, self.tr("Save error"), str(error))
            return
        self.current_file = path

        self.setLayout(layout)