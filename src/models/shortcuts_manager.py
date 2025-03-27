from typing import Optional
import qtawesome as qta

from .factory_conf_file import FactoryConfFile


class ShortcutsManager(FactoryConfFile):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path, FactoryConfFile.RWX.READ)
        self.action_file(self.rw_mode)

    def get_shortcut(self, shortcut_name: str) -> Optional[str]:
        for data in self.file_data:
            if data["name"] == shortcut_name:
                return data["keys"]
        return None
