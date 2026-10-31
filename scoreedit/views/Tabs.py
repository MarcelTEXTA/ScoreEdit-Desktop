from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from .ManualScoreEditor import ManualScoreEditor
from .MidiTab import MidiTab
from .TextEdit import TextEdit
from .DecryptTab import DecryptTab
from .PlugInsTab import PluginLoader

class Tabs(QTabWidget):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window

        self.setMaximumHeight(300)
        
        self.plugins_tab = QWidget()
        self.plugins_tab.setObjectName("TabItem")
        self.plugins_tab.setLayout(QVBoxLayout())

        self.addTab(ManualScoreEditor(main_window), self.tr("Virtual key"))
        self.addTab(MidiTab(), self.tr("MIDI editor"))
        self.addTab(TextEdit(), self.tr("Text editor"))
        self.addTab(DecryptTab(), "Decrypter")
        self.addTab(self.plugins_tab, self.tr("Plug-ins"))

        self.plugin_loader = PluginLoader()
        self._load_plugin_widgets()

    def _load_plugin_widgets(self):
        layout = self.plugins_tab.layout()
        try:
            self.plugin_loader.load_plugins()
        except (ImportError, OSError) as error:
            QMessageBox.critical(self, self.tr("Plug-in error"), str(error))
            return
        if not self.plugin_loader.get_plugins():
            layout.addWidget(QLabel(self.tr("No plug-ins are installed.")))
            return
        for plugin in self.plugin_loader.get_plugins():
            name = getattr(plugin, "name", plugin.__name__.rsplit(".", 1)[-1])
            button = QPushButton(self.tr("Run {name}").format(name=name))
            if callable(getattr(plugin, "run", None)):
                button.clicked.connect(
                    lambda checked=False, current=plugin: self._run_plugin(current)
                )
            else:
                button.setEnabled(False)
            layout.addWidget(button)
        layout.addStretch()

    def _run_plugin(self, plugin):
        try:
            plugin.run(self.main_window)
        except Exception as error:
            QMessageBox.critical(self, self.tr("Plug-in error"), str(error))
