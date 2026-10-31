from PyQt5.QtWidgets import QScrollArea, QComboBox, QFrame, QPushButton, QButtonGroup, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy, QSpacerItem, QMenu
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from .Canvas import Canvas

class ScoreEditor(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()

        # Création du layout principal
        main_layout = QVBoxLayout()

        # Création du canvas
        self.canvas = Canvas(score_editor=self)

        # Zone de défilement pour le canvas
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.canvas)
        scroll_area.setWidgetResizable(True)

        # Créer une frame pour contenir les boutons et autres contrôles
        self.frame = QFrame()
        self.frame.setObjectName("ToolbarFrame")

        frame_layout = QHBoxLayout(self.frame)

        # ComboBox pour sélectionner la clé
        self.clef_combo = QComboBox()
        self.clef_combo.addItems([self.tr("treble clef"), self.tr("bass clef"), self.tr("C clef"), self.tr("More options")])
        self.clef_combo.currentIndexChanged.connect(self.change_clef)
        frame_layout.addWidget(self.clef_combo, alignment=Qt.AlignLeft)

        # ComboBox pour sélectionner le temps
        self.time_signature_combo = QComboBox()
        self.time_signature_combo.addItems(["2/2", "3/2", "4/2", "2/4", "3/4", "4/4", "5/4", "6/4", "7/4", "3/8", "6/8", "9/8", "12/8"])
        self.time_signature_combo.currentIndexChanged.connect(self.change_time_signature)
        frame_layout.addWidget(self.time_signature_combo, alignment=Qt.AlignLeft)

        # ComboBox pour sélectionner le type de note
        self.note_type_combo = QComboBox()
        self.note_type_combo.addItems([self.tr("Whole note"), self.tr("Half note"), self.tr("Quarter note"), self.tr("Eighth note"), self.tr("Sixteenth note"), self.tr("Thirty-second note"), self.tr("Sixty-fourth note")])
        self.note_type_combo.currentIndexChanged.connect(self.change_note_type)
        frame_layout.addWidget(self.note_type_combo, alignment=Qt.AlignLeft)
        self.note_type = self.note_type_combo.currentText()

        if self.note_type_combo.currentText() == self.tr("Whole note"):
            self.canvas.note_type = 'whole'
        elif self.note_type_combo.currentText() == self.tr("Half note"):
            self.canvas.note_type = 'half'
        elif self.note_type_combo.currentText() == self.tr("Quarter note"):
            self.canvas.note_type = 'quarter'
        elif self.note_type_combo.currentText() == self.tr("Eighth note"):
            self.canvas.note_type = 'eighth'
        elif self.note_type_combo.currentText() == self.tr("Sixteenth note"):
            self.canvas.note_type = 'sixteenth'
        elif self.note_type_combo.currentText() == self.tr("Thirty-second note"):
            self.canvas.note_type = 'thirty_second'
        elif self.note_type_combo.currentText() == self.tr("Sixty-fourth note"):
            self.canvas.note_type = 'sixty_fourth'

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
        select_button = QPushButton() # sélectionné, peut sélectionné les notes pour les déplacer, les supprimer, les couper, les coller, reglés leurs propriétés
        select_button.setIcon(QIcon("IconApp/Toolbar/selections.png"))
        select_button.setIconSize(QSize(17, 17))
        select_button.setCheckable(True)  # Rendre le bouton "checkable"
        select_button.clicked.connect(lambda: on_button_clicked(select_button))
        frame_layout.addWidget(select_button, alignment=Qt.AlignLeft)

        insert_button = QPushButton() # insert seulement les notes en cliquant sur la podtrée
        insert_button.setIcon(QIcon("IconApp/Toolbar/insertions.png"))
        insert_button.setIconSize(QSize(17, 17))
        insert_button.setCheckable(True)  # Rendre le bouton "checkable"
        insert_button.clicked.connect(lambda: on_button_clicked(insert_button))
        frame_layout.addWidget(insert_button, alignment=Qt.AlignLeft)

        delet_button = QPushButton() # supprime les notes cliqué
        delet_button.setIcon(QIcon("IconApp/Toolbar/gomme.png"))
        delet_button.setIconSize(QSize(17, 17))
        delet_button.setCheckable(True)  # Rendre le bouton "checkable"
        delet_button.clicked.connect(lambda: on_button_clicked(delet_button))
        frame_layout.addWidget(delet_button, alignment=Qt.AlignLeft)

        colle_button = QPushButton() # cliqués note pour la dupliqué avec la note à droite
        colle_button.setIcon(QIcon("IconApp/Toolbar/colle.png"))
        colle_button.setIconSize(QSize(17, 17))
        colle_button.setCheckable(True)  # Rendre le bouton "checkable"
        colle_button.clicked.connect(lambda: on_button_clicked(colle_button))
        frame_layout.addWidget(colle_button, alignment=Qt.AlignLeft)

        coupe_button = QPushButton() # coupe une note en deux (blanche cliqué devient deux noires)
        coupe_button.setIcon(QIcon("IconApp/Toolbar/ciseaux.png"))
        coupe_button.setIconSize(QSize(17, 17))
        coupe_button.setCheckable(True)  # Rendre le bouton "checkable"
        coupe_button.clicked.connect(lambda: on_button_clicked(coupe_button))
        frame_layout.addWidget(coupe_button, alignment=Qt.AlignLeft)

        # Ajouter les boutons au groupe
        button_group.addButton(select_button)
        button_group.addButton(insert_button)
        button_group.addButton(delet_button)
        button_group.addButton(colle_button)
        button_group.addButton(coupe_button)

        separator_line = QFrame()
        separator_line.setFrameShape(QFrame.VLine)  # Définir la ligne verticale
        separator_line.setFrameShadow(QFrame.Plain)  # Effet de la ligne
        frame_layout.addWidget(separator_line)

        inf_note = QPushButton() # - 1/2 ton à la note
        inf_note.setIcon(QIcon("IconApp/Toolbar/note_inf.png"))
        inf_note.setIconSize(QSize(17, 17))

        supp_note = QPushButton() # + 1/2 ton à la note
        supp_note.setIcon(QIcon("IconApp/Toolbar/note_supp.png"))
        supp_note.setIconSize(QSize(17, 17))

        inf_octave = QPushButton() # - 1 octave à la note
        inf_octave.setIcon(QIcon("IconApp/Toolbar/oct_inf.png"))
        inf_octave.setIconSize(QSize(17, 17))

        supp_octave = QPushButton() # + 1 octave à la note
        supp_octave.setIcon(QIcon("IconApp/Toolbar/oct_supp.png"))
        supp_octave.setIconSize(QSize(17, 17))

        frame_layout.addWidget(inf_note, alignment=Qt.AlignLeft)
        frame_layout.addWidget(supp_note, alignment=Qt.AlignLeft)
        frame_layout.addWidget(inf_octave, alignment=Qt.AlignLeft)
        frame_layout.addWidget(supp_octave, alignment=Qt.AlignLeft)

        # Boutons à droite
        right_separator_line = QFrame()
        right_separator_line.setFrameShape(QFrame.VLine)  # Définir la ligne verticale
        right_separator_line.setFrameShadow(QFrame.Plain)  # Effet de la ligne
        frame_layout.addWidget(right_separator_line)

        score_style = QPushButton(self.tr("score style")) # change le style de la partition
        # score_style.setIcon(QIcon("IconApp/Toolbar/style.png"))
        frame_layout.addWidget(score_style, alignment=Qt.AlignRight)

        self.more_button = QPushButton(self.tr("more")) # plus d'options
        self.more_button.clicked.connect(self.show_menu)
        frame_layout.addWidget(self.more_button, alignment=Qt.AlignRight)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        frame_layout.addSpacerItem(spacer)

        # Ajouter la frame au layout principal
        main_layout.addWidget(self.frame)

        # Ajouter le canvas et la zone de défilement dans le layout principal
        main_layout.addWidget(scroll_area)

        layout.addLayout(main_layout)

        self.setLayout(layout)

        # Variables pour la clé, la signature temporelle, et le type de note sélectionnés
        self.selected_clef = 'sol'
        self.selected_time_signature = '4/4'
        self.selected_note_type = 'noire'

    def show_menu(self):
        menu = QMenu(self)

        menu.addAction(self.tr("Add note"), self.canvas.add_note)
        menu.addAction(self.tr("Add rest"))
        menu.addAction(self.tr("Add chord"))
        menu.addAction(self.tr("Add text"))

        menu.exec(self.more_button.mapToGlobal(self.more_button.rect().bottomLeft()))

    def change_clef(self):
        """Changer la clé en fonction de la sélection."""
        clef = self.clef_combo.currentText()
        if clef == "Clé de Sol":
            self.canvas.set_clef('sol')
        elif clef == "Clé de Fa":
            self.canvas.set_clef('fa')
        elif clef == "Clé d'Ut":
            self.canvas.set_clef('ut')

    def change_time_signature(self):
        """Changer la signature temporelle."""
        self.selected_time_signature = self.time_signature_combo.currentText()

        # Diviser la signature temporelle en battements et valeur de note
        beats, note_value = map(int, self.selected_time_signature.split("/"))
        self.canvas.set_time_signature(beats, note_value)

    def change_note_type(self):
        label = self.note_type_combo.currentText()
        # Convertir le label français vers le nom interne utilisé par le Canvas
        type_map = {
            "Ronde": "ronde",
            "Blanche": "blanche",
            "Noire": "noire",
            "Croche": "croche",
            "Double croche": "double_croche",
            "Triple croche": "triple_croche"
        }
        note_type = type_map.get(label, "noire")  # valeur par défaut = noire
        self.canvas.set_note_type(note_type)

    def set_note_type(self, note_type):
        """Mettre à jour le type de note dans le Canvas."""
        self.canvas.note_type = note_type
        self.note_type_combo.setCurrentText(note_type)