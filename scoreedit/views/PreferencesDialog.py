import os
import sys
import json
from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit, QHBoxLayout, QListWidget, QStackedWidget, QVBoxLayout, QWidget, QLabel, QPushButton, QGroupBox, QCheckBox, QRadioButton, QSpacerItem, QSizePolicy, QScrollArea
from PyQt5.QtCore import Qt

class PreferencesDialog(QDialog):
    def __init__(self, parent=None, flags=None):
        super().__init__(parent)

        main_layout = QVBoxLayout(self)

        # Layout horizontal principal
        content_layout = QHBoxLayout(self)
        main_layout.addLayout(content_layout)

        # Liste des préférences
        self.list_widget = QListWidget()
        self.list_widget.addItems([self.tr("General"), self.tr("Display"), self.tr("Scores"), self.tr("MIDI"), self.tr("Audio"), self.tr("Shortucts and gestures"), self.tr("Plugins")])
        self.list_widget.setMaximumWidth(300) # addaptative au contenu
        content_layout.addWidget(self.list_widget)

        # QStackedWidget pour contenir les différents écrans de préférences
        self.stacked_widget = QStackedWidget()
        self.stacked_scroller = QScrollArea()
        self.stacked_scroller.setWidget(self.stacked_widget)
        self.stacked_scroller.setWidgetResizable(True)
        self.stacked_scroller.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        content_layout.addWidget(self.stacked_scroller)

        # Ajouter des widgets dans le QStackedWidget
        self.stacked_widget.addWidget(self.create_general_preferences())
        self.stacked_widget.addWidget(self.create_display_preferences())
        self.stacked_widget.addWidget(self.create_score_preferences())
        self.stacked_widget.addWidget(self.create_midi_preferences())
        self.stacked_widget.addWidget(self.create_audio_preferences())
        self.stacked_widget.addWidget(self.create_shortcut_preferences())
        self.stacked_widget.addWidget(self.create_plugin_preferences())

        # Connecter le changement de ligne à l'affichage de la page correspondante
        self.list_widget.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)

        # Configurer la fenêtre
        self.list_widget.setCurrentRow(0)
        self.setWindowTitle(self.tr("Preferences"))
        self.setModal(True)
        self.show()

        # boutons en bas
        button_layout = QHBoxLayout()
        self.button_ok = QPushButton(self.tr("OK"))
        self.button_ok.clicked.connect(self.accept)
        self.button_cancel = QPushButton(self.tr("Cancel"))
        self.button_cancel.clicked.connect(self.reject)
        main_layout.addLayout(button_layout, Qt.AlignBottom)
        button_layout.addWidget(self.button_ok)
        button_layout.addWidget(self.button_cancel)

    def accept(self):
        return super().accept()
    
        # Récupérer les valeurs des préférences
        self.selected_theme = None  # Valeur par défaut, à remplacer par la sélection de l'utilisateur
        self.username = "user"  # Valeur par défaut, à remplacer par la saisie de l'utilisateur
        self.password = "password"
        self.language = "en"  # Langue par défaut, à remplacer par la sélection de l'utilisateur
        self.default_directory = self.path_edit.text()  # Chemin par défaut, à remplacer par la saisie de l'utilisateur
        self.default_format = "score"  # Format par défaut, à remplacer par la sélection de l'utilisateur
        self.check.isChecked()  # Pour savoir si la case est cochée
        self.help_sheck.isChecked()  # Pour savoir si la case est cochée
        self.info_bulle_check.isChecked()  # Pour savoir si la case est cochée
        self.start_prog_check.isChecked()  # Pour savoir si la case est cochée
        self.UI_mode_h_radio.isChecked()  # Pour savoir si la radio est cochée
        self.UI_mode_v_radio.isChecked()  # Pour savoir si la radio est cochée
        self.animation_check.isChecked()  # Pour savoir si la case est cochée

        # écrire dans un fichier de configuration ou appliquer les préférences
        with open("config.json", "w") as f:
            config = {
                'first_open': False,
                'theme': self.selected_theme,
                'username': self.username,
                'password': self.password,
                'language': self.language,
                'default_directory': self.default_directory,
                'default_format': self.default_format,
                # autres paramètres par défaut à ajouter
                'file_dialog': self.check.isChecked(),
                'experience_plus': self.help_sheck.isChecked(),
                'tooltips': True,  # info_bulle_check.isChecked(),
                'startup': self.start_prog_check.isChecked(),
                'user_interface': 'horizontal',  # UI_mode_h_radio.isChecked() ? 'horizontal' : 'vertical',
                'animation': self.animation_check.isChecked(),
                'score_display': 'horizontal' if self.score_mode_radio.isChecked() else 'page',
                # 'shortcut': self.shortcut_edit.text(),  # à implémenter
            }
            json.dump(config, f, indent=4)


        # 'first_open': False,
        # 'theme': self.selected_theme,
        # 'username': self.username,
        # 'password': self.password,
        # 'language': self.language,
        # 'default_directory': self.default_directory,
        # 'default_format': self.default_format,
        # # autre paramètres par défaut à ajouter
        # 'file_dialog': False,
        # 'experience_plus': False,
        # 'tooltips': True,
        # 'startup': False,
        # 'user_interface': 'horizontal',
        # 'animation': True,
        # 'score_display': 'horizontal',
        # 'shortcut': 'default',

    def reject(self):
        return super().reject()
    
    def set_language(self, language):
        # Implémenter la logique pour changer la langue de l'application
        print(f"Language set to: {language}")
        # Ici, vous pouvez ajouter le code pour recharger les traductions ou mettre à jour l'interface utilisateur

    def create_general_preferences(self):
        widget = QWidget()
        layout = QVBoxLayout()

        group_languages = QGroupBox(self.tr("Languages"), self)
        layout_language = QVBoxLayout(group_languages)

        combo = QComboBox()
        list_item = ["English", "Français", "Deutsch", "Español", "Italiano", "Nederlands"]
        combo.addItems(list_item)
        combo.currentIndexChanged.connect(lambda index: self.set_language(list_item[index]))
        layout_language.addWidget(combo)

        layout.addWidget(group_languages)
        
        # UI pour les préférences générales
        groupe_dialog = QGroupBox(self.tr("Dialog box"), self)
        layout_dialog = QVBoxLayout(groupe_dialog)
        
        self.check = QCheckBox(self.tr("Display TEXTA dialogs for opening files or saving files"))
        
        layout_dialog.addWidget(self.check)

        layout.addWidget(groupe_dialog)

        group_help = QGroupBox(self.tr("help and user experience"), self)
        layout_help = QVBoxLayout(group_help)

        self.help_sheck = QCheckBox(self.tr("Send anonymous usage information to TEXTA to improve the software."))
        self.help_sheck_info = QLabel(self.tr("Before checking the box, please read the terms and conditions of the enhanced user experience.."))
        self.help_sheck_info.setWordWrap(True)
        layout_help.addWidget(self.help_sheck)
        layout_help.addWidget(self.help_sheck_info)

        info_bulle_check = QCheckBox(self.tr("Display tooltips on button hovers"))
        layout_help.addWidget(info_bulle_check)

        layout.addWidget(group_help)

        start_group = QGroupBox(self.tr("Start"), self)
        layout_start = QVBoxLayout(start_group)

        self.start_prog_check = QCheckBox(self.tr("Start TEXTA score edit at computer startup"))
        layout_start.addWidget(self.start_prog_check)

        layout.addWidget(start_group)

        group_path = QGroupBox(self.tr("Paths"), self)
        layout_path = QVBoxLayout(group_path)

        user_name = os.getlogin()

        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText(self.tr("Path to the folder where the scores are saved"))
        self.path_edit.setText(f"C:/Users/{user_name}/Documents/TEXTA score edit/")
        layout_path.addWidget(self.path_edit)

        self.btn_path = QPushButton(self.tr("Browse"))
        self.btn_path.clicked.connect(lambda: self.set_path(self.path_edit.text()))
        layout_path.addWidget(self.btn_path)

        layout.addWidget(group_path)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addSpacerItem(spacer)

        widget.setLayout(layout)
        return widget

    def create_display_preferences(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.comboBox = QComboBox(self)
        self.comboBox.addItem(self.tr("Light theme"), "styles/style.css")
        self.comboBox.addItem(self.tr("Dark theme"), "styles/style_2.css")
        self.comboBox.addItem(self.tr("Color theme"), "styles/style_3.css")
        self.comboBox.addItem(self.tr("Compact theme"), "styles/style_4.css")
        self.comboBox.addItem(self.tr("Glass theme"), "styles/style_5.css")
        self.comboBox.addItem(self.tr("OS theme"), "styles/vide.css")
        layout.addWidget(self.comboBox)

        self.comboBox.currentIndexChanged.connect(self.change_theme)

        UI_mode_group = QGroupBox(self.tr("User interface mode"), self)
        layout_ui = QVBoxLayout(UI_mode_group)

        UI_mode_v_radio = QRadioButton()
        UI_mode_v_radio.setText(self.tr("Vertical"))
        UI_mode_v_radio.setChecked(True)
        layout_ui.addWidget(UI_mode_v_radio)

        UI_mode_h_radio = QRadioButton()
        UI_mode_h_radio.setText(self.tr("Horizontal"))
        layout_ui.addWidget(UI_mode_h_radio)

        layout.addWidget(UI_mode_group)

        animat_group = QGroupBox(self.tr("Animation"), self)
        layout_animation = QVBoxLayout(animat_group)

        self.animation_check = QCheckBox(self.tr("Enable animations"))
        layout_animation.addWidget(self.animation_check)

        display_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addSpacerItem(display_spacer)

        layout.addWidget(animat_group)

        widget.setLayout(layout)
        return widget
    
    def change_theme(self):
        pass

    def create_score_preferences(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # UI pour les préférences de partition

        goup_score_display = QGroupBox(self.tr("Score displays"), self)
        layout_score_display = QVBoxLayout(goup_score_display)

        self.score_mode_radio = QRadioButton()
        self.score_mode_radio.setText(self.tr("Hotizontal mode"))
        self.score_mode_radio.setChecked(True)

        self.score_mode_radio2 = QRadioButton()
        self.score_mode_radio2.setText(self.tr("Page mode"))

        layout_score_display.addWidget(self.score_mode_radio)
        layout_score_display.addWidget(self.score_mode_radio2)

        layout.addWidget(goup_score_display)

        score_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout_score_display.addSpacerItem(score_spacer)

        widget.setLayout(layout)
        return widget

    def create_midi_preferences(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(self.tr("MIDI preferences")))
        widget.setLayout(layout)
        return widget

    def create_audio_preferences(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(self.tr("Audio preference")))
        widget.setLayout(layout)
        return widget
    
    def create_shortcut_preferences(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # UI pour les préférences de raccourcis
        options_layout = QHBoxLayout()
        import_button = QPushButton(self.tr("Import"))
        export_button = QPushButton(self.tr("Export"))
        options_layout.addWidget(import_button)
        options_layout.addWidget(export_button)

        # listes des raccourcis (2 colonnes)
        shortcuts_group = QListWidget()
        shortcuts_group.addItems([self.tr("Ctrl + N : New"),
                                  self.tr("Ctrl + O : Open"),
                                  self.tr("Ctrl + S : Save"),
                                  self.tr("Ctrl + Q : Quit"),
                                  self.tr("Ctrl + Z : Cancel"),
                                  self.tr("Ctrl + Y : Redo"),
                                  self.tr("Ctrl + C : Copy"),
                                  self.tr("Ctrl + V : Paste"),
                                  self.tr("Ctrl + X : Cut"),
                                  self.tr("Ctrl + A : Select all"),
                                  self.tr("Ctrl + F : Search"),
                                  self.tr("Ctrl + P : Print"),
                                  self.tr("Ctrl + E : Export"),
                                  self.tr("Ctrl + Shift + E : Export to PDF"),
                                  self.tr("Ctrl + Shift + S : Export to image"),
                                  self.tr("Ctrl + Shift + N : New score"), 
                                  self.tr("Trackpad : Zoom"),
                                  self.tr("Trackpad : Move score"),
                                  self.tr("Trackpad : Move view"),
                                  ])

        layout.addLayout(options_layout)
        layout.addWidget(shortcuts_group)

        widget.setLayout(layout)
        return widget
    
    def create_plugin_preferences(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(self.tr("Plug-in managers")))
        widget.setLayout(layout)
        return widget
    
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    dialog = PreferencesDialog()
    dialog.exec_()
    sys.exit(app.exec_())