import json
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QFileDialog
from PyQt5.QtCore import Qt

class WelcomeDialog(QDialog):
    def __init__(self, parent=None, flags=None):
        super().__init__(parent)

        self.setWindowTitle(self.tr("Welcome !"))
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout(self)

        self.list_widget = QListWidget() # Liste des fichiers récents
        
        # self.list_widget.itemClicked.connect(self.item_clicked)
        layout.addWidget(self.list_widget)

        button_layout = QHBoxLayout()

        self.open_button = QPushButton(self.tr("Open"))
        self.open_button.clicked.connect(self.open_file)
        button_layout.addWidget(self.open_button)

        self.new_button = QPushButton(self.tr("New file"))
        self.new_button.clicked.connect(self.new)
        button_layout.addWidget(self.new_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def new(self):
        #ferme la fenêtre de bienvenue
        self.close()

    def open_file(self):
        # Ouvrir un fichier via un QFileDialog
        file_name, _ = QFileDialog.getOpenFileName(self, self.tr("Open a projetc"), "", "Score Files (*.score);;Xml music (*.xml);;All Files (*)")
        
        if file_name:
            try:
                with open(file_name, 'r') as file:
                    content = file.read()
                    
                    # Ajouter une méthode pour découper les objets JSON concaténés
                    json_objects = []
                    decoder = json.JSONDecoder()

                    pos = 0
                    while pos < len(content):
                        try:
                            obj, index = decoder.raw_decode(content, pos)
                            json_objects.append(obj)
                            pos = index
                        except ValueError as e:
                            print(f"Erreur de décodage à la position {pos}: {e}")
                            break

                    # Charger chaque objet JSON dans le canvas
                    for obj in json_objects:
                        self.score_editor.canvas.load_canvas_data(obj)

                    print(f"Fichier .score chargé avec succès : {file_name}")

            except json.JSONDecodeError as e:
                print(f"Erreur de décodage JSON dans le fichier .score : {e}")
            except Exception as e:
                print(f"Erreur lors de l'ouverture du fichier : {e}")
