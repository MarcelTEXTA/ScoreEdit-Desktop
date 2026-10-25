import os
from PyQt5.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QWidget, QTextEdit, QHBoxLayout, QLabel
from PyQt5.QtWidgets import QFileDialog
from .PreviewDialog import PreviewDialog

class DecryptTab(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("TabItem")

        main_layout = QHBoxLayout()

        params_layout = QVBoxLayout()
        params_label = QLabel(self.tr("Partition analysis parameters :"))
        
        self.note_duration_input = self.create_input_field(self.tr("Note duration (ms)"))

        self.tempo_input = self.create_input_field(self.tr("Tempo (BPM)"))

        self.pitch_detection_input = self.create_input_field(self.tr("Note detection accuracy (%)"))

        analyse_button = QPushButton(self.tr("Score analysis"))
        analyse_button.clicked.connect(self.analyse_partition)

        params_layout.addWidget(params_label)
        params_layout.addWidget(self.note_duration_input)
        params_layout.addWidget(self.tempo_input)
        params_layout.addWidget(self.pitch_detection_input)
        params_layout.addStretch()

        convert_layout = QVBoxLayout()
        convert_label = QLabel(self.tr("Convert audio to score :"))

        self.audio_file_input = QTextEdit()
        self.audio_file_input.setPlaceholderText(self.tr("Audio file path..."))
        self.audio_file_input.setFixedHeight(40)

        self.select_audio_button = QPushButton(self.tr("Selecting an audio file"))
        self.select_audio_button.clicked.connect(self.open_file_dialog)
        
        self.convert_button = QPushButton(self.tr("Convert to partition"))
        self.convert_button.clicked.connect(self.convert_audio_to_score)

        convert_layout.addWidget(convert_label)
        convert_layout.addWidget(self.audio_file_input)
        convert_layout.addWidget(self.select_audio_button)
        convert_layout.addWidget(self.convert_button)
        convert_layout.addStretch()

        main_layout.addLayout(params_layout)
        main_layout.addLayout(convert_layout)

        self.setLayout(main_layout)

    def create_input_field(self, label_text):
        layout = QVBoxLayout()
        label = QLabel(label_text)
        input_field = QLineEdit()
        layout.addWidget(label)
        layout.addWidget(input_field)
        container = QWidget()
        container.setLayout(layout)
        return container

    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, self.tr("Select an audio file"), "", "audio file (*.mp3 *.wav *.flac);;all file (*)")
        
        if file_name:
            self.audio_file_input.setPlainText(file_name)

    def convert_audio_to_score(self):
        audio_file_path = self.audio_file_input.toPlainText()

        note_duration = self.note_duration_input.layout().itemAt(1).widget().text()
        tempo = self.tempo_input.layout().itemAt(1).widget().text()
        pitch_detection = self.pitch_detection_input.layout().itemAt(1).widget().text()

        if not all([audio_file_path, note_duration, tempo, pitch_detection]):
            print("Veuillez remplir tous les paramètres.")
            return

        print("Conversion de l'audio en partition...")

        print("Conversion terminée.")

    def analyse_partition(self):
        note_duration = self.note_duration_input.layout().itemAt(1).widget().text()
        tempo = self.tempo_input.layout().itemAt(1).widget().text()
        pitch_detection = self.pitch_detection_input.layout().itemAt(1).widget().text()

        if not all([note_duration, tempo, pitch_detection]):
            print("Veuillez remplir tous les paramètres.")
            return

        print("Analyse de la partition...")

        print("Analyse terminée.")

        self.preview_correction()

    def preview_correction(self):
        preview_dialog = PreviewDialog()
        preview_dialog.exec_()
        pass
