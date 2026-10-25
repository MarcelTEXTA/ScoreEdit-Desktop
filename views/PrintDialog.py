from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton


class PrintDialog(QDialog):
    def __init__(self, parent=None, flags=None):
        super().__init__(parent)

        self.setWindowTitle("Print")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout(self)

        self.print_button = QPushButton("Print")
        self.print_button.clicked.connect(self.print)
        layout.addWidget(self.print_button)

        self.setLayout(layout)

    def print(self):
        print("Print")