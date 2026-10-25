from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout
from PyQt5.QtGui import QIcon

class TextEdit(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("TabItem")
        
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.textEdit = QTextEdit()
        self.textEdit.setPlaceholderText(self.tr("Enter text or lyrics here, xml, score_shell ..."))

        layout.addWidget(self.textEdit)

        self.setLayout(layout)