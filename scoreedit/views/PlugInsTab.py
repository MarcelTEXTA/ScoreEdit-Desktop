import importlib
import pkgutil

from .. import plugins

class PluginLoader:
    def __init__(self):
        self.plugins = []

    def load_plugins(self):
        for module_info in pkgutil.iter_modules(plugins.__path__):
            if module_info.name == "plugin":
                continue
            module = importlib.import_module(f"{plugins.__name__}.{module_info.name}")
            if module not in self.plugins:
                self.plugins.append(module)

    def get_plugins(self):
        return self.plugins
