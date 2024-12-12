from dev.project.src.classes.configurationFile import ConfigurationFile
import os
import typing
from qtpy.QtWidgets import QMainWindow, QMenuBar, QAction

class MenuBarManager:
    @typing.overload
    def __init__(self, parent: QMainWindow):
        self.parent = parent
        self.file_manager = ConfigurationFile(os.getenv("MENUBAR_FILE"))
        self.data_manager = self.file_manager.data
    
    @typing.overload
    def __init__(self, file_manager: ConfigurationFile) -> None:
        self.parent = None
        self.file_manager = file_manager
        self.data_manager = self.file_manager.data
    
    @typing.overload
    def __init__(self, parent: QMainWindow, file_manager: ConfigurationFile) -> None:
        self.parent = parent
        self.file_manager = file_manager
        self.data_manager = self.file_manager.data

    def menuBar(self):
        menuBar = self.parent.menuBar()
        for menu in self.data_manager:
            menuBar.addMenu(self.create_menu(menu))
        return menuBar
    
    def setParent(self, parent: QMainWindow) -> None:
        self.parent = parent
    
    def create_menu(self, menu: dict) -> QMenuBar:
        menu_bar = QMenuBar(self.parent)
        
        for obj in self.data_manager:
            menu_bar.addMenu(title=obj["title"]) # Add "Header" to the menu bar
            for q_act in obj["actions"]:
                q_action = QAction(q_act["name"], self.parent)
                q_action.setStatusTip(q_act["status_tip"])


        return menu_bar
    
    def get_menu_name(self, key: str) -> str:
        for menu_obj in self.data_manager:
            if menu_obj["name"] == key:
                return menu_obj["menu"]

    def get_one_menu(self, key: str) -> dict:
        for menu_obj in self.data_manager:
            if menu_obj["name"] == key:
                return menu_obj

    def get_one_action(self, key_menu: str, key_action) -> dict:
        menu = self.get_one_menu(key_menu)
        for action in menu["actions"]:
            if action["name_low"] == key_action:
                return action