import importlib
import os

class PluginLoader:
    def __init__(self):
        self.plugins = []

    def load_plugins(self):
        plugin_dir = "plugins"  # Le dossier où sont stockés les plug-ins
        for filename in os.listdir(plugin_dir):
            if filename.endswith(".py"):
                module_name = filename[:-3]  # Supprimer le ".py" pour obtenir le nom du module
                module = importlib.import_module(f"plugins.{module_name}")
                self.plugins.append(module)

    def get_plugins(self):
        return self.plugins
