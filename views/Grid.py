from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt , QRect

class Grid(QWidget):
    def __init__(self, grid_size, columns, rows):
        super().__init__()
        self.grid_size = grid_size
        self.columns = columns
        self.rows = rows
        self.notes = []

        self.setMinimumSize(self.columns * self.grid_size, self.rows * self.grid_size)

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor(200, 200, 200), 1, Qt.SolidLine)
        painter.setPen(pen)

        # Dessiner la grille
        for col in range(self.columns):
            for row in range(self.rows):
                rect = QRect(col * self.grid_size, row * self.grid_size, self.grid_size, self.grid_size)
                painter.drawRect(rect)

        # Dessiner les notes
        pen = QPen(QColor(0, 0, 0), 1, Qt.SolidLine)
        painter.setPen(pen)
        for note in self.notes:
            painter.fillRect(note, QColor(100, 200, 100))

    def mousePressEvent(self, event):
        """Ajouter ou retirer une note à la grille."""
        x = event.x() // self.grid_size
        y = event.y() // self.grid_size

        rect = QRect(x * self.grid_size, y * self.grid_size, self.grid_size, self.grid_size)
        
        if rect in self.notes:
            self.notes.remove(rect)  # Retirer la note si elle est déjà présente
        else:
            self.notes.append(rect)  # Ajouter la note

        self.update()

    def clear_grid(self):
        """Effacer toutes les notes de la grille."""
        self.notes.clear()
        self.update()
