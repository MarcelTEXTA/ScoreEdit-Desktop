from PyQt5.QtWidgets import QWidget, QSizePolicy
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
from PyQt5.QtCore import Qt, QPoint, QPointF, QRectF

# la canvas dois avoir une grille pour mettre les notes dans les lignes et interlignes de la portée
class Canvas(QWidget):
    STAFF_LINE_SPACING = 10
    NOTE_STEP = STAFF_LINE_SPACING // 2

    def __init__(self, parent=None, score_editor=None):
        super().__init__(parent)
        # self.setMinimumSize(100, 350)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) # Ajuster la taille du canvas
        self.measure_positions = [QPoint(50, 50)]  # Première mesure par défaut
        self.num_staff_lines = 5  # Nombre de lignes dans la portée
        self.measure_width = 200  # Largeur de chaque mesure
        self.staff_spacing = 40   # Espacement entre les portées
        self.setAutoFillBackground(True)

        self.clef = 'sol'
        self.accidentals = []
        self.notes = []
        self.text_annotations = []
        self.tool = 'selection' # outil par défault

        self.current_measure_note_value = 0
        self.time_signature = (4, 4)
        self.selected_note_index = None
        self.clipboard = None
        self._undo_history = []
        self._redo_history = []
        self._dragging_note = False

        self.score_editor = score_editor

        self.note_type = 'noire'  # Type de note par défaut

    def set_tool(self, mode):
        """Changer l'outil actif."""
        self.tool = mode
        self.update()

    def set_note_type(self, note_type):
        self.note_type = note_type
        self.update()

    def _snapshot(self):
        return {
            "clef": self.clef,
            "accidentals": list(self.accidentals),
            "time_signature": tuple(self.time_signature),
            "measure_positions": [QPoint(point) for point in self.measure_positions],
            "notes": [
                {"position": QPoint(note["position"]), "type": note["type"]}
                for note in self.notes
            ],
            "text_annotations": [dict(item) for item in self.text_annotations],
        }

    def _record_undo(self):
        self._undo_history.append(self._snapshot())
        if len(self._undo_history) > 100:
            del self._undo_history[0]
        self._redo_history.clear()

    def _restore_snapshot(self, snapshot):
        self.clef = snapshot["clef"]
        self.accidentals = list(snapshot["accidentals"])
        self.time_signature = tuple(snapshot["time_signature"])
        self.measure_positions = [QPoint(point) for point in snapshot["measure_positions"]]
        self.notes = [
            {"position": QPoint(note["position"]), "type": note["type"]}
            for note in snapshot["notes"]
        ]
        self.text_annotations = [dict(item) for item in snapshot["text_annotations"]]
        self.current_measure_note_value = sum(
            self.get_note_value(note["type"]) for note in self.notes
        )
        self.selected_note_index = None
        self.update()

    def undo(self):
        if not self._undo_history:
            return
        self._redo_history.append(self._snapshot())
        self._restore_snapshot(self._undo_history.pop())

    def redo(self):
        if not self._redo_history:
            return
        self._undo_history.append(self._snapshot())
        self._restore_snapshot(self._redo_history.pop())

    def select_all(self):
        self.selected_note_index = None
        self._selected_note_indices = set(range(len(self.notes)))
        self.update()

    def copy_selected(self):
        selected = getattr(self, "_selected_note_indices", set())
        if self.selected_note_index is not None:
            selected = {self.selected_note_index}
        if selected:
            self.clipboard = [
                {
                    "position": QPoint(self.notes[index]["position"]),
                    "type": self.notes[index]["type"],
                }
                for index in sorted(selected)
                if index < len(self.notes)
            ]

    def cut_selected(self):
        self.copy_selected()
        selected = getattr(self, "_selected_note_indices", set())
        if self.selected_note_index is not None:
            selected = {self.selected_note_index}
        if not selected:
            return
        self._record_undo()
        self.notes = [note for index, note in enumerate(self.notes) if index not in selected]
        self._selected_note_indices = set()
        self.current_measure_note_value = sum(
            self.get_note_value(note["type"]) for note in self.notes
        )
        self.selected_note_index = None
        self._selected_note_indices = set()
        self.update()

    def paste(self):
        if not self.clipboard:
            return
        self._record_undo()
        for note in self.clipboard:
            self.notes.append(
                {
                    "position": QPoint(note["position"].x() + 20, note["position"].y() + 20),
                    "type": note["type"],
                }
            )
        self.current_measure_note_value = sum(
            self.get_note_value(note["type"]) for note in self.notes
        )
        self.update()

    def set_time_signature(self, beats, note_value):
        """Definir la signature temporelle; exemple (4, 4) pour 4/4"""
        self._record_undo()
        self.time_signature = (beats, note_value)
        self.update()

    def load_canvas_data(self, data):
        """Charger les données du fichier dans le canvas."""
        if not isinstance(data, dict):
            raise TypeError("Score data must be a JSON object.")

        measures = data.get("measures", [])
        if not isinstance(measures, list):
            raise ValueError("Score data must contain a list of measures.")

        clef = data.get("clef", "sol")
        accidentals = data.get("accidentals", [])
        if not isinstance(accidentals, list):
            raise ValueError("Score accidentals must be a list.")

        time_signature = data.get("time_signature", [4, 4])
        if not isinstance(time_signature, (list, tuple)) or len(time_signature) != 2:
            raise ValueError("Score time signature must contain two values.")
        if not all(isinstance(value, int) and value > 0 for value in time_signature):
            raise ValueError("Time signature values must be positive integers.")
        text_annotations = data.get("symbols", [])
        if not isinstance(text_annotations, list):
            raise ValueError("Score symbols must be a list.")
        if any(
            not isinstance(item, dict)
            or not isinstance(item.get("text"), str)
            or not isinstance(item.get("position"), dict)
            or "x" not in item["position"]
            or "y" not in item["position"]
            for item in text_annotations
        ):
            raise ValueError("Each score symbol must contain text and a position.")

        measure_positions = []
        notes = []
        for measure in measures:
            if not isinstance(measure, dict):
                raise ValueError("Each score measure must be a JSON object.")
            position = measure.get("position", {"x": 50, "y": 50})
            if not isinstance(position, dict) or "x" not in position or "y" not in position:
                raise ValueError("Each measure must have an x/y position.")
            measure_positions.append(QPoint(position["x"], position["y"]))

            measure_notes = measure.get("notes", [])
            if not isinstance(measure_notes, list):
                raise ValueError("Measure notes must be a list.")
            for note in measure_notes:
                if not isinstance(note, dict) or "type" not in note:
                    raise ValueError("Each score note must have a type and position.")
                note_position = note.get("position")
                if not isinstance(note_position, dict) or "x" not in note_position or "y" not in note_position:
                    raise ValueError("Each note must have an x/y position.")
                notes.append(
                    {
                        "position": QPoint(note_position["x"], note_position["y"]),
                        "type": note["type"],
                    }
                )

        self._undo_history.clear()
        self._redo_history.clear()
        self.selected_note_index = None
        self._selected_note_indices = set()
        self._dragging_note = False
        self.clef = clef
        self.accidentals = accidentals
        self.time_signature = tuple(time_signature)
        self.measure_positions = measure_positions or [QPoint(50, 50)]
        self.notes = notes
        self.text_annotations = [
            {
                "text": item["text"],
                "position": QPoint(
                    item["position"]["x"],
                    item["position"]["y"],
                ),
            }
            for item in text_annotations
        ]
        self.current_measure_note_value = sum(
            self.get_note_value(note["type"]) for note in notes
        )
        self.update()

    def clear_score(self):
        self.clef = "sol"
        self.accidentals = []
        self.notes = []
        self.text_annotations = []
        self.time_signature = (4, 4)
        self.measure_positions = [QPoint(50, 50)]
        self.current_measure_note_value = 0
        self.selected_note_index = None
        self._selected_note_indices = set()
        self._undo_history.clear()
        self._redo_history.clear()
        self.update()

    def get_canvas_data(self): # dois récupérer les positions des notes, les types de notes, les altérations, la clé, mesure, signature temporelle, symboles
        """Récupère toutes les données du canvas pour les sauvegarder."""
        time_signature = self.time_signature
        all_notes = [
            {
                "position": {
                    "x": note["position"].x(),
                    "y": note["position"].y(),
                },
                "type": note["type"],
            }
            for note in self.notes
        ]
        data = {
            "clef": self.clef,
            "accidentals": list(self.accidentals),
            "measures": [],
            "notes": all_notes,
            "time_signature": list(time_signature),
            "symbols": [
                {
                    "text": item["text"],
                    "position": {
                        "x": item["position"].x(),
                        "y": item["position"].y(),
                    },
                }
                for item in self.text_annotations
            ]
        }
        
        # Créer une liste des mesures avec leurs notes
        for measure in self.measure_positions:
            # Filtrer les notes correspondant aux mesures dans la canvas
            measure_notes = [
                note
                for note in all_notes
                if note["position"]["x"] >= measure.x()
                and note["position"]["x"] < measure.x() + self.measure_width
            ]
            
            # Ajouter la mesure et ses notes
            data["measures"].append({
                "position": {"x": measure.x(), "y": measure.y()},
                "notes": measure_notes,
                "symbols": [],
                "time_signature": list(time_signature),
                "key_signature": list(self.accidentals),
                "clef": self.clef
            })

        return data

    def set_clef(self, clef_type):
        """Définir la clé (clé de sol, clé de fa, etc.)."""
        self._record_undo()
        self.clef = clef_type
        self.update()

    def add_accidental(self, accidental_type): # dois ajouter une altération (dièse, bémol), positionné dans la grille
        """Ajouter une altération (dièse, bémol)."""
        self._record_undo()
        self.accidentals.append(accidental_type)
        self.update()

    def add_measure(self):
        self._record_undo()
        if not self.measure_positions:
            self.measure_positions.append(QPoint(50, 50))
        last_measure = self.measure_positions[-1]
        new_measure_x = last_measure.x() + self.measure_width # + 10
        self.measure_positions.append(QPoint(new_measure_x, 50))
        self.update()

    def add_note(self, note_type, position):
        """Ajouter une note avec un type (noire, blanche, etc.)."""
        note_value = self.get_note_value(note_type)
        if note_value <= 0:
            raise ValueError(f"Unsupported note type: {note_type}")
        self._record_undo()
        
        # Initialiser la signature temporelle si elle n'existe pas
        if not hasattr(self, 'time_signature'):
            self.time_signature = (4, 4)  # Par défaut à 4/4 si aucune signature temporelle n'est définie
        
        beats_per_measure = self.time_signature[0]  # Nombre de temps
        note_value_per_beat = 4 / self.time_signature[1]  # Valeur de la note par temps

        total_capacity = beats_per_measure * note_value_per_beat

        measure_index = max(
            (
                index
                for index, measure in enumerate(self.measure_positions)
                if measure.x() <= position.x()
            ),
            default=0,
        )
        measure = self.measure_positions[measure_index]
        measure_value = sum(
            self.get_note_value(note["type"])
            for note in self.notes
            if measure.x() <= note["position"].x() < measure.x() + self.measure_width
        )
        if measure_value + note_value > total_capacity:
            next_measure = self.measure_positions[measure_index + 1] if measure_index + 1 < len(self.measure_positions) else None
            if next_measure is None:
                self.measure_positions.append(
                    QPoint(measure.x() + self.measure_width, measure.y())
                )
                next_measure = self.measure_positions[-1]
            next_index = self.measure_positions.index(next_measure)
            left_margin = self._measure_left_margin(next_index)
            next_positions, _ = self._note_grid(next_index, note_type)
            next_x = next_positions[0] if next_positions else next_measure.x() + left_margin
            position = QPoint(next_x, position.y())
            measure = next_measure
            measure_value = sum(
                self.get_note_value(note["type"])
                for note in self.notes
                if measure.x() <= note["position"].x() < measure.x() + self.measure_width
            )
        if measure_value + note_value > total_capacity:
            return
        self.notes.append({'position': position, 'type': note_type})
        self.current_measure_note_value = sum(
            self.get_note_value(note["type"]) for note in self.notes
        )
        self.update()

    def get_note_value(self, note_type): # calcule la valeur de la note en fonction de son type pour les mesures
        note_values = {
            'ronde' : 4,
            'pause_ronde': 4,
            'blanche' : 2,
            'pause_blanche': 2,
            'noire' : 1,
            'pause_noire': 1,
            'croche' : 0.5,
            'pause_croche': 0.5,
            'doubleCroche' : 0.25,
            'quatrupleCroche' : 0.125,
            'sextupleCroche' : 0.0625,
            'septupleCroche' : 0.03125,
        }
        return note_values.get(note_type, 0)

    def paintEvent(self, event): # si l'outil de dessin est activé, il doit dessiner les notes
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for position in self.measure_positions:
            self.draw_staff(
                painter,
                position.x(),
                position.y(),
                self.num_staff_lines,
            )

        # Dessiner la clé de sol
        if self.clef:
            self.draw_clef(painter, self.clef)

        # Dessiner les altérations
        self.draw_accidentals(painter)

        # Dessiner les notes
        self.draw_notes(painter)

        painter.setPen(QPen(QColor(0, 0, 0), 1))
        painter.setFont(QFont("Sans Serif", 12))
        for item in self.text_annotations:
            position = item["position"]
            painter.drawText(position.x(), position.y(), item["text"])

    def draw_staff(self, painter, x, y, num_lines=5, line_spacing=10):
        """Dessiner une portée et afficher sa grille pendant l'insertion."""
        self.draw_grid(painter, x, y, num_lines, line_spacing)
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        for i in range(num_lines):
            y_pos = y + i * line_spacing
            painter.drawLine(x, y_pos, x + self.measure_width, y_pos)
        painter.drawLine(
            x + self.measure_width,
            y,
            x + self.measure_width,
            y + (num_lines - 1) * line_spacing,
        )

    def add_staff(self, painter, x, y):
        """Ajouter une portée en dessous."""
        self.draw_staff(painter, x, y)

    def _measure_left_margin(self, measure_index):
        return 50 if measure_index == 0 else 12

    def _measure_capacity(self):
        beats, denominator = self.time_signature
        return beats * 4 / denominator

    def _note_slots_per_measure(self, note_type):
        note_value = self.get_note_value(note_type)
        if note_value <= 0:
            return 0
        return max(1, round(self._measure_capacity() / note_value))

    def _measure_index_at_x(self, x: int) -> int:
        for index, measure in enumerate(self.measure_positions):
            if measure.x() <= x < measure.x() + self.measure_width:
                return index
        return min(
            range(len(self.measure_positions)),
            key=lambda index: abs(self.measure_positions[index].x() - x),
        )

    def _note_grid(self, measure_index: int, note_type: str) -> tuple[list[int], float]:
        measure = self.measure_positions[measure_index]
        slots = self._note_slots_per_measure(note_type)
        if slots == 0:
            return [], 0
        left = self._measure_left_margin(measure_index)
        cell_width = (self.measure_width - left) / slots
        positions = [
            measure.x() + left + round((slot + 0.5) * cell_width)
            for slot in range(slots)
        ]
        return positions, cell_width

    def _snap_note_x(self, x: int, measure_index: int, note_type: str) -> int:
        positions, _ = self._note_grid(measure_index, note_type)
        if not positions:
            return x
        return min(positions, key=lambda grid_x: abs(grid_x - x))

    def draw_grid(self, painter, x, y, num_lines=5, line_spacing=10):
        """Afficher les subdivisions rythmiques et les pas de hauteur à l'insertion."""
        if self.tool != "insertion":
            return

        measure_index = self._measure_index_at_x(x)
        note_positions, _ = self._note_grid(measure_index, self.note_type)
        grid_pen = QPen(QColor(115, 155, 185, 90), 1, Qt.PenStyle.DotLine)
        painter.setPen(grid_pen)
        grid_top = y - 2 * line_spacing
        grid_bottom = y + (num_lines + 1) * line_spacing
        for grid_y in range(grid_top, grid_bottom + 1, self.NOTE_STEP):
            painter.drawLine(x, grid_y, x + self.measure_width, grid_y)
        for grid_x in note_positions:
            painter.drawLine(grid_x, grid_top, grid_x, grid_bottom)

    def draw_clef(self, painter, clef_type):
        """Dessiner la clé (Sol, Fa, etc.)."""
        font = QFont('Times', 30)
        painter.setFont(font)

        if clef_type == 'sol':
            painter.drawText(60, 85, '𝄞')
        elif clef_type == 'fa':
            painter.drawText(60, 85, '𝄢')
        elif clef_type == 'ut':
            painter.drawText(60, 85, '𝄡')

    def draw_accidentals(self, painter):
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

    def mousePressEvent(self, event): # dois ajouter une note sélectionné dans la grille si l'outil de dessin est activé
        position = event.pos()
        measure_index = self._measure_index_at_x(position.x())
        measure = self.measure_positions[measure_index]
        closest_line = self.get_closest_line(position.y(), measure.y())
        note_position = QPoint(position.x(), closest_line)
        
        if self.tool == 'insertion':
            if event.button() != Qt.MouseButton.LeftButton:
                return
            note_type = self.note_type
            note_x = self._snap_note_x(position.x(), measure_index, note_type)
            self.add_note(note_type, QPoint(note_x, closest_line))

        elif self.tool == 'delet':
            self.delete_note_at_position(note_position)
        elif self.tool == 'colle':
            self.duplicate_note_at_position(note_position)
        elif self.tool == 'coupe':
            self.cut_note_at_position(note_position)
        elif self.tool == 'selection':
            index = self.note_index_at_position(note_position)
            if index is None:
                self.selected_note_index = None
                self._selected_note_indices = set()
                self._dragging_note = False
            else:
                self._record_undo()
                self.selected_note_index = index
                self._selected_note_indices = {index}
                self._dragging_note = True
            self.update()

    def mouseMoveEvent(self, event):
        if self._dragging_note and self.selected_note_index is not None:
            note = self.notes[self.selected_note_index]
            position = event.pos()
            measure_index = self._measure_index_at_x(position.x())
            measure = self.measure_positions[measure_index]
            note_x = self._snap_note_x(
                position.x(),
                measure_index,
                note["type"],
            )
            note["position"] = QPoint(
                note_x,
                self.get_closest_line(position.y(), measure.y()),
            )
            self.update()

    def mouseReleaseEvent(self, event):
        if self._dragging_note:
            self._dragging_note = False

    def note_index_at_position(self, position):
        for index, note in enumerate(self.notes):
            note_position = note["position"]
            if (
                abs(note_position.x() - position.x()) <= 14
                and abs(note_position.y() - position.y()) <= 7
            ):
                return index
        return None

    def delete_note_at_position(self, position):
        """supprimer une note à la position donnée."""
        index = self.note_index_at_position(position)
        if index is None:
            return
        self._record_undo()
        self.notes.pop(index)
        self.selected_note_index = None
        self.current_measure_note_value = sum(
            self.get_note_value(note["type"]) for note in self.notes
        )
        self.update()

    def duplicate_note_at_position(self, position):
        """Dupliquer une note à la position donnée."""
        index = self.note_index_at_position(position)
        if index is None:
            return
        self._record_undo()
        note = self.notes[index]
        self.notes.append(
            {
                "position": QPoint(note["position"].x() + 20, note["position"].y()),
                "type": note["type"],
            }
        )
        self.current_measure_note_value += self.get_note_value(note["type"])
        self.update()

    def cut_note_at_position(self, position):
        """Couper une note à la position donnée."""
        index = self.note_index_at_position(position)
        if index is None:
            return
        note_type = self.notes[index]["type"]
        split_types = {
            "ronde": "blanche",
            "blanche": "noire",
            "noire": "croche",
            "croche": "doubleCroche",
            "doubleCroche": "quatrupleCroche",
            "quatrupleCroche": "sextupleCroche",
            "sextupleCroche": "septupleCroche",
        }
        smaller_type = split_types.get(note_type)
        if smaller_type is None:
            return
        self._record_undo()
        note = self.notes[index]
        self.notes[index] = {"position": QPoint(note["position"]), "type": smaller_type}
        self.notes.append(
            {
                "position": QPoint(note["position"].x() + 20, note["position"].y()),
                "type": smaller_type,
            }
        )
        self.current_measure_note_value = sum(
            self.get_note_value(item["type"]) for item in self.notes
        )
        self.update()

    def select_note_at_position(self, position):
        """Sélectionner une note à la position donnée."""
        self.selected_note_index = self.note_index_at_position(position)
        self._selected_note_indices = (
            {self.selected_note_index}
            if self.selected_note_index is not None
            else set()
        )
        self.update()

    def transpose_selected(self, semitones):
        if self.selected_note_index is None:
            return
        self._record_undo()
        note = self.notes[self.selected_note_index]
        note["position"] = QPoint(
            note["position"].x(),
            note["position"].y() - (5 * semitones),
        )
        self.update()

    def transpose_selected_octave(self, octaves):
        if self.selected_note_index is None:
            return
        self._record_undo()
        note = self.notes[self.selected_note_index]
        note["position"] = QPoint(
            note["position"].x(),
            note["position"].y() - (35 * octaves),
        )
        self.update()

    def add_rest(self, position, note_type=None):
        rest_types = {
            "ronde": "pause_ronde",
            "blanche": "pause_blanche",
            "noire": "pause_noire",
            "croche": "pause_croche",
        }
        rest_type = rest_types.get(note_type or self.note_type, "pause_noire")
        self.add_note(rest_type, position)

    def add_chord(self, position):
        intervals = (-20, -10, 0)
        self._record_undo()
        for interval in intervals:
            self.add_note(self.note_type, QPoint(position.x(), position.y() + interval))

    def add_text(self, text, position):
        if not text.strip():
            return
        self._record_undo()
        self.text_annotations.append(
            {"text": text.strip(), "position": QPoint(position)}
        )
        self.update()

    def adjust_selected_pitch(self, semitones):
        self.transpose_selected(semitones)

    def delete_selected(self):
        self.cut_selected()

    def draw_notes(self, painter):
        """Dessiner des têtes de notes dimensionnées selon l'espacement rythmique."""
        rest_symbols = {
            "pause_ronde": "𝄻",
            "pause_blanche": "𝄼",
            "pause_noire": "𝄽",
            "pause_croche": "𝄾",
        }
        for index, note in enumerate(self.notes):
            x, y = note['position'].x(), note['position'].y()
            note_type = note['type']
            measure_index = self._measure_index_at_x(x)
            measure = self.measure_positions[measure_index]
            _, cell_width = self._note_grid(measure_index, note_type)
            head_width = min(12.0, max(3.0, cell_width * 0.7))
            head_height = min(8.0, max(3.0, head_width * 0.65))
            if index == self.selected_note_index:
                painter.setPen(QPen(QColor(200, 30, 30), 2))
            else:
                painter.setPen(QPen(QColor(0, 0, 0), 1))

            if note_type in rest_symbols:
                painter.setFont(QFont("Times", max(8, round(head_width * 1.5))))
                painter.drawText(x, y, rest_symbols[note_type])
                continue

            if note_type == "ronde" or note_type == "blanche":
                painter.setBrush(Qt.BrushStyle.NoBrush)
            else:
                painter.setBrush(QColor(0, 0, 0))
            self._draw_ledger_lines(
                painter,
                x,
                y,
                measure.y(),
                head_width,
            )

            painter.save()
            painter.translate(x, y)
            painter.rotate(-20)
            painter.drawEllipse(
                QRectF(
                    -head_width / 2,
                    -head_height / 2,
                    head_width,
                    head_height,
                )
            )
            painter.restore()

            note_value = self.get_note_value(note_type)
            if note_value <= 2:
                stem_up = y > measure.y() + 2 * self.STAFF_LINE_SPACING
                stem_x = x + head_width / 2 if stem_up else x - head_width / 2
                stem_end = y - 3 * self.STAFF_LINE_SPACING if stem_up else y + 3 * self.STAFF_LINE_SPACING
                painter.drawLine(round(stem_x), y, round(stem_x), stem_end)

                flag_count = {
                    "croche": 1,
                    "doubleCroche": 2,
                    "quatrupleCroche": 3,
                    "sextupleCroche": 4,
                    "septupleCroche": 5,
                }.get(note_type, 0)
                direction = 1 if stem_up else -1
                for flag in range(flag_count):
                    flag_y = stem_end + direction * flag * 4
                    flag_path = QPainterPath(QPointF(stem_x, flag_y))
                    flag_path.quadTo(
                        stem_x + 8,
                        flag_y + direction * 3,
                        stem_x + 7,
                        flag_y + direction * 8,
                    )
                    painter.drawPath(flag_path)
            painter.setBrush(Qt.BrushStyle.NoBrush)

    def _draw_ledger_lines(self, painter, x, y, staff_y, head_width):
        staff_top = staff_y
        staff_bottom = staff_y + (self.num_staff_lines - 1) * self.STAFF_LINE_SPACING
        ledger_left = round(x - head_width / 2 - 4)
        ledger_right = round(x + head_width / 2 + 4)

        if y < staff_top:
            ledger_y = staff_top - self.STAFF_LINE_SPACING
            while ledger_y >= y:
                painter.drawLine(ledger_left, ledger_y, ledger_right, ledger_y)
                ledger_y -= self.STAFF_LINE_SPACING
        elif y > staff_bottom:
            ledger_y = staff_bottom + self.STAFF_LINE_SPACING
            while ledger_y <= y:
                painter.drawLine(ledger_left, ledger_y, ledger_right, ledger_y)
                ledger_y += self.STAFF_LINE_SPACING

    def get_closest_line(self, y, staff_y=50):
        """Caler une hauteur sur une ligne ou un interligne de la portée."""
        return (
            round((y - staff_y) / self.NOTE_STEP) * self.NOTE_STEP
            + staff_y
        )

    def resizeEvent(self, event):
        """Mettre à jour la taille du canvas en fonction des mesures."""
        if self.measure_positions:
            total_width = self.measure_positions[-1].x() + 150
            self.setFixedWidth(max(self.width(), total_width))
