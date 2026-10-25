from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QLabel
from .ManualScoreEditor import ManualScoreEditor
from .MidiTab import MidiTab
from .TextEdit import TextEdit
from .DecryptTab import DecryptTab
from .PlugInsTab import PluginLoader

class Tabs(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMaximumHeight(300)
        
        self.plugins_tab = QWidget()
        self.plugins_tab.setObjectName("TabItem")
        self.plugins_tab.setLayout(QVBoxLayout())

        tab1 = QWidget()
        tab1.setObjectName("TabItem")
        tab1_layout = QVBoxLayout()
        tab1_layout.addWidget(QLabel("Fonction en cours de dévelopement..."))
        tab1.setLayout(tab1_layout)

        self.addTab(tab1, self.tr("Drawing"))
        self.addTab(ManualScoreEditor(), self.tr("Virtual key"))
        self.addTab(MidiTab(), self.tr("MIDI editor"))
        self.addTab(TextEdit(), self.tr("Text editor"))
        self.addTab(DecryptTab(), "Decrypter")
        self.addTab(self.plugins_tab, self.tr("Plug-ins"))

        # self.plugin_loader = PluginLoader()
        # self.plugin_loader.load_plugins()

        # self.add_plugins_to_tab()
