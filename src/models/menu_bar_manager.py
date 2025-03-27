from typing import Optional, List
import qtawesome as qta

from .factory_conf_file import FactoryConfFile
from .menu_bar_object import MenuBarObject


class MenuBarManager(FactoryConfFile):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path, FactoryConfFile.RWX.READ)
        self.action_file(self.rw_mode)

        self.menubar_object: List[MenuBarObject] = [
            MenuBarObject.from_dict(menu) for menu in self.file_data
        ]

    def get_menu_name(self, menu_name: str) -> Optional[str]:
        for data in self.file_data:
            if data["name"] == menu_name:
                return data["title"]
        return None

    def get_menu_object(self, menu_name: str) -> Optional[MenuBarObject]:
        for menu in self.menubar_object:
            if menu.title == menu_name:
                return menu
        return None

    def get_one_menu(self, menu_name: str) -> Optional[dict]:
        for data in self.file_data:
            if data["name"] == menu_name:
                return data
        return None

    def get_one_action(self, menu_name: str, action_name: str) -> Optional[dict]:
        menu = self.get_one_menu(menu_name)
        if menu is not None:
            for action in menu["actions"]:
                if action["name_low"] == action_name:
                    return action

        return None
