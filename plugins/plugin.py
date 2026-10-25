# plugins/plugin.py
class Plugin:
    def __init__(self, name):
        self.name = name  # Associer le nom du plugin

    def get_name(self):
        return self.name