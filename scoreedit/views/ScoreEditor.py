from PyQt5.QtWidgets import QScrollArea, QComboBox, QFrame, QPushButton, QButtonGroup, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy, QSpacerItem, QMenu, QInputDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QPoint, Qt, QSize
from .Canvas import Canvas
from ..resources import resource_path

class ScoreEditor(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()

        main_layout = QVBoxLayout()

        # Création du canvas
        self.canvas = Canvas(score_editor=self)

        # Zone de défilement pour le canvas
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.canvas)
        scroll_area.setWidgetResizable(True)

        self.frame = QFrame()
        self.frame.setObjectName("ToolbarFrame")

        frame_layout = QHBoxLayout(self.frame)

        # ComboBox pour sélectionner la clé
        self.clef_combo = QComboBox()
        self.clef_combo.addItems([self.tr("treble clef"), self.tr("bass clef"), self.tr("C clef")])
        self.clef_combo.currentIndexChanged.connect(self.change_clef)
        frame_layout.addWidget(self.clef_combo, alignment=Qt.AlignLeft)

        # ComboBox pour sélectionner le temps
        self.time_signature_combo = QComboBox()
        self.time_signature_combo.addItems(["2/2", "3/2", "4/2", "2/4", "3/4", "4/4", "5/4", "6/4", "7/4", "3/8", "6/8", "9/8", "12/8"])
        self.time_signature_combo.setCurrentText("4/4")
        self.time_signature_combo.currentIndexChanged.connect(self.change_time_signature)
        frame_layout.addWidget(self.time_signature_combo, alignment=Qt.AlignLeft)

        # ComboBox pour sélectionner le type de note
        self.note_type_combo = QComboBox()
        self.note_type_combo.addItems([
            self.tr("Whole note"),
            self.tr("Half note"),
            self.tr("Quarter note"),
            self.tr("Eighth note"),
            self.tr("Sixteenth note"),
            self.tr("Thirty-second note"),
            self.tr("Sixty-fourth note")
        ])
        self.note_type_combo.setCurrentIndex(2)
        self.note_type_combo.currentIndexChanged.connect(self.change_note_type)
        frame_layout.addWidget(self.note_type_combo, alignment=Qt.AlignLeft)
        self.change_note_type()

        # Création d'un groupe de boutons pour le comportement exclusif
        button_group = QButtonGroup(self)
        button_group.setExclusive(True)

        # Fonction pour gérer la sélection d'un bouton
        def on_button_clicked(button):
            for b in button_group.buttons():
                b.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(175, 175, 175);
                        border-radius: 9px;
                    }
                """)
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgb(150, 150, 250);
                    border-radius: 9px;
                }
            """)

            # appliquer le comportement en fonction du bouton sélectionné
            if button == select_button:
                self.canvas.set_tool('selection')
            elif button == insert_button:
                self.canvas.set_tool('insertion')
            elif button == delet_button:
                self.canvas.set_tool('delet')
            elif button == colle_button:
                self.canvas.set_tool('colle')
            elif button == coupe_button:
                self.canvas.set_tool('coupe')

            # Désélectionner les autres boutons
            for b in button_group.buttons():
                if b != button:
                    b.setChecked(False)

        # Création des QPushButton avec des icônes uniquement
        select_button = QPushButton()
        select_button.setIcon(QIcon(str(resource_path("IconApp", "toolbar", "selections.png"))))
        select_button.setIconSize(QSize(17, 17))
        select_button.setCheckable(True)
        select_button.clicked.connect(lambda: on_button_clicked(select_button))
        frame_layout.addWidget(select_button, alignment=Qt.AlignLeft)

        insert_button = QPushButton()
        insert_button.setIcon(QIcon(str(resource_path("IconApp", "toolbar", "insertions.png"))))
        insert_button.setIconSize(QSize(17, 17))
        insert_button.setCheckable(True)
        insert_button.clicked.connect(lambda: on_button_clicked(insert_button))
        frame_layout.addWidget(insert_button, alignment=Qt.AlignLeft)

        delet_button = QPushButton() # supprime les notes cliqué
        delet_button.setIcon(QIcon(str(resource_path("IconApp", "toolbar", "gomme.png"))))
        delet_button.setIconSize(QSize(17, 17))
        delet_button.setCheckable(True)
        delet_button.clicked.connect(lambda: on_button_clicked(delet_button))
        frame_layout.addWidget(delet_button, alignment=Qt.AlignLeft)

        colle_button = QPushButton()
        colle_button.setIcon(QIcon(str(resource_path("IconApp", "toolbar", "colle.png"))))
        colle_button.setIconSize(QSize(17, 17))
        colle_button.setCheckable(True)
        colle_button.clicked.connect(lambda: on_button_clicked(colle_button))
        frame_layout.addWidget(colle_button, alignment=Qt.AlignLeft)

        coupe_button = QPushButton()
        coupe_button.setIcon(QIcon(str(resource_path("IconApp", "toolbar", "ciseaux.png"))))
        coupe_button.setIconSize(QSize(17, 17))
        coupe_button.setCheckable(True)
        coupe_button.clicked.connect(lambda: on_button_clicked(coupe_button))
        frame_layout.addWidget(coupe_button, alignment=Qt.AlignLeft)

        button_group.addButton(select_button)
        button_group.addButton(insert_button)
        button_group.addButton(delet_button)
        button_group.addButton(colle_button)
        button_group.addButton(coupe_button)

        separator_line = QFrame()
        separator_line.setFrameShape(QFrame.VLine) 
        separator_line.setFrameShadow(QFrame.Plain)
        frame_layout.addWidget(separator_line)

        inf_note = QPushButton()
        inf_note.setIcon(QIcon(str(resource_path("IconApp", "toolbar", "note_inf.png"))))
        inf_note.setIconSize(QSize(17, 17))

        supp_note = QPushButton()
        supp_note.setIcon(QIcon(str(resource_path("IconApp", "toolbar", "note_supp.png"))))
        supp_note.setIconSize(QSize(17, 17))

        inf_octave = QPushButton()
        inf_octave.setIcon(QIcon(str(resource_path("IconApp", "toolbar", "oct_inf.png"))))
        inf_octave.setIconSize(QSize(17, 17))

        supp_octave = QPushButton()
        supp_octave.setIcon(QIcon(str(resource_path("IconApp", "toolbar", "oct_supp.png"))))
        supp_octave.setIconSize(QSize(17, 17))
        inf_note.clicked.connect(lambda: self.canvas.transpose_selected(-1))
        supp_note.clicked.connect(lambda: self.canvas.transpose_selected(1))
        inf_octave.clicked.connect(lambda: self.canvas.transpose_selected_octave(-1))
        supp_octave.clicked.connect(lambda: self.canvas.transpose_selected_octave(1))

        frame_layout.addWidget(inf_note, alignment=Qt.AlignLeft)
        frame_layout.addWidget(supp_note, alignment=Qt.AlignLeft)
        frame_layout.addWidget(inf_octave, alignment=Qt.AlignLeft)
        frame_layout.addWidget(supp_octave, alignment=Qt.AlignLeft)

        # Boutons à droite
        right_separator_line = QFrame()
        right_separator_line.setFrameShape(QFrame.VLine)
        right_separator_line.setFrameShadow(QFrame.Plain)
        frame_layout.addWidget(right_separator_line)

        self.more_button = QPushButton(self.tr("more"))
        self.more_button.clicked.connect(self.show_menu)
        frame_layout.addWidget(self.more_button, alignment=Qt.AlignRight)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        frame_layout.addSpacerItem(spacer)

        # Ajouter la frame au layout principal
        main_layout.addWidget(self.frame)

        main_layout.addWidget(scroll_area)

        layout.addLayout(main_layout)

        self.setLayout(layout)

        self.selected_clef = 'sol'
        self.selected_time_signature = '4/4'
        self.selected_note_type = 'noire'

    def show_menu(self):
        menu = QMenu(self)
        menu.addAction(
            self.tr("Add note"),
            lambda: self.canvas.add_note(self.canvas.note_type, QPoint(100, 100)),
        )
        menu.addAction(
            self.tr("Add rest"),
            lambda: self.canvas.add_rest(QPoint(100, 100)),
        )
        menu.addAction(
            self.tr("Add chord"),
            lambda: self.canvas.add_chord(QPoint(100, 100)),
        )
        menu.addAction(self.tr("Add text"), self.add_text)

        menu.exec(self.more_button.mapToGlobal(self.more_button.rect().bottomLeft()))

    def add_text(self):
        text, accepted = QInputDialog.getText(self, self.tr("Add text"), self.tr("Text"))
        if accepted:
            self.canvas.add_text(text, QPoint(100, 120))

    def change_clef(self):
        """Changer la clé en fonction de la sélection."""
        clefs = ("sol", "fa", "ut")
        index = self.clef_combo.currentIndex()
        if 0 <= index < len(clefs):
            self.canvas.set_clef(clefs[index])

    def change_time_signature(self):
        """Changer la signature temporelle."""
        self.selected_time_signature = self.time_signature_combo.currentText()

        beats, note_value = map(int, self.selected_time_signature.split("/"))
        self.canvas.set_time_signature(beats, note_value)

    def change_note_type(self):
        note_types = (
            "ronde",
            "blanche",
            "noire",
            "croche",
            "doubleCroche",
            "quatrupleCroche",
            "sextupleCroche",
        )
        index = self.note_type_combo.currentIndex()
        note_type = note_types[index] if 0 <= index < len(note_types) else "noire"
        self.canvas.set_note_type(note_type)

    def set_note_type(self, note_type):
        """Mettre à jour le type de note dans le Canvas."""
        note_types = (
            "ronde",
            "blanche",
            "noire",
            "croche",
            "doubleCroche",
            "quatrupleCroche",
            "sextupleCroche",
        )
        if note_type not in note_types:
            return
        self.note_type_combo.setCurrentIndex(note_types.index(note_type))
        self.canvas.set_note_type(note_type)