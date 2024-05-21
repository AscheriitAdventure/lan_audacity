import os
import sys
import logging
import logging.config
import json
import yaml
import xmltodict
import csv
import configparser
import string
import qtawesome as qta
from PyQt5.QtWidgets import (
    QMainWindow,
    QStatusBar,
    QToolBar,
    QLineEdit,
    QWidget,
    QSizePolicy,
    QAction,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


class SwitchFile:
    @staticmethod
    def json(abs_path: str) -> any:
        with open(abs_path, "r+", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def yaml(abs_path: str) -> any:
        with open(abs_path, "r+", encoding="utf-8") as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    @staticmethod
    def xml(abs_path: str) -> any:
        with open(abs_path, "r+", encoding="utf-8") as file:
            return xmltodict.parse(file.read())

    @staticmethod
    def csv(abs_path: str) -> any:
        with open(abs_path, "r+", encoding="utf-8") as file:
            return csv.DictReader(file)

    @staticmethod
    def txt(abs_path: str) -> any:
        with open(abs_path, "r+", encoding="utf-8") as file:
            return file.read()

    @staticmethod
    def ini(abs_path: str) -> any:
        config = configparser.ConfigParser()
        config.read(abs_path, encoding="utf-8")
        return config

    @staticmethod
    def conf(abs_path: str) -> any:
        config = configparser.ConfigParser()
        config.read(abs_path)
        return config


def current_dir():
    try:
        curr_path = os.getcwd()
        return curr_path
    except Exception as e:
        logging.error(
            f"Une erreur s'est produite lors de l'obtention du répertoire de travail actuel : {e}"
        )
        return "Analyse Erreur"


class ConfigurationFile:
    def __init__(self, abs_path: str):
        self.__abs_path: str = abs_path
        self.__file: str = os.path.basename(abs_path)
        self.__data = self.load_file()

    @property
    def abs_path(self) -> str:
        return self.__abs_path

    @abs_path.setter
    def abs_path(self, abs_path: str) -> None:
        if abs_path:
            self.__abs_path = abs_path
        else:
            logging.error(
                "Le chemin du fichier de configuration est vide ou non-renseigné."
            )

    @property
    def file(self) -> str:
        return self.__file

    @property
    def data(self) -> any:
        return self.__data

    def load_file(self) -> any:
        switch_file = SwitchFile()
        if os.path.exists(self.abs_path):
            return getattr(
                switch_file,
                ConfigurationFile.get_extension(self.abs_path),
                switch_file.txt,
            )(self.abs_path)
        else:
            logging.error(f"Le fichier de configuration {self.file} n'existe pas.")
            return None

    def get_value(self, key: str) -> str | None:
        if self.data:
            return self.data.get(key)
        else:
            logging.warning("Aucune configuration chargée ou trouvée.")
            return None

    @staticmethod
    def get_extension(abs_path: str) -> str:
        _, file_extension = os.path.splitext(abs_path)
        return file_extension.lower().strip(string.punctuation)


class LanguageApp:
    def __init__(self, file_manager: ConfigurationFile):
        self.data_manager = file_manager.data
        self.langManager: str = "english"
        self.langList = ["english", "français"]

    @property
    def language(self):
        return self.langManager

    @language.setter
    def language(self, lang: str):
        self.langManager = lang

    @property
    def language_list(self):
        return self.langList

    def get_textTranslate(self, key: str):
        for data in self.data_manager:
            if key in data["string"]:
                return data[self.language]


class ShortcutApp:
    def __init__(self, file_manager: ConfigurationFile):
        self.data_manager = file_manager.data

    def get_shortcut(self, key: str) -> str:
        for shortcut in self.data_manager:
            if shortcut["name"] == key:
                return shortcut["keys"]


class IconsApp:
    def __init__(self, file_manager: ConfigurationFile):
        self.data_manager = file_manager.data

    def get_icon(self, key: str) -> QIcon:
        for icon in self.data_manager:
            if icon["name"] == key:
                if icon["options"] is None:
                    ico_obj = qta.icon(*icon["platform_and_name"])
                else:
                    ico_obj = qta.icon(
                        *icon["platform_and_name"], options=icon["options"]
                    )
                return ico_obj


class MenuBarApp:
    def __init__(self, file_manager: ConfigurationFile):
        self.data_manager = file_manager.data

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


class MainApp(QMainWindow):
    def __init__(self, software_manager: ConfigurationFile, parent=None):
        super().__init__(parent)
        # Software Information
        self.softwareManager = software_manager
        # Data Language Manager
        self.langManager = LanguageApp(
            ConfigurationFile(
                f"{current_dir()}/{self.softwareManager.data['software']['conf']['translate_app']['path']}"
            )
        )
        # Data Shortcut Manager
        self.shortcutManager = ShortcutApp(
            ConfigurationFile(
                f"{current_dir()}/{self.softwareManager.data['software']['conf']['shortcuts_app']['path']}"
            )
        )
        # Data Icon Manager
        self.iconsManager = IconsApp(
            ConfigurationFile(
                f"{current_dir()}/{self.softwareManager.data['software']['conf']['icons_app']['path']}"
            )
        )
        # Data MenuBar Manager
        self.menuBarManager = MenuBarApp(
            ConfigurationFile(
                f"{current_dir()}/{self.softwareManager.data['software']['conf']['navBar_app']['path']}"
            )
        )

        # Set the Window title
        self.setWindowTitle(self.softwareManager.data["system"]["name"])
        # Set the Window icon
        self.setWindowIcon(self.iconsManager.get_icon("lan_audacity"))
        # Center the window
        self.centerWindow()
        # Set the navBar
        self.initUI_menu()
        # Set the Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Setting the GUI Information
        self.initUI_central()

        self.show()

    def centerWindow(self):
        # Obtenir la géométrie de l'écran
        screen_geometry = QApplication.desktop().screenGeometry()

        # Obtenir la géométrie de la fenêtre
        window_geometry = self.geometry()

        # Calculer la position pour centrer la fenêtre
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2

        # Déplacer la fenêtre
        self.move(x, y)

    def initUI_menu(self):
        # Add toolbars
        infobar = QToolBar(self)
        # Set the toolbar to a fixed top position
        self.addToolBar(Qt.TopToolBarArea, infobar)
        # Add a Spacer
        spacerI = QWidget()
        spacerI.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        infobar.addWidget(spacerI)

        toolsbar = QToolBar(self)
        # Set the toolbar to a fixed left position
        self.addToolBar(Qt.LeftToolBarArea, toolsbar)

        commandLine = QLineEdit("Lan Audacity")
        commandLine.setAlignment(Qt.AlignCenter)
        commandLine.setClearButtonEnabled(True)
        commandLine.setAcceptDrops(True)
        commandLine.setDragEnabled(True)
        commandLine.setMinimumWidth(75)
        commandLine.setMaximumWidth(250)
        # Add commandLine to infobar
        infobar.addWidget(commandLine)

        for menu in self.menuBarManager.data_manager:
            menu_obj = self.menuBar().addMenu(menu["menu"])
            for action in menu["actions"]:
                act_obj = QAction(action["name"], self)
                act_obj.setIcon(self.iconsManager.get_icon(action["icon_name"]))
                act_obj.setShortcut(
                    self.shortcutManager.get_shortcut(action["shortcut_name"])
                )
                act_obj.setStatusTip(action["status_tip"])
                # act_obj.triggered.connect(action['trigger'])
                menu_obj.addAction(act_obj)
                if action["name_low"] == "save_project":
                    menu_obj.addSeparator()
                elif action["name_low"] == "exit":
                    menu_obj.addSeparator()

            # Add Action to the infobar
            toggle_pSideBar = QAction(
                qta.icon("fa5s.window-maximize", rotated=270),
                "Toggle Primary Side Bar",
                self,
            )
            toggle_pSideBar.setShortcut("Ctrl+B")
            toggle_pSideBar.setStatusTip("Toggle Primary Side Bar")
            # toggle_pSideBar.triggered.connect(self.toggle_primary_side_bar)  # Define the function to be triggered

    def initUI_central(self):
        pass


if __name__ == "__main__":
    softw_manager = ConfigurationFile(current_dir() + "/conf/config_app.yaml")
    print(softw_manager.abs_path)
    path_log = (
        f"{current_dir()}/{softw_manager.data['software']['conf']['log_app']['path']}"
    )
    logs_manager = ConfigurationFile(path_log)

    logging.config.dictConfig(logs_manager.data)
    logger = logging.getLogger(__name__)

    logger.info(
        f"{softw_manager.data['system']['name']} - version {softw_manager.data['system']['version']}"
    )

    from qtpy.QtWidgets import QApplication

    app = QApplication(sys.argv)
    app.setApplicationName(softw_manager.data["system"]["name"])
    app.setApplicationVersion(softw_manager.data["system"]["version"])
    app.setOrganizationName(softw_manager.data["system"]["organization"])

    main_window = MainApp(softw_manager)
    main_window.show()

    sys.exit(app.exec_())
