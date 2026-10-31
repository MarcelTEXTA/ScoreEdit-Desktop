from PyQt5.QtWidgets import QFrame, QToolBox, QVBoxLayout, QWidget, QPushButton


class Sidebar(QFrame):
    def __init__(self, canvas, parent=None):
        super().__init__(parent)
        self.canvas = canvas
        self.setObjectName("sidebar")
        self.setFrameShape(QFrame.StyledPanel)
        self.setFixedWidth(210)

        layout = QVBoxLayout(self)
        self.toolbox = QToolBox()
        layout.addWidget(self.toolbox)

        tools = QWidget()
        tools_layout = QVBoxLayout(tools)
        for label, tool in (
            (self.tr("Insert notes"), "insertion"),
            (self.tr("Select and move"), "selection"),
            (self.tr("Delete notes"), "delet"),
            (self.tr("Duplicate notes"), "colle"),
            (self.tr("Split notes"), "coupe"),
        ):
            button = QPushButton(label)
            button.clicked.connect(lambda checked=False, mode=tool: self.canvas.set_tool(mode))
            tools_layout.addWidget(button)
        tools_layout.addStretch()
        self.toolbox.addItem(tools, self.tr("Editing tools"))

        accidentals = QWidget()
        accidentals_layout = QVBoxLayout(accidentals)
        for label, symbol in (
            (self.tr("Add sharp"), "#"),
            (self.tr("Add flat"), "b"),
        ):
            button = QPushButton(label)
            button.clicked.connect(
                lambda checked=False, accidental=symbol: self.canvas.add_accidental(accidental)
            )
            accidentals_layout.addWidget(button)
        accidentals_layout.addStretch()
        self.toolbox.addItem(accidentals, self.tr("Accidentals"))

        measures = QWidget()
        measures_layout = QVBoxLayout(measures)
        add_measure_button = QPushButton(self.tr("Add measure"))
        add_measure_button.clicked.connect(self.canvas.add_measure)
        measures_layout.addWidget(add_measure_button)
        for label, clef in (
            (self.tr("Treble clef"), "sol"),
            (self.tr("Bass clef"), "fa"),
            (self.tr("Alto clef"), "ut"),
        ):
            button = QPushButton(label)
            button.clicked.connect(lambda checked=False, value=clef: self.canvas.set_clef(value))
            measures_layout.addWidget(button)
        measures_layout.addStretch()
        self.toolbox.addItem(measures, self.tr("Score"))
