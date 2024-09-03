from src.classes.configurationFile import ConfigurationFile


class ShortcutApp:
    def __init__(self, file_manager: ConfigurationFile):
        self.data_manager = file_manager.data

    def get_shortcut(self, key: str) -> str:
        for shortcut in self.data_manager:
            if shortcut["name"] == key:
                return shortcut["keys"]