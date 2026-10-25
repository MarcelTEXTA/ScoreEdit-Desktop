import sys
import os
import json
import time
from PyQt5.QtWidgets import (QApplication,
                            QMainWindow,
                            QVBoxLayout,
                            QWidget,
                            QHBoxLayout,
                            QLabel,
                            QSplitter,
                            QSplashScreen)
from PyQt5.QtGui import QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QPropertyAnimation, QUrl, QTranslator
from PyQt5.QtWidgets import QFileDialog
from views import DecryptTab as DecryptTab
from views import MidiTab as MidiTab
from views import ManualScoreEditor as ManualScoreEditor
from views import ScoreEditor as ScoreEditor
from views import OptionsBar as OptionsBar
from views import WelcomeDialog as WelcomeDialog
from views import FirstWelcomeDialog as FirstWelcomeDialog
from views import TextEdit as TextEdit
from views.PlugInsTab import PluginLoader as PluginLoader
from views import Sidebar as Sidebar
from views import Tabs as Tabs

class MainWindow(QMainWindow):
    def __init__(self, main_window=None):
        super().__init__()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        self.title_bar = OptionsBar.OptionsBar(self, main_window=self)
        main_layout.addWidget(self.title_bar)

        content_layout = QHBoxLayout()

        self.sidebar = Sidebar.Sidebar()
        content_layout.addWidget(self.sidebar)

        right_layout = QVBoxLayout()
        
        self.score_editor = ScoreEditor.ScoreEditor()
        self.tabs = Tabs.Tabs()
        
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(self.score_editor)
        splitter.addWidget(self.tabs)
        splitter.setSizes([100, 200])
        
        right_layout.addWidget(splitter)
        content_layout.addLayout(right_layout)

        self.h_sidebar = QWebEngineView()
        self.h_sidebar.setFixedWidth(350)
        self.h_sidebar.hide()
        content_layout.addWidget(self.h_sidebar)

        main_layout.addLayout(content_layout)

        self.init_animation()

    def load(self):
        splash_pix = QPixmap("IconApp/app/splash_image.jpg")
        splash = QSplashScreen(splash_pix)
        splash.showMessage("The MarcelHosting : Resource loading...", Qt.AlignBottom | Qt.AlignCenter, Qt.black)
        splash.show()

        for i in range(1, 101):
            splash.showMessage(f"Loading : {i}%", Qt.AlignBottom | Qt.AlignCenter, Qt.white)
            QApplication.processEvents()

            time.sleep(0.01)
        
        with open('config.json', 'r') as f:
            data = json.load(f)
            
            if data.get('theme') == 'dark':
                with open('styles/style2.css', 'r') as f:
                    self.setStyleSheet(f.read())
            elif data.get('theme') == 'compact':
                with open("styles/style3.css", "r") as f:
                    self.setStyleSheet(f.read())
            elif data.get('theme') == 'glass':
                with open("styles/style4.css", "r") as f:
                    self.setStyleSheet(f.read())
            elif data.get('theme') == 'light':
                with open('styles/style.css', 'r') as f:
                    self.setStyleSheet(f.read())

            if 'language' in data:
                self.language = data['language']
                self.apply_language(self.language)
                pass

            if 'username' in data:
                self.username = data['username']
                pass

            if 'password' in data:
                self.password = data['password']
                pass

            if 'default_directory' in data:
                self.default_directory = data['default_directory']
                pass

            if 'default_format' in data:
                self.default_format = data['default_format']
                pass

        splash.finish(self)

    def apply_language(self, language):
        translator = QTranslator(self)
        if language == 'fr':
            translator.load("fr_FR.qm")
        elif language == 'de':
            translator.load("de_DE.qm")
        QApplication.instance().installTranslator(translator)

    def OpenApp(self):
        if len(sys.argv) > 1 and sys.argv[1].endswith('.score'):
            self.score_editor.open_file(sys.argv[1])
        else:
            self.welcome_dialog = WelcomeDialog.WelcomeDialog()
            self.welcome_dialog.exec()

    def first_open(self):
        if not os.path.exists('config.json'):
            self.frist_welcome_dialog = FirstWelcomeDialog()
            self.frist_welcome_dialog.exec()

    def toggle_help_sidebar(self):
        """Afficher ou masquer le volet latéral d'aide."""
        if self.h_sidebar.isVisible():
            self.h_sidebar.hide()
        elif self.h_sidebar.url() == QUrl('url/help.html'):
            self.h_sidebar.show()
        else:
            html_path = os.path.abspath('url/help.html')
            local_url = QUrl.fromLocalFile(html_path)
            self.h_sidebar.setUrl(local_url)
            self.h_sidebar.show()

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
    
    def add_plugins_to_tab(self):
        plugin_layout = QVBoxLayout()  # Utilisation d'un layout vertical pour les plug-ins
    
        if self.plugins_tab.layout() is None:
            self.plugins_tab.setLayout(plugin_layout)
        else:
            plugin_layout = self.plugins_tab.layout()
        
        for plugin in self.plugin_loader.get_plugins():
            plugin_name = getattr(plugin, "name", "Unnamed Plugin")

            plugin_widget = QLabel(f"Plug-in: {plugin_name}")
            plugin_layout.addWidget(plugin_widget)

            if hasattr(plugin, "run"):
                plugin.run(self)

        self.plugins_tab.setLayout(plugin_layout)

    def init_animation(self):
        self.window_animation = QPropertyAnimation(self, b"windowOpacity")
        self.window_animation.setStartValue(0)
        self.window_animation.setEndValue(1)
        self.window_animation.setDuration(500)
        self.window_animation.start()

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, self.tr("Open file"), "", "Scores (*.xml *.musicxml)")
        if file_name:
            print(f"Fichier ouvert: {file_name}")

    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, self.tr("Save at"), "", "Scores (*.xml *.musicxml)")
        if file_name:
            print(f"File saved: {file_name}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow(main_window=None)
    main_window.first_open()
    main_window.load()
    main_window.OpenApp()
    main_window.show()
    sys.exit(app.exec_())