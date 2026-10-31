import json
from PyQt5.QtWidgets import QMenu, QPushButton, QWidget, QHBoxLayout, QProgressDialog, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from .PreferencesDialog import PreferencesDialog
from .PrintDialog import PrintDialog
from .PreferencesDialog import PreferencesDialog
from .Canvas import Canvas
from .SysButton import SysButton

class OptionsBar(QWidget):
    def __init__(self, canvas, parent=None, main_window=None):
        super(OptionsBar, self).__init__(parent)
        # self.setFixedHeight(30)

        self.setObjectName("OptionsBar")

        self.canvas = canvas
        self.main_window = main_window

        self.menu_button = QPushButton(self.tr("Options"), self)
        self.menu_button.clicked.connect(self.show_menu)
        self.menu_button.setFlat(True)

        self.save_button = QPushButton(self.tr("Save"))
        self.save_button.clicked.connect(self.save_file)
        self.save_button.setShortcut('Ctrl+S')
        self.save_button.setFlat(True)

        self.open_file_button = QPushButton(self.tr("Open"))
        self.open_file_button.clicked.connect(self.open_file)
        self.open_file_button.setShortcut('Ctrl+O')
        self.open_file_button.setFlat(True)

        self.new_project_button = QPushButton(self.tr("New project"))
        self.new_project_button.clicked.connect(self.new_project)
        self.new_project_button.setShortcut('Ctrl+N')
        self.new_project_button.setFlat(True)

        self.print_button = QPushButton(self.tr("Print"))
        self.print_button.clicked.connect(self.print_score)
        self.print_button.setShortcut('Ctrl+P')
        self.print_button.setFlat(True)

        self.play_button = QPushButton(self.tr("Read score"))
        self.play_button.clicked.connect(self.ScorePlayer)
        self.play_button.setShortcut('F5')
        self.play_button.setFlat(True)

        self.help_button = QPushButton(self.tr("Help"))
        self.help_button.clicked.connect(self.main_window.toggle_help_sidebar)
        self.help_button.setShortcut('F1')
        self.help_button.setFlat(True)

        self.acount_button = QPushButton(self.tr("Account"))
        self.acount_button.clicked.connect(self.main_window.toggle_acount_sidebar)
        self.acount_button.setShortcut('Alt+C')
        self.acount_button.setFlat(True)

        # self.sys_button = SysButton()

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.help_button)
        button_layout.addWidget(self.acount_button)
        # button_layout.addWidget(self.sys_button)
        button_layout.setContentsMargins(0, 0, 0, 0)

        layout = QHBoxLayout()
        layout.addWidget(self.menu_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.open_file_button)
        layout.addWidget(self.new_project_button)
        layout.addWidget(self.print_button)
        layout.addStretch()
        layout.addLayout(button_layout)
        layout.setContentsMargins(5, 0, 5, 0)
        
        self.setLayout(layout)

        self.setMouseTracking(True)

        self.is_dragging = False

        self.maximized = False

    def ScorePlayer(self):
        print("Playing the score")
        message = QMessageBox(self)
        message.setWindowTitle(self.tr("Playing ..."))
        message.setText(self.tr("Playing the score"))
        message.exec_()

    def show_menu(self):
        # Crée le menu contextuel principal
        menu_button_actived = QMenu(self)

        # Menu Fichier
        file_menu = QMenu(self.tr("File"), self)
        
        open_action = file_menu.addAction(self.tr("Open a project"))
        new_project_action = file_menu.addAction(self.tr("Open project"))
        close_project_action = file_menu.addAction(self.tr("close project"))
        new_version_project_action = file_menu.addAction(self.tr("New version project"))
        save_action = file_menu.addAction(self.tr("Save"))
        save_as_action = file_menu.addAction(self.tr("Save at"))
        print_action = file_menu.addAction(self.tr("Print score"))

        file_menu.addSeparator()

        score_online_action = file_menu.addAction(self.tr("put the score online"))
        score_movie_action = file_menu.addAction(self.tr("Create an online video Partition"))

        file_menu.addSeparator()

        import_menu = QMenu(self.tr("Import"), self)
        import_audio_action = import_menu.addAction(self.tr("Audio file"))
        import_midi_action = import_menu.addAction(self.tr("MIDI file"))
        import_xml_action = import_menu.addAction(self.tr("XML file"))
        
        file_menu.addMenu(import_menu)

        export_menu = QMenu(self.tr("Export"), self)
        export_audio_action = export_menu.addAction(self.tr("Audio file"))
        export_picture_action = export_menu.addAction(self.tr("Pictures"))
        export_pdf_action = export_menu.addAction(self.tr("PDF file"))
        export_midi_action = export_menu.addAction(self.tr("MIDI file"))
        export_xml_action = export_menu.addAction(self.tr("XML file"))
        
        file_menu.addMenu(export_menu)

        file_menu.addSeparator()

        preferences_action = file_menu.addAction(self.tr("Preferences"))

        file_menu.addSeparator()
        
        exit_action = file_menu.addAction(self.tr("Quit"))

        open_action.triggered.connect(self.open_file)
        new_project_action.triggered.connect(self.new_project)
        save_action.triggered.connect(self.save_file)
        save_as_action.triggered.connect(self.save_at)
        print_action.triggered.connect(self.print_score)
        # score_online_action.triggered.connect(self.score_online)
        # score_movie_action.triggered.connect(self.score_movie)
        import_audio_action.triggered.connect(self.import_audio)
        # import_midi_action.triggered.connect(self.import_midi)
        # import_xml_action.triggered.connect(self.import_xml)
        # export_audio_action.triggered.connect(self.export_audio)
        # export_picture_action.triggered.connect(self.export_picture)
        # export_pdf_action.triggered.connect(self.export_pdf)
        # export_midi_action.triggered.connect(self.export_midi)
        # export_xml_action.triggered.connect(self.export_xml)
        preferences_action.triggered.connect(self.preferences)
        exit_action.triggered.connect(self.exit_app)

        menu_button_actived.addMenu(file_menu)

        # Menu Édition
        edit_menu = QMenu(self.tr("Edit"), self)
        
        annule_action = edit_menu.addAction(self.tr("Cancel"))
        retablir_action = edit_menu.addAction(self.tr("Redo"))
        historique_action = edit_menu.addAction(self.tr("History"))
        
        edit_menu.addSeparator()
        
        copy_action = edit_menu.addAction(self.tr("Copy"))
        cut_action = edit_menu.addAction(self.tr("Cut"))
        paste_action = edit_menu.addAction(self.tr("Paste"))
        
        edit_menu.addSeparator()
        
        select_action = edit_menu.addAction(self.tr("Select"))
        all_select_action = edit_menu.addAction(self.tr("Select all"))
        search_action = edit_menu.addAction(self.tr("Search / Remplace"))
        reorganize_action = edit_menu.addAction(self.tr("Réorganize"))
        mesure_auto_action = edit_menu.addAction(self.tr("Autmatic measures"))
        annotation_perfomance_action = edit_menu.addAction(self.tr("performance annotation"))
        
        annule_action.triggered.connect(self.annule)
        # retablir_action.triggered.connect(self.retablir)
        # copy_action.triggered.connect(self.copy)
        # cut_action.triggered.connect(self.cut)
        # paste_action.triggered.connect(self.paste)
        # select_action.triggered.connect(self.select)
        # all_select_action.triggered.connect(self.all_select)
        # search_action.triggered.connect(self.search)
        # reorganize_action.triggered.connect(self.reorganize)
        # mesure_auto_action.triggered.connect(self.mesure_auto)
        annotation_perfomance_action.triggered.connect(self.annotation_perfomance)
        
        menu_button_actived.addMenu(edit_menu)

        # Menu MIDI
        midi_menu = QMenu(self.tr("MIDI"), self)
        
        open_midi_edit_action = midi_menu.addAction(self.tr("Open MIDI editor"))
        open_rythme_edit_action = midi_menu.addAction(self.tr("Open rhythm editor"))
        control_edit_action = midi_menu.addAction(self.tr("Control editor"))
        saved_midi_action = midi_menu.addAction(self.tr("Recorder MIDI"))
        
        midi_menu.addSeparator()
        
        transpose_action = midi_menu.addAction(self.tr("Transpose"))
        setting_midi_action = midi_menu.addAction(self.tr("MIDI settings"))
        
        # open_midi_edit_action.triggered.connect(self.open_midi_edit)
        # open_rythme_edit_action.triggered.connect(self.open_rythme_edit)
        # control_edit_action.triggered.connect(self.control_edit)
        # saved_midi_action.triggered.connect(self.saved_midi)
        
        menu_button_actived.addMenu(midi_menu)

        # Menu Projet
        project_menu = QMenu(self.tr("Project"), self)
        
        new_partition_action = project_menu.addAction(self.tr("New score"))
        duplic_part_action = project_menu.addAction(self.tr("Duplic score"))
        new_version_score_action = project_menu.addAction(self.tr("New score version"))
        delete_score_action = project_menu.addAction(self.tr("Delete score"))
        delete_vierge_scores_action = project_menu.addAction(self.tr("delete all empty scores"))
        
        project_menu.addSeparator()
        
        library_action = project_menu.addAction(self.tr("Library"))
        marqueurs_action = project_menu.addAction(self.tr("Markers"))
        explorer_action = project_menu.addAction(self.tr("Explorer"))
        calc_tempo_action = project_menu.addAction(self.tr("tempo calculator"))
        timecode_curseur_action = project_menu.addAction(self.tr("Timecode cursor"))
        notepad_action = project_menu.addAction(self.tr("Notepad"))
        
        new_partition_action.triggered.connect(self.new_partition)
        # duplic_part_action.triggered.connect(self.duplic_part)
        # new_version_score_action.triggered.connect(self.new_version_score)
        # delete_score_action.triggered.connect(self.delete_score)
        # delete_vierge_scores_action.triggered.connect(self.delete_vierge_scores)
        # library_action.triggered.connect(self.library)
        # marqueurs_action.triggered.connect(self.marqueurs)
        # explorer_action.triggered.connect(self.explorer)
        # calc_tempo_action.triggered.connect(self.calc_tempo)
        # timecode_curseur_action.triggered.connect(self.timecode_curseur)
        # notepad_action.triggered.connect(self.notepad)
        
        menu_button_actived.addMenu(project_menu)

        # Menu Déchiffrer
        decrypt_menu = QMenu("Decrypter", self)
        
        decrypt_audio_action = decrypt_menu.addAction(self.tr("Decrypte audio file"))
        decrypt_midi_live_action = decrypt_menu.addAction(self.tr("Decrypte MIDI live"))
        decrypt_midi_action = decrypt_menu.addAction(self.tr("Decrypte MIDI file"))
        decrypt_audio_saved_action = decrypt_menu.addAction(self.tr("Decrypte audio recorder"))
        
        decrypt_menu.addSeparator()
        
        harmonic_annaliser_action = decrypt_menu.addAction(self.tr("Harmonic analysis"))
        tonn_annalyse_action = decrypt_menu.addAction(self.tr("Tonnage analysis"))
        scan_partition_decryption_action = decrypt_menu.addAction(self.tr("Scan score decryption"))
        hauteur_correction_action = decrypt_menu.addAction(self.tr("Height corrector"))
        
        # decrypt_audio_action.triggered.connect(self.decrypt_audio)
        # decrypt_midi_live_action.triggered.connect(self.decrypt_midi_live)
        # decrypt_midi_action.triggered.connect(self.decrypt_midi)
        # decrypt_audio_saved_action.triggered.connect(self.decrypt_audio_saved)
        # harmonic_annaliser_action.triggered.connect(self.harmonic_annaliser)
        # tonn_annalyse_action.triggered.connect(self.tonn_annalyse)
        # scan_partition_decryption_action.triggered.connect(self.scan_partition_decryption)
        
        menu_button_actived.addMenu(decrypt_menu)

        # Menu Partition
        score_menu = QMenu(self.tr("Score"), self)
        
        partition_option_action = score_menu.addAction(self.tr("Score options"))
        
        score_menu.addSeparator()
        
        page_mode_action = score_menu.addAction(self.tr("Page mode"))
        
        score_menu.addSeparator()
        
        group_ungroup_notes_action = score_menu.addAction(self.tr("Group / ungroup notes"))
        convert_ornament_note_action = score_menu.addAction(self.tr("Convert to ornamental note"))
        define_n_olet_action = score_menu.addAction(self.tr("Define N-olet"))
        split_action = score_menu.addAction(self.tr("Burst"))
        
        score_menu.addSeparator()
        
        mix_staves_action = score_menu.addAction(self.tr("Mixing litters"))
        extract_voice_action = score_menu.addAction(self.tr("Extract voice"))
        insert_legato_action = score_menu.addAction(self.tr("Insert Legato"))
        show_hide_action = score_menu.addAction(self.tr("Show / Hide"))
        invert_action = score_menu.addAction(self.tr("Reverse"))
        
        partition_option_action.triggered.connect(self.partition_option)
        # page_mode_action.triggered.connect(self.page_mode)
        # group_ungroup_notes_action.triggered.connect(self.group_ungroup_notes)
        # convert_ornament_note_action.triggered.connect(self.convert_ornament_note)
        # define_n_olet_action.triggered.connect(self.define_n_olet)
        # split_action.triggered.connect(self.split)
        # mix_staves_action.triggered.connect(self.mix_staves)
        # extract_voice_action.triggered.connect(self.extract_voice)
        # insert_legato_action.triggered.connect(self.insert_legato)
        # show_hide_action.triggered.connect(self.show_hide)
        # invert_action.triggered.connect(self.invert)
        
        menu_button_actived.addMenu(score_menu)

        # Menu Aide
        help_menu = QMenu(self.tr("Help"), self)
        
        open_doc_action = help_menu.addAction(self.tr("Documentation"))
        faq_action = help_menu.addAction(self.tr("Frequently asked questions"))
        
        help_menu.addSeparator()
        
        credits_action = help_menu.addAction(self.tr("Credits"))
        about_action = help_menu.addAction(self.tr("About TEXTA score edit"))
        
        # open_doc_action.triggered.connect(self.open_doc)
        # faq_action.triggered.connect(self.faq)
        # credits_action.triggered.connect(self.credits)
        about_action.triggered.connect(self.about)
        
        menu_button_actived.addMenu(help_menu)

        # Affiche le menu au niveau du bouton
        menu_button_actived.exec(self.menu_button.mapToGlobal(self.menu_button.rect().bottomLeft()))

    def open_file(self):
        # Ouvrir un fichier via un QFileDialog
        file_name, _ = QFileDialog.getOpenFileName(self, self.tr("Open file"), "", "Score Files (*.score);;All Files (*)")
        
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
                            print(f"Decoding error at position {pos}: {e}")
                            message_box = QMessageBox(self)
                            message_box.setIcon(QMessageBox.Critical)
                            message_box.setWindowTitle(self.tr("Error"))
                            message_box.setText(self.tr("Decoding error at position {pos}: {e}").format(pos=pos, error=e))
                            break

                    # Charger chaque objet JSON dans le canvas
                    for obj in json_objects:
                        self.score_editor.canvas.load_canvas_data(obj)

                    print(f"File .score successfully loaded : {file_name}")

            except json.JSONDecodeError as e:
                print(f"Erreur de décodage JSON dans le fichier .score : {e}")
            except Exception as e:
                print(f"Erreur lors de l'ouverture du fichier : {e}")
                # message box :
                message_box = QMessageBox(self)
                message_box.setIcon(QMessageBox.Critical)
                message_box.setWindowTitle("Erreur")
                message_box.setText(f"Erreur lors de l'ouverture du fichier : {e}")
                message_box.exec_()

    def new_project(self):
        try:
            self.main_window.new_project()  # Appel de la méthode new_project de MainUI
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), self.tr("Erreur lors de la création d'un nouveau projet : {e}").format(e=e))
    
    def save_file(self): # Si le fichier à déjà un repertoire, simplement enregistrer les modifications, sinon demander où enregistrer
        # Vérifier si le fichier a déjà un emplacement
        if hasattr(self, "file_name"):
            # Enregistrer les modifications dans le fichier existant
            with open(self.file_name, 'w') as file:
                # Récupérer les données du canvas via get_canvas_data
                data = self.canvas.get_canvas_data()
                
                # Enregistrer les données dans le fichier .score
                json.dump(data, file)
        else:
            self.save_at()

    def save_at(self): # demander où enregistrer le fichier dans tous les cas
        # Ouvre un dialogue pour demander où enregistrer le fichier
        file_name, _ = QFileDialog.getSaveFileName(self, self.tr("Save at"), "", "Score Files (*.score);;All Files (*)")
        
        if file_name:
            # Récupérer les données du canvas via get_canvas_data
            data = self.canvas.get_canvas_data()

            # Calculer l'effort total (par exemple, le nombre total de notes dans toutes les mesures)
            total_steps = sum(len(measure["notes"]) for measure in data["measures"])
            
            # Créer la fenêtre de dialogue pour afficher la progression
            progress_dialog = QProgressDialog(self.tr("Saving file ..."), self.tr("Cancel"), 0, total_steps, self)
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.show()
            
            # Enregistrer les données dans un fichier .score
            with open(file_name, 'w') as file:
                for i, measure in enumerate(data["measures"]):
                    for j, note in enumerate(measure["notes"]):
                        # Enregistrer la note dans le fichier
                        json.dump(note, file)

                        # Mettre à jour le texte de la barre de progression pour afficher la note en cours d'enregistrement
                        progress_dialog.setLabelText(self.tr("Enregistrement de la note {note['position']} dans la mesure {i + 1}").format(position=note['position'], measure=i + 1))
                        
                        # Mettre à jour la progression
                        progress_dialog.setValue(progress_dialog.value() + 1)

                        # Vérifier si l'utilisateur a annulé l'enregistrement
                        if progress_dialog.wasCanceled():
                            return  # Si l'utilisateur annule, on arrête l'enregistrement
            print(self.tr("Fichier enregistré sous : {file_name}").format(file_name=file_name))

    def print_score(self):
        try:
            self.print_dialog = PrintDialog()
            self.print_dialog.exec_()
        except Exception as e:
            print(f"Erreur lors de l'impression de la partition : {e}")
            # message box :
            message_box = QMessageBox(self)
            message_box.setIcon(QMessageBox.Critical)
            message_box.setWindowTitle(self.tr("Eror"))
            message_box.setText(self.tr("Erreur lors de l'impression de la partition : {e}").format(e=e))
            message_box.exec()

    def get_canvas_data(self):
        # Exemples de données étendues, avec plus de mesures et plus de notes.
        notes = [
            {"pitch": "C4", "duration": "quarter"},
            {"pitch": "D4", "duration": "half"},
            {"pitch": "E4", "duration": "quarter"},
            {"pitch": "F4", "duration": "whole"},
            {"pitch": "G4", "duration": "eighth"},
            # Tu peux ajouter ici plus de notes pour tester l'enregistrement
        ]
        
        # Exemple de mesures : Supposons que tu as 100 mesures, chaque mesure contenant des notes
        measures = [{"notes": notes} for _ in range(100)]  # Créer 100 mesures avec les mêmes notes
        
        return {
            "clef": "sol",  # Toujours la clé de sol
            "notes": notes,  # Les notes de la partition
            "measures": measures  # Les mesures de la partition (100 mesures ici)
        }
    
    def import_audio(self): #importation s'un fichier audio pour le decrypter via QFileDialog
        # Ouvre un dialogue pour sélectionner un fichier audio
        file_name, _ = QFileDialog.getOpenFileName(self, self.tr("Import an audio file"), "", "Audio Files (*.mp3 *.wav *.ogg)")
        
        if file_name:
            # Charger le fichier audio ici
            print(f"Fichier audio importé : {file_name}")

    def preferences(self):
        pref_dialog = PreferencesDialog(self)
        pref_dialog.exec_()

    def exit_app(self):
        self.main_window.close()

    def annule(self):
        print("Annuler")

    def annotation_perfomance(self): # ouvrir une fenetre pour ajouter des annotations de performance
        # ouvrir la fenetre d'annotation de performance
        print("Annotation de performance")
        annotation_perfomance_dialog = QMessageBox(self)
        annotation_perfomance_dialog.setWindowTitle("Annotation de performance")
        annotation_perfomance_dialog.setText("Ajouter des annotations de performance")

    def new_partition(self):
        try:
            # met une partition dans Canvas
            Canvas.add_staff(self, painter, x, y)
        except Exception as e:
            print(f"Erreur lors de la création d'une nouvelle partition : {e}")
            # message box :
            message_box = QMessageBox(self)
            message_box.setIcon(QMessageBox.Critical)
            message_box.setWindowTitle(self.tr("Error"))
            message_box.setText(self.tr("Erreur lors de la création d'une nouvelle partition, contactez l'administrateur : {e}").format(e=e))
            message_box.exec_()
        
    def partition_option(self):
        # ouvre PreferencesDialog pour les options de partition
        pref_dialog = PreferencesDialog(self)

        # Afficher uniquement les options de partition
        pref_dialog.create_score_preferences()

        pref_dialog.exec_()

    def about(self):
        # boite de dialogue pour afficher les informations sur l'application
        about_dialog = QMessageBox(self)
        about_dialog.setWindowTitle(self.tr("About TEXTA score edit"))
        about_dialog.setText("""TEXTA score edit - Éditeur de partitions musicales
                             
Version 1.1.0 dev preview - Version du noyau 3.9.1
                             
© 2025 TEXTA compagny. Tous droits réservés.

Développé par Ethan Macaluso""")
        about_dialog.exec_()