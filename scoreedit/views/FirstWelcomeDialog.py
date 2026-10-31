import json
from PyQt5.QtWidgets import QComboBox, QDialog, QVBoxLayout, QRadioButton, QLabel, QPushButton, QCheckBox, QStackedWidget, QWidget, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt

class FirstWelcomeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Welcome back !")
        self.setGeometry(100, 100, 300, 200)

        self.selected_theme = "light"  # Valeur par défaut
        self.username = ""
        self.password = ""
        self.language = "en"  # Langue par défaut
        self.default_directory = "/home/user/Music/TextaScores"
        self.default_format = "score"

        # Layout principal
        layout = QVBoxLayout(self)

        # Multi-page avec QStackedWidget
        self.stacked_layout = QStackedWidget(self)
        layout.addWidget(self.stacked_layout)

        # Créer les pages
        self.page1 = self.create_page1()
        self.page2 = self.create_page2()
        self.page3 = self.create_page3()

        # Ajouter les pages au QStackedWidget
        self.stacked_layout.addWidget(self.page1)
        self.stacked_layout.addWidget(self.page2)
        self.stacked_layout.addWidget(self.page3)

        self.setLayout(layout)

    def create_page1(self):
        """Créer la première page."""
        page = QWidget()  # Créer un widget de page
        layout = QVBoxLayout(page)

        # Label de bienvenue
        label = QLabel("Welcome to TEXTA Score Edit Dev Preview!\n\nFollow the instructions to configure TEXTA score edit.\nThis version is currently under development.\nPlease provide us with your feedback so that we can improve the\nsoftware for you.", self)
        layout.addWidget(label)

        lang_combo = QComboBox()
        lang_combo.addItems(["English", "Français", "Deutsch", "Español", "Italiano", "Nederlands"])
        lang_combo.setCurrentText("English")
        lang_combo.currentIndexChanged.connect(lambda index: self.set_language(lang_combo.itemText(index)))
        layout.addWidget(lang_combo)

        # Bouton Next pour aller à la deuxième page
        next_button = QPushButton("Next >", self)
        next_button.clicked.connect(self.next_page)
        layout.addWidget(next_button)

        page.setLayout(layout)
        return page

    def create_page2(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel("Choose your default theme :", self)
        layout.addWidget(label)

        light_button = QRadioButton("Light", self)
        light_button.setChecked(True)
        light_button.toggled.connect(lambda: self.set_theme("light"))

        dark_button = QRadioButton("Dark", self)
        dark_button.toggled.connect(lambda: self.set_theme("dark"))

        compact_button = QRadioButton("Compact", self)
        compact_button.toggled.connect(lambda: self.set_theme("compact"))

        glass_button = QRadioButton("Glass", self)
        glass_button.toggled.connect(lambda: self.set_theme("glass"))

        os_button = QRadioButton("OS", self)
        os_button.toggled.connect(lambda: self.set_theme("os"))

        layout.addWidget(light_button)
        layout.addWidget(dark_button)
        layout.addWidget(compact_button)
        layout.addWidget(glass_button)
        layout.addWidget(os_button)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        back_button = QPushButton("< Back", self)
        back_button.clicked.connect(lambda: self.stacked_layout.setCurrentIndex(0))
        button_layout.addWidget(back_button)

        next_button = QPushButton("Next >", self)
        next_button.clicked.connect(lambda: self.stacked_layout.setCurrentIndex(2))
        button_layout.addWidget(next_button)

        page.setLayout(layout)
        return page

    def create_page3(self):
        """Créer la deuxième page."""
        page = QWidget()  # Créer un widget de page
        layout = QVBoxLayout(page)

        # Label de la deuxième page
        label = QLabel("Let's connect to your Xcloud acount!", self)
        layout.addWidget(label)

        user_name = QLineEdit(self)
        user_name.setPlaceholderText("Username")
        user_name.textChanged.connect(self.set_username)
        layout.addWidget(user_name)

        password = QLineEdit(self)
        password.setPlaceholderText("Password")
        password.setEchoMode(QLineEdit.Password)
        password.textChanged.connect(self.set_password)
        layout.addWidget(password)

        agree_checkbox = QCheckBox("I agree to the terms and conditions", self)
        layout.addWidget(agree_checkbox)

        button_layout = QHBoxLayout()

        back_button = QPushButton("< Back", self)
        back_button.clicked.connect(lambda: self.stacked_layout.setCurrentIndex(1))  # Aller à la première page
        button_layout.addWidget(back_button)

        # Bouton Finish pour fermer la fenêtre
        next_button = QPushButton("Finish", self)
        next_button.clicked.connect(lambda: self.accept())
        button_layout.addWidget(next_button)

        layout.addLayout(button_layout)

        page.setLayout(layout)
        return page
    
    def set_theme(self, theme):
        """Définit le thème sélectionné."""
        self.selected_theme = theme

    def set_username(self, username):
        """Enregistrer le nom d'utilisateur."""
        self.username = username

    def set_password(self, password):
        """Enregistrer le mot de passe."""
        self.password = password

    def set_language(self, language):
        """Définir la langue sélectionnée."""
        self.language = language

    def next_page(self):
        """Changer de page et afficher la page suivante."""
        self.stacked_layout.setCurrentIndex(1)  # Aller à la deuxième page

    def accept(self):
        """Fermer la boîte de dialogue."""
        super().accept()

        data = {
            'first_open': False,
            'theme': self.selected_theme,
            'username': self.username,
            'password': self.password,
            'language': self.language,
            'default_directory': self.default_directory,
            'default_format': self.default_format,
            # autre paramètres par défaut à ajouter
            'file_dialog': False,
            'experience_plus': False,
            'tooltips': True,
            'startup': False,
            'user_interface': 'horizontal',
            'animation': True,
            'score_display': 'horizontal',
            'shortcut': 'default',
        }

        with open('config.json', 'w') as f:
            json.dump(data, f)
