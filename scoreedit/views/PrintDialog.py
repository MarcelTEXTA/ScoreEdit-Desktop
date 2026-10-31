from PyQt5.QtGui import QPainter
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import (
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

class PrintDialog(QDialog):
    def __init__(self, parent=None, flags=None, canvas=None):
        if flags is None:
            super().__init__(parent)
        else:
            super().__init__(parent, flags)
        self.canvas = canvas

        self.setWindowTitle(self.tr("Print score"))
        self.setMinimumWidth(300)

        layout = QVBoxLayout(self)
        buttons = QHBoxLayout()
        self.print_button = QPushButton(self.tr("Print"))
        self.print_button.clicked.connect(self.print_to_printer)
        self.pdf_button = QPushButton(self.tr("Export PDF"))
        self.pdf_button.clicked.connect(self.export_pdf)
        close_button = QPushButton(self.tr("Close"))
        close_button.clicked.connect(self.reject)
        buttons.addWidget(self.print_button)
        buttons.addWidget(self.pdf_button)
        buttons.addWidget(close_button)
        layout.addLayout(buttons)

    def print(self):
        self.print_to_printer()

    def print_to_printer(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() != QPrintDialog.Accepted:
            return
        self._render(printer)

    def export_pdf(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, self.tr("Export PDF"), "", self.tr("PDF files (*.pdf)")
        )
        if not file_name:
            return
        if not file_name.lower().endswith(".pdf"):
            file_name += ".pdf"
        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(file_name)
        if not self._render(printer):
            return
        QMessageBox.information(self, self.tr("PDF exported"), file_name)

    def _render(self, printer):
        if self.canvas is None:
            QMessageBox.warning(
                self, self.tr("Print error"), self.tr("No score is available to print.")
            )
            return False
        painter = QPainter()
        if not painter.begin(printer):
            QMessageBox.critical(
                self, self.tr("Print error"), self.tr("The printer could not be started.")
            )
            return False
        page = printer.pageRect(QPrinter.DevicePixel)
        source = self.canvas.rect()
        if source.isEmpty() or page.isEmpty():
            painter.end()
            QMessageBox.warning(
                self, self.tr("Print error"), self.tr("The score has no printable area.")
            )
            return False
        scale = min(page.width() / source.width(), page.height() / source.height())
        painter.translate(page.topLeft())
        painter.scale(scale, scale)
        self.canvas.render(painter)
        painter.end()
        return True