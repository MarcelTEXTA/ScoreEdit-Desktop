from PyQt5.QtWidgets import QWidget, QSizePolicy, QFrame, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QImage, QIcon
from PyQt5.QtCore import Qt, QPoint, QSize

# la canvas dois avoir une grille pour mettre les notes dans les lignes et interlignes de la portée
class Canvas(QWidget):
    def __init__(self, parent=None, score_editor=any):
        super().__init__(parent)
        # self.setMinimumSize(100, 350)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) # Ajuster la taille du canvas
        self.measure_positions = [QPoint(50, 50)]  # Première mesure par défaut
        self.num_staff_lines = 5  # Nombre de lignes dans la portée
        self.measure_width = 200  # Largeur de chaque mesure
        self.staff_spacing = 40   # Espacement entre les portées
        # arrirer plan transparent
        color = QColor(255, 255, 255, 0)
        self.setAutoFillBackground(True)

        self.clef = 'sol'
        self.accidentals = []
        self.notes = []
        self.tool = 'insertion' # outil par défault

        self.current_measure_note_value = 0

        self.score_editor = score_editor

        self.note_type = 'noire'  # Type de note par défaut

    def set_tool(self, mode):
        """Changer l'outil actif."""
        self.tool = mode
        print(f"Mode de l'outil défini sur : {self.tool}")  # Pour le débogage

    def set_time_signature(self, beats, note_value):
        """Definir la signature temporelle; exemple (4, 4) pour 4/4"""
        self.time_signature = (beats, note_value)
        self.update()

    def load_canvas_data(self, data): # dois charger les données du fichier dans le canvas
        """Charger les données du fichier dans le canvas."""
        self.clef = data.get("clef", None)
        self.accidentals = data.get("accidentals", [])
        self.measure_positions = [QPoint(measure["position"]["x"], measure["position"]["y"]) for measure in data.get("measures", [])]
        self.notes = []

        # Charger les notes dans chaque mesure
        for measure in data.get("measures", []):
            for note in measure["notes"]:
                position = QPoint(note["position"]["x"], note["position"]["y"])
                self.notes.append({'position': position, 'type': note["type"]})

        # Forcer la mise à jour du canvas pour redessiner
        self.update()

    def get_canvas_data(self): # dois récupérer les positions des notes, les types de notes, les altérations, la clé, mesure, signature temporelle, symboles
        """Récupère toutes les données du canvas pour les sauvegarder."""
        data = {
            "clef": self.clef,
            "accidentals": self.accidentals,
            "measures": [],
            "notes": [],
            "time_signature": self.time_signature,
            "symbols": []
        }
        
        # Créer une liste des mesures avec leurs notes
        for measure in self.measure_positions:
            # Filtrer les notes correspondant aux mesures dans la canvas
            measure_notes = [note for note in self.notes if note['position'].x() >= measure.x() and note['position'].x() < measure.x() + self.measure_width]
            
            # Ajouter la mesure et ses notes
            data["measures"].append({
                "position": measure,
                "notes": measure_notes,
                "symbols": [],
                "time_signature": self.time_signature,
                "key_signature": self.accidentals,
                "clef": self.clef
            })

        return data

    def set_clef(self, clef_type):
        """Définir la clé (clé de sol, clé de fa, etc.)."""
        self.clef = clef_type
        self.update()

    def add_accidental(self, accidental_type): # dois ajouter une altération (dièse, bémol), positionné dans la grille
        """Ajouter une altération (dièse, bémol)."""
        self.accidentals.append(accidental_type)
        self.update()

    def add_measure(self):
        last_measure = self.measure_positions[-1]
        new_measure_x = last_measure.x() + self.measure_width # + 10
        self.measure_positions.append(QPoint(new_measure_x, 50))
        self.update()

    def add_note(self, note_type, position):
        """Ajouter une note avec un type (noire, blanche, etc.)."""
        note_value = self.get_note_value(note_type)
        
        # Initialiser la signature temporelle si elle n'existe pas
        if not hasattr(self, 'time_signature'):
            self.time_signature = (4, 4)  # Par défaut à 4/4 si aucune signature temporelle n'est définie
        
        beats_per_measure = self.time_signature[0]  # Nombre de temps
        note_value_per_beat = 4 / self.time_signature[1]  # Valeur de la note par temps

        total_capacity = beats_per_measure * note_value_per_beat

        # Vérifier si l'ajout de cette note dépasse la mesure actuelle
        if self.current_measure_note_value + note_value <= total_capacity:
            self.notes.append({'position': position, 'type': note_type})
            self.current_measure_note_value += note_value
            self.update()
        else:
            # Ajouter une nouvelle mesure si la mesure actuelle est pleine
            self.add_measure()
            self.current_measure_note_value = note_value  # Réinitialiser la valeur des notes dans la nouvelle mesure
            self.notes.append({'position': position, 'type': note_type})
        self.update()

    def get_note_value(self, note_type): # calcule la valeur de la note en fonction de son type pour les mesures
        note_values = {
            'ronde' : 4,
            'blanche' : 2,
            'noire' : 1,
            'croche' : 0.5,
            'doubleCroche' : 0.25,
            'quatrupleCroche' : 0.125,
            'sextupleCroche' : 0.0625,
            'septupleCroche' : 0.03125,
        }
        return note_values.get(note_type, 0)

    def paintEvent(self, event): # si l'outil de dessin est activé, il doit dessiner les notes
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Dessiner la portée à une position donnée (par exemple 50, 50)
        self.draw_staff(painter, 50, 50)  # Vous pouvez ajuster x et y ici

        # Dessiner la clé de sol
        if self.clef:
            self.draw_clef(painter, self.clef)

        # Dessiner les altérations
        self.draw_accidentals(painter)

        # Dessiner les notes
        self.draw_notes(painter)

        # Dessiner les barres de mesure
        for position in self.measure_positions:
            self.draw_staff(painter, position.x(), position.y(), self.num_staff_lines)

    def draw_staff(self, painter, x, y, num_lines=5, line_spacing=10):
        """Dessiner les lignes de la portée ainsi que la grille qui est invisible à chaque mesures."""
        for i in range(num_lines):
            y_pos = y + i * line_spacing
            painter.drawLine(x, y_pos, x + self.measure_width, y_pos)  # Lignes horizontales de la portée
        # grille invisible
        self.draw_grid(painter, x, y, num_lines, line_spacing)

        # Séparer les mesures avec une ligne verticale
        painter.drawLine(x + self.measure_width, y, x + self.measure_width, y + (num_lines - 1) * line_spacing)

    def add_staff(self, painter, x, y):
        """Ajouter une portée en dessous."""
        self.draw_staff(painter, x, y)

    def draw_grid(self, painter, x, y, num_lines=5, line_spacing=10):
        """Dessiner la grille invisible de la portée."""
        for i in range(num_lines):
            y_pos = y + i * line_spacing
            painter.drawLine(x, y_pos, x + self.measure_width, y_pos)  # Lignes horizontales de la grille

    def draw_clef(self, painter, clef_type):
        """Dessiner la clé (Sol, Fa, etc.)."""
        font = QFont('Times', 30)
        painter.setFont(font)

        if clef_type == 'sol':
            painter.drawText(60, 85, '𝄞')  # Clé de Sol
        elif clef_type == 'fa':
            painter.drawText(60, 85, '𝄢')  # Clé de Fa
        elif clef_type == 'ut':
            painter.drawText(60, 85, '𝄡') # clé de Ut

    def draw_accidentals(self, painter): # dois dessiner les altérations (dièses, bémols) sur la portée (positionné dans la grille)
        """Dessiner les altérations (dièses, bémols) sur la portée."""
        font = QFont('Times', 20)
        painter.setFont(font)

        x = 100
        for accidental in self.accidentals:
            if accidental == '#': # dois répsecté la position des altérations pour les dièses
                painter.drawText(x, 65, '#')  # Dièse
                # position des dièses (Fa, Do, Sol, Ré, La, Mi, Si)
                if x == 100 or x == 140 or x == 180 or x == 220 or x == 260 or x == 300 or x == 340:
                    x += 20
                elif accidental == '##': # dois répsecté la position des altérations pour les doubles dièses
                    painter.drawText(x, 65, '##')  # Double dièse
                else:
                    x += 40
                
            elif accidental == 'b': # dois répsecté la position des altérations pour les bémols
                painter.drawText(x, 65, '♭')  # Bémol
                # position des bémols (Si, Mi, La, Ré, Sol, Do, Fa)
                if x == 100 or x == 140 or x == 180 or x == 220 or x == 260 or x == 300 or x == 340:
                    x += 20
                else:
                    x += 40

    def draw_measures(self, painter):
        """Dessiner les barres de mesure."""
        pen = QPen(QColor(0, 0, 0), 2)
        painter.setPen(pen)

        for measure in self.measure_positions:
            painter.drawLine(measure.x(), 50, measure.x(), 90)

    def set_tool(self, mode):
        self.tool = mode
        print(f"Outil défini sur : {self.tool}")

    def mousePressEvent(self, event): # dois ajouter une note sélectionné dans la grille si l'outil de dessin est activé
        position = event.pos()
        closest_line = self.get_closest_line(position.y())
        note_position = QPoint(position.x(), closest_line)
        
        if self.tool == 'insertion':
            if event.button() == Qt.LeftButton:
                mouse_x = event.x()
                mouse_y = event.y()
                closest_y = self.get_closest_line(mouse_y)

            elif event.button() == Qt.RightButton:
                pass  # Ne rien faire pour le clic droit

            note_type = self.score_editor.note_type  # Récupérer le type de note sélectionné dans l'éditeur de partition

            if note_type == 'whole':
                note_type = 'ronde'
            elif note_type == 'half':
                note_type = 'blanche'
            elif note_type == 'quarter':
                note_type = 'noire'
            elif note_type == 'eighth':
                note_type = 'croche'
            elif note_type == 'sixteenth':
                note_type = 'doubleCroche'
            elif note_type == 'thirty_second':
                note_type = 'quatrupleCroche'
            elif note_type == 'sixtuple':
                note_type = 'sextupleCroche'
                

            # Ajouter une note noire à la position cliquée
            self.add_note(note_type, QPoint(mouse_x, closest_y))

        elif self.tool == 'delet':
            self.delete_note_at_position(note_position)
        elif self.tool == 'colle':
            self.duplicate_note_at_position(note_position)
        elif self.tool == 'coupe':
            self.cut_note_at_position(note_position)
        elif self.tool == 'selection':
            self.select_note_at_position(note_position)

    def set_note_type(self, note_type):
        self.note_type = note_type

    def delete_note_at_position(self, position):
        """supprimer une note à la position donnée."""
        for note in self.notes:
            if note['position'] == position:
                self.notes.remove(note)
                self.update()
                break

    def duplicate_note_at_position(self, position):
        """Dupliquer une note à la position donnée."""
        for note in self.notes:
            if note['position'] == position:
                new_position = QPoint(position.x() + 20, position.y())
                new_note = {'position' : new_position, 'type': note['type']}
                self.note.append(new_note)
                self.update()
                break

    def cut_note_at_position(self, position):
        """Couper une note à la position donnée."""
        for note in self.notes:
            if note['position'] == position:
                note_value = self.get_note_value(note['type'])
                self.current_measure_note_value -= note_value
                self.notes.remove(note)
                self.update()
                break

    def select_note_at_position(self, position):
        """Sélectionner une note à la position donnée."""
        for note in self.notes:
            if note['position'] == position:
                print(f"Note sélectionnée : {note}")

                # changer la couleur de la note sélectionnée
                color = QColor(255, 0, 0, 255)
                self.setAutoFillBackground(True)

                # condition pour vérifier l'oject sélectionné
                if self.notes: # si la note est sélectionnée
                    # afficher une QFrame flottante :
                    float_frame = QFrame()
                    float_frame.setFrameShape(QFrame.StyledPanel)

                    layout_frame = QHBoxLayout(float_frame)

                    note_inf = QPushButton()
                    note_inf.setIcons(QIcon('IconApp/ToolBar/note_inf.png'))
                    note_inf.setIconSize(QSize(18, 18))
                    layout_frame.addWidget(note_inf)

                    note_sup = QPushButton()
                    note_sup.setIcons(QIcon('IconApp/ToolBar/note_sup.png'))
                    note_sup.setIconSize(QSize(18, 18))
                    layout_frame.addWidget(note_sup)

                    oct_inf = QPushButton()
                    oct_inf.setIcons(QIcon('IconApp/ToolBar/oct_inf.png'))
                    oct_inf.setIconSize(QSize(18, 18))
                    layout_frame.addWidget(oct_inf)

                    oct_sup = QPushButton()
                    oct_sup.setIcons(QIcon('IconApp/ToolBar/oct_sup.png'))
                    oct_sup.setIconSize(QSize(18, 18))
                    layout_frame.addWidget(oct_sup)

                elif self.accidentals:
                    pass
                elif self.measure_positions:
                    pass

                self.update()
                break

    def draw_notes(self, painter):
        """Dessiner les notes sur la portée."""
        font = QFont('Times', 20)
        painter.setFont(font)

        note_symbols = {
            'ronde': '𝅝',
            'blanche': '𝅗𝅥',
            'noire': '𝅘𝅥',
            'croche': '𝅘𝅥𝅮',
            'doubleCroche': '𝅘𝅥𝅯',
            'quatrupleCroche': '𝅘𝅥𝅰',
            'sextupleCroche': '𝅘𝅥𝅱',
            'septupleCroche': '𝅘𝅥𝅲',
        }

        for note in self.notes:
            x, y = note['position'].x(), note['position'].y()
            note_type = note['type']
            symbol = note_symbols.get(note_type, '')  # Récupère le symbole correspondant
            painter.drawText(x, y, symbol)
            if symbol:
                painter.drawText(x, y, symbol)

    def get_closest_line(self, y):
        """Trouver la ligne la plus proche sur la portée."""
        top_margin = 50
        line_spacing = 10
        # closest_line = round((y - top_margin) / line_spacing) * line_spacing + top_margin
        # return closest_line
        return round((y - top_margin) / line_spacing) * line_spacing + top_margin

    def resizeEvent(self, event):
        """Mettre à jour la taille du canvas en fonction des mesures."""
        if self.measure_positions:
            total_width = self.measure_positions[-1].x() + 150  # Largeur totale en fonction des mesures
            self.setFixedWidth(max(self.width(), total_width))  # Ajuste la largeur minimale du canvas
