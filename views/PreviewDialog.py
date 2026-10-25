# boite de dialogue de prévisualisation avec canvas
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton
from .Canvas import Canvas

class PreviewDialog(QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal
        main_layout = QVBoxLayout()

        # Ajouter le canvas pour la partition
        self.canvas = Canvas()
        main_layout.addWidget(self.canvas)

        # Ajouter un bouton pour fermer la boîte de dialogue
        close_button = QPushButton("Fermer")
        close_button.clicked.connect(self.close)
        main_layout.addWidget(close_button)

        self.setLayout(main_layout)

        self.setWindowTitle("Prévisualisation")
        self.setFixedWidth(800)
        self.setFixedHeight(600)
        self.show()

    def close(self):
        self.hide()