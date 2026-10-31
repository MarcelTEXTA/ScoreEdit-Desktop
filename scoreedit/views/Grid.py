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
        self._resizing_note = None
        self.setMouseTracking(True)

        self.setMinimumSize(self.columns * self.grid_size, self.rows * self.grid_size)

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor(200, 200, 200), 1, Qt.SolidLine)
        painter.setPen(pen)

        for col in range(self.columns + 1):
            x = col * self.grid_size
            painter.drawLine(x, 0, x, self.rows * self.grid_size)
        for row in range(self.rows + 1):
            y = row * self.grid_size
            painter.drawLine(0, y, self.columns * self.grid_size, y)

        pen = QPen(QColor(30, 90, 150), 1, Qt.SolidLine)
        painter.setPen(pen)
        for note in self.notes:
            painter.fillRect(note, QColor(100, 180, 230))
            painter.drawRect(note)

    def mousePressEvent(self, event):
        """Ajouter ou retirer une note à la grille."""
        x = max(0, min(self.columns - 1, event.x() // self.grid_size))
        y = max(0, min(self.rows - 1, event.y() // self.grid_size))

        rect = QRect(x * self.grid_size, y * self.grid_size, self.grid_size, self.grid_size)
        existing = next(
            (note for note in self.notes if note.y() == rect.y() and note.x() <= rect.x() < note.x() + note.width()),
            None,
        )
        if event.button() == Qt.RightButton:
            if existing is not None:
                self.notes.remove(existing)
                self.update()
            return
        if event.button() != Qt.LeftButton:
            return
        if existing is not None:
            self._resizing_note = existing
        else:
            self.notes.append(rect)
            self._resizing_note = self.notes[-1]

        self.update()

    def mouseMoveEvent(self, event):
        if self._resizing_note is None or not event.buttons() & Qt.LeftButton:
            return
        right = max(
            self._resizing_note.x() + self.grid_size,
            min(
                self.columns * self.grid_size,
                ((event.x() // self.grid_size) + 1) * self.grid_size,
            ),
        )
        self._resizing_note.setWidth(right - self._resizing_note.x())
        self.update()

    def mouseReleaseEvent(self, event):
        self._resizing_note = None

    def clear_grid(self):
        """Effacer toutes les notes de la grille."""
        self.notes.clear()
        self.update()

    def get_notes(self):
        return [
            (note.x() // self.grid_size, note.y() // self.grid_size, note.width() // self.grid_size)
            for note in self.notes
        ]

    def set_notes(self, notes):
        parsed = []
        for column, row, duration in notes:
            if not (0 <= column < self.columns and 0 <= row < self.rows and duration > 0):
                continue
            width = min(duration, self.columns - column) * self.grid_size
            parsed.append(
                QRect(
                    column * self.grid_size,
                    row * self.grid_size,
                    width,
                    self.grid_size,
                )
            )
        self.notes = parsed
        self.update()
