from PyQt5.QtWidgets import QApplication, QComboBox, QPushButton, QVBoxLayout, QLabel, QDialog, QColorDialog, QSpinBox, QGroupBox, QCheckBox, QFontComboBox
from PyQt5.QtCore import QFile

class ThemeDialog(QDialog):
    def __init__(self, parent=None):
        super(ThemeDialog, self).__init__(parent)
        
        self.setWindowTitle(self.tr("Theme customization"))
        
        # Initialisation des variables
        self.bg_color = "#FFFFFF"
        self.text_color = "#000000"
        self.button_color = "#0078D4"
        self.border_color = "#CCCCCC"
        self.font_family = "Arial"
        self.font_size = 12
        self.opacity = 1.0
        self.rounded_borders = False
        self.button_shadow = False
        
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Section pour le choix du thème
        theme_group = QGroupBox("Sélectionner un thème", self)
        theme_layout = QVBoxLayout(theme_group)
        
        

        self.apply_button = QPushButton(self.tr("Apply"))
        self.apply_button.clicked.connect(self.apply_theme)
        
        theme_layout.addWidget(self.comboBox)
        theme_layout.addWidget(self.apply_button)
        
        # Ajouter la section thème au layout principal
        layout.addWidget(theme_group)

    def apply_theme(self):
        """Charge et applique le style du fichier sélectionné."""
        qss_file = self.comboBox.currentData()
        self.load_qss(qss_file)
        
    def load_qss(self, qss_file):
        """Charge le fichier QSS et applique le style à l'application."""
        file = QFile(qss_file)
        if file.open(QFile.ReadOnly | QFile.Text):
            qss = file.readAll().data().decode()
            QApplication.instance().setStyleSheet(qss)
        file.close()
