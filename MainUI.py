import sys
import os
import json
import time
from PyQt5.QtWidgets import (QApplication,
                               QMainWindow,
                               QFrame,
                               QVBoxLayout,
                               QWidget,
                               QHBoxLayout,
                               QLabel,
                               QTabWidget,
                               QSizePolicy,
                               QSpacerItem,
                               QToolBox,
                               QSplitter,
                               QPushButton,
                               QMessageBox,
                               QSplashScreen)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QPropertyAnimation, QUrl, QTranslator
from PyQt5.QtWidgets import QFileDialog
from DecryptTab import DecryptTab
from MidiTab import MidiTab
from ManualScoreEditor import ManualScoreEditor
from ScoreEditor import ScoreEditor
from OptionsBar import OptionsBar
from WelcomeDialog import WelcomeDialog
from FirstWelcomeDialog import FirstWelcomeDialog
from TextEdit import TextEdit
from PlugInsTab import PluginLoader

class MainUI(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.setObjectName("MainUI")

        # self.first_open()
        # self.load()
        # self.OpenApp()

        main_layout = QVBoxLayout()

        self.title_bar = OptionsBar(self, main_window=self)

        main_layout.addWidget(self.title_bar)

        # Layout principal horizontal pour le contenu
        content_layout = QHBoxLayout()

        # Volet latéral
        self.sidebar = self.create_sidebar()
        content_layout.addWidget(self.sidebar)

        # Section droite : canvas + onglets
        right_layout = QVBoxLayout()

        # Utilisation de ScoreEditor
        self.score_editor = ScoreEditor()

        Splitter = QSplitter(Qt.Orientation.Vertical) # doit pouvoir être redimensionné
        Splitter.addWidget(self.score_editor)
        right_layout.addWidget(Splitter)

        # redimensionner les widgets
        Splitter.setSizes([100, 200])

        # Onglets sous le canvas
        self.tabs = self.create_tabs()
        content_layout.addLayout(right_layout)
        Splitter.addWidget(self.tabs)

        self.h_sidebar = QWebEngineView()
        # self.h_sidebar.setReadOnly(True)
        self.h_sidebar.setFixedWidth(350)
        self.h_sidebar.hide()  # Le volet est caché par défaut
        content_layout.addWidget(self.h_sidebar)

        # Appliquer le layout horizontal au widget central
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

        # Animation de la fenêtre
        self.init_animation()

    def load(self): # cette fonction charge les fichiers de configuration
        splash_pix = QPixmap("IconApp/app/splash_image.jpg")  # Image pour l'écran de démarrage
        splash = QSplashScreen(splash_pix)
        splash.showMessage("TEXTA music : Resource loading...", Qt.AlignBottom | Qt.AlignCenter, Qt.black)
        splash.show()

        # Simuler le chargement des ressources avec une boucle
        for i in range(1, 101):  # Charger en 100 étapes
            # Mettre à jour le message
            splash.showMessage(f"Loading : {i}%", Qt.AlignBottom | Qt.AlignCenter, Qt.white)
            QApplication.processEvents()  # Mise à jour de l'écran

            # Simuler un temps de chargement
            time.sleep(0.01)  # Attendre 20ms (0.02s) pour chaque étape

        # Charger les fichiers de configuration après l'écran de chargement
        
        with open('config.json', 'r') as f:
            data = json.load(f)
            
            # 1. Charger le thème
            if data.get('theme') == 'dark':
                with open('styles/style_2.css', 'r') as f:
                    self.setStyleSheet(f.read())
            elif data.get('theme') == 'compact':
                with open("styles/style_3.css", "r") as f:
                    self.setStyleSheet(f.read())
            elif data.get('theme') == 'glass':
                with open("styles/style_4.css", "r") as f:
                    self.setStyleSheet(f.read())
            else:
                with open('styles/style.css', 'r') as f:
                    self.setStyleSheet(f.read())

            # 2. Charger la langue
            if 'language' in data:
                self.language = data['language']
                # Assurez-vous que les traductions sont appliquées ici
                self.apply_language(self.language)
                pass

            # 3. Charger le nom d'utilisateur et mot de passe
            if 'username' in data:
                self.username = data['username']
                # Mettre à jour le champ de saisie du nom d'utilisateur si nécessaire
                # self.user_name_edit.setText(self.username)
                pass

            if 'password' in data:
                self.password = data['password']
                # Mettre à jour le champ de mot de passe si nécessaire
                # self.password_edit.setText(self.password)
                pass

            # 4. Charger le répertoire par défaut
            if 'default_directory' in data:
                self.default_directory = data['default_directory']
                # Mettre à jour le champ correspondant dans l'interface utilisateur si nécessaire
                # self.directory_edit.setText(self.default_directory)
                pass

            # 5. Charger le format par défaut
            if 'default_format' in data:
                self.default_format = data['default_format']
                # Mettre à jour les options de format dans l'interface
                # self.format_combobox.setCurrentText(self.default_format)
                pass

        splash.finish(self)  # Fermer l'écran de démarrage

    def apply_language(self, language):
        # Charger le fichier de traduction correspondant
        translator = QTranslator(self)
        if language == 'fr':
            translator.load("fr_FR.qm")  # Exemple : fichier de traduction français
        elif language == 'de':
            translator.load("de_DE.qm")  # Exemple : fichier de traduction allemand
        # Appliquer le traducteur
        QApplication.instance().installTranslator(translator)

    def OpenApp(self): # cette fonction vérifie si l'utilisateur à ouvert un fichier .score
        # condition qui détermine si l'utilisateur a ouvert un fichier .score
        if len(sys.argv) > 1 and sys.argv[1].endswith('.score'):
            # ouvrir le fichier .score
            self.score_editor.open_file(sys.argv[1])
        else:
            self.welcome_dialog = WelcomeDialog()
            self.welcome_dialog.exec()

    def first_open(self): # cette fonction vérifie si c'est la première fois que l'utilisateur ouvre l'application
        # si le fichier de configuration n'existe pas, on ouvre la boite de dialogue de bienvenue
        if not os.path.exists('config.json'):
            self.frist_welcome_dialog = FirstWelcomeDialog()
            self.frist_welcome_dialog.exec()

    def toggle_help_sidebar(self):
        """Afficher ou masquer le volet latéral d'aide."""
        if self.h_sidebar.isVisible():
            self.h_sidebar.hide()  # Cacher si déjà visible
        elif self.h_sidebar.url() == QUrl('url/help.html'):
            self.h_sidebar.show()  # Afficher le volet
        else:
            html_path = os.path.abspath('url/help.html')
            local_url = QUrl.fromLocalFile(html_path)
            self.h_sidebar.setUrl(local_url)
            self.h_sidebar.show()  # Afficher le volet

    def toggle_acount_sidebar(self):
        if self.h_sidebar.isVisible():
            self.h_sidebar.hide()
        elif self.h_sidebar.url() == QUrl('url/account.html'):
            self.h_sidebar.show()
        else:
            html_path = os.path.abspath('url/account.html')
            local_url = QUrl.fromLocalFile(html_path)
            self.h_sidebar.setUrl(local_url)
            self.h_sidebar.show()
            
    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFrameShape(QFrame.StyledPanel)
        sidebar.setFixedWidth(250)

        sidebar_layout = QVBoxLayout()

        toolbox = QToolBox()
        sidebar_layout.addWidget(toolbox)

        # Onglet 1 : Bibliothèque d'images - Favoris
        tab_1_widget = QWidget()
        tab_1_layout = QVBoxLayout()

        image1 = QLabel()
        image1.setPixmap(QPixmap('image1.jpg'))
        image2 = QLabel()
        image2.setPixmap(QPixmap('image2.jpg'))

        tab_1_layout.addWidget(image1)
        tab_1_layout.addWidget(image2)

        tab_1_widget.setLayout(tab_1_layout)
        toolbox.addItem(tab_1_widget, 'Favourits')

        # Onglet 2 : Bibliothèque d'images - Récents
        tab_2_widget = QWidget()
        tab_2_layout = QVBoxLayout()

        image3 = QLabel()
        image3.setPixmap(QPixmap('image3.jpg'))
        image4 = QLabel()
        image4.setPixmap(QPixmap('image4.jpg'))

        tab_2_layout.addWidget(image3)
        tab_2_layout.addWidget(image4)

        tab_2_widget.setLayout(tab_2_layout)
        toolbox.addItem(tab_2_widget, 'Recents')

        # Onglet 3 : Bibliothèque d'images - Tonnalité
        tab_3_widget = QWidget()
        tab_3_layout = QVBoxLayout()

        image5 = QLabel()
        image5.setPixmap(QPixmap('image5.jpg'))

        tab_3_layout.addWidget(image5)

        tab_3_widget.setLayout(tab_3_layout)
        toolbox.addItem(tab_3_widget, 'key')

        # Onglet 4 : Bibliothèque d'images - Clés
        tab_4_widget = QWidget()
        tab_4_layout = QVBoxLayout()

        image6 = QLabel()
        image6.setPixmap(QPixmap('image6.jpg'))

        tab_4_layout.addWidget(image6)

        tab_4_widget.setLayout(tab_4_layout)
        toolbox.addItem(tab_4_widget, 'clef')

        # Onglet 5 : Bibliothèque d'images - Mesures
        tab_5_widget = QWidget()
        tab_5_layout = QVBoxLayout()

        image7 = QLabel()
        image7.setPixmap(QPixmap('image7.jpg'))

        tab_5_layout.addWidget(image7)
        toolbox.addItem(tab_5_widget, self.tr('Measures'))

        # Onglet 6 : Bibliothèque d'images - Symboles accords
        tab_6_widget = QWidget()
        tab_6_layout = QVBoxLayout()

        image8 = QLabel()
        image8.setPixmap(QPixmap('image8.jpg'))

        tab_6_layout.addWidget(image8)

        tab_6_widget.setLayout(tab_6_layout)
        toolbox.addItem(tab_6_widget, self.tr('Chord symbols'))

        # Onglet 7 : Bibliothèque d'images - Symboles guitares
        tab_7_widget = QWidget()
        tab_7_layout = QVBoxLayout()

        image9 = QLabel()
        image9.setPixmap(QPixmap('image9.jpg'))

        tab_7_layout.addWidget(image9)

        tab_7_widget.setLayout(tab_7_layout)
        toolbox.addItem(tab_7_widget, self.tr('Guitar symbols'))

        # Onglet 8 : Bibliothèque d'images - Symboles de notes
        tab_8_widget = QWidget()
        tab_8_layout = QVBoxLayout()

        image10 = QLabel()
        image10.setPixmap(QPixmap('image10.jpg'))

        tab_8_layout.addWidget(image10)

        tab_8_widget.setLayout(tab_8_layout)
        toolbox.addItem(tab_8_widget, self.tr('Note symbols'))

        # Onglet 9 : Bibliothèque d'image - Nuances
        tab_9_widget = QWidget()
        tab_9_layout = QVBoxLayout()

        image11 = QLabel()
        image11.setPixmap(QPixmap('image11.jpg'))

        tab_9_layout.addWidget(image11)

        tab_9_widget.setLayout(tab_9_layout)
        toolbox.addItem(tab_9_widget, self.tr('Dynamics'))

        # Onglet 10 : Bibliothèque d'images - Lignes
        tab_10_widget = QWidget()
        tab_10_layout = QVBoxLayout()

        image12 = QLabel()
        image12.setPixmap(QPixmap('image12.jpg'))

        tab_10_layout.addWidget(image12)

        tab_10_widget.setLayout(tab_10_layout)
        toolbox.addItem(tab_10_widget, self.tr('Lines'))

        # Onglet 11 : Bibliothèque d'images - Autres
        tab_11_widget = QWidget()
        tab_11_layout = QVBoxLayout()

        image13 = QLabel()
        image13.setPixmap(QPixmap('image13.jpg'))

        tab_11_layout.addWidget(image13)

        tab_11_widget.setLayout(tab_11_layout)
        toolbox.addItem(tab_11_widget, self.tr('Other'))

        # Onglet 12 : Bibliothèque d'images - Vos symboles
        tab_12_widget = QWidget()
        tab_12_layout = QVBoxLayout()

        add_image = QPushButton(self.tr("New symbol"))
        # add_image.clicked.connect(self.open_file)

        tab_12_layout.addWidget(add_image)

        tab_12_widget.setLayout(tab_12_layout)
        toolbox.addItem(tab_12_widget, self.tr('User symbols'))

        toolbox.setCurrentIndex(1)

        spacer_sidebar = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        sidebar_layout.addSpacerItem(spacer_sidebar)

        sidebar.setLayout(sidebar_layout)
        return sidebar

    def create_tabs(self):
        tabs = QTabWidget()
        tabs.setMaximumHeight(300)

        self.plugins_tab = QWidget()
        self.plugins_tab.setObjectName("TabItem")
        self.plugins_tab.setLayout(QVBoxLayout())

        tab1 = QWidget()
        tab1.setObjectName("TabItem")
        tab1_layout = QVBoxLayout()
        tab1_layout.addWidget(QLabel("Fonction en cours de dévelopement..."))
        tab1.setLayout(tab1_layout)

        # Ajout des onglets
        tabs.addTab(tab1, self.tr("Drawing"))
        tabs.addTab(ManualScoreEditor(), self.tr("Virtual key"))
        tabs.addTab(MidiTab(), self.tr("MIDI editor"))
        tabs.addTab(TextEdit(), self.tr("Text editor"))
        tabs.addTab(DecryptTab(), "Decrypter")
        tabs.addTab(self.plugins_tab, self.tr("Plug-ins"))

        self.plugin_loader = PluginLoader()
        self.plugin_loader.load_plugins()

        self.add_plugins_to_tab()

        return tabs
    
    def add_plugins_to_tab(self):
        plugin_layout = QVBoxLayout()  # Utilisation d'un layout vertical pour les plug-ins
    
        # Vérifier si plugins_tab a déjà un layout, sinon on le met
        if self.plugins_tab.layout() is None:
            self.plugins_tab.setLayout(plugin_layout)
        else:
            # Si un layout existe déjà, on réutilise le layout actuel sans le redéfinir
            plugin_layout = self.plugins_tab.layout()
        
        # Si tu as des plug-ins chargés via PluginLoader
        for plugin in self.plugin_loader.get_plugins():
            # Chaque plugin est un module, donc on peut accéder à la variable 'name' dans le module
            plugin_name = getattr(plugin, "name", "Unnamed Plugin")  # Par défaut, "Unnamed Plugin" si 'name' n'existe pas

            # Créer un label avec le nom du plug-in
            plugin_widget = QLabel(f"Plug-in: {plugin_name}")  # Afficher le nom du plug-in
            plugin_layout.addWidget(plugin_widget)

            # Si ton plugin a des interactions ou des widgets spécifiques, ajoute-les ici
            # Vérifier si la fonction 'run' existe
            if hasattr(plugin, "run"):
                plugin.run(self)  # Appeler la fonction 'run' du plugin

        self.plugins_tab.setLayout(plugin_layout)

    def init_animation(self):
        self.window_animation = QPropertyAnimation(self, b"windowOpacity")
        self.window_animation.setStartValue(0)
        self.window_animation.setEndValue(1)
        self.window_animation.setDuration(500)
        self.window_animation.start()

    def open_file(self):
        # Ouvre un fichier via un QFileDialog
        file_name, _ = QFileDialog.getOpenFileName(self, self.tr("Open file"), "", "Scores (*.xml *.musicxml)")
        if file_name:
            # Charger le fichier ici
            print(f"Fichier ouvert: {file_name}")

    def save_file(self):
        # Enregistre un fichier via un QFileDialog
        file_name, _ = QFileDialog.getSaveFileName(self, self.tr("Save at"), "", "Scores (*.xml *.musicxml)")
        if file_name:
            # Enregistrer le fichier ici
            print(f"File saved: {file_name}")