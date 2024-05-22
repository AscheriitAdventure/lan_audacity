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
import time
import shutil
import qtawesome as qta
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal as Signal, QDir, QFile, QIODevice
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


class Device:
    def __init__(
        self,
        device_ipv4: str,
        mask_ipv4: str,
        save_path: str,
        device_name: str = None,
        device_ipv6: str = None,
        mask_ipv6: str = None,
        device_type: str = None,
        device_os: str = None,
        device_model: str = None,
        device_brand: str = None,
        device_mac: str = None,
        device_gateway: str = None,
        device_dns: str = None,
        device_dhcp: str = None,
        device_snmp: str = None,
        device_ssh: str = None,
        device_logs: str = None,
        device_data: str = None,
    ):
        self.uuid = uuid.uuid4()
        self.name = device_name
        self.ipv4 = device_ipv4
        self.mask_ipv4 = mask_ipv4
        self.ipv6 = device_ipv6
        self.mask_ipv6 = mask_ipv6
        self.type = device_type
        self.os = device_os
        self.model = device_model
        self.brand = device_brand
        self.mac = device_mac
        self.gateway = device_gateway
        self.dns = device_dns
        self.dhcp = device_dhcp
        self.snmp = device_snmp
        self.ssh = device_ssh
        self.logs = device_logs
        self.data = device_data
        self.date_unix: float = time.time()
        self.last_update_unix: float = time.time()
        self.abs_path = f"{save_path}/{self.uuid}.json"

    def create_device(self):
        if not os.path.exists(self.abs_path):
            with open(self.abs_path, "w") as f:
                json.dump(self.__dict__, f, indent=4)
            return f"{self.name} is created"
        else:
            return f"{self.name} already exists"

    def open_device(self):
        if os.path.exists(self.abs_path):
            with open(self.abs_path, "r") as f:
                return json.load(f)
        else:
            return f"{self.name} doesn't exist"

    def save_device(self):
        if os.path.exists(self.abs_path):
            self.last_update_unix = time.time()
            with open(self.abs_path, "w") as f:
                json.dump(self.__dict__, f, indent=4)
            return f"{self.name} is saved"
        else:
            return f"{self.name} doesn't exist"

    def delete_device(self):
        if os.path.exists(self.abs_path):
            os.remove(self.abs_path)
            return f"{self.name} is deleted"
        else:
            return f"{self.name} doesn't exist"

    def ip_to_cidr(self):
        pass

    def cidr_to_ip(self):
        pass


class Network:
    def __init__(
        self,
        network_ipv4: str,
        network_mask_ipv4: str,
        save_path: str,
        network_name: str = None,
        network_ipv6: str = None,
        network_gateway: str = None,
        network_dns: str = None,
        network_dhcp: str = None,
        uuid: str = None,
    ):
        if uuid:
            self.uuid: str = uuid
        else:
            self.uuid: str = str(uuid.uuid4())
        self.name: str = network_name
        self.ipv4: str = network_ipv4
        self.mask_ipv4: str = network_mask_ipv4
        self.ipv6: str = network_ipv6
        self.gateway: str = network_gateway
        self.dns: str = network_dns
        self.dhcp: str = network_dhcp
        self.date_unix: float = time.time()
        self.last_update_unix: float = time.time()

        self.abs_path = f"{save_path}/{self.uuid}.json"
        self.devices = []

        self.create_network()

    def create_network(self):
        if not os.path.exists(self.abs_path):
            with open(self.abs_path, "w+") as f:
                json.dump(self.__dict__, f, indent=4)
            return f"{self.name} is created"
        else:
            return f"{self.name} already exists"

    def open_network(self):
        if os.path.exists(self.abs_path):
            with open(self.abs_path, "r") as f:
                return json.load(f)
        else:
            return f"{self.name} doesn't exist"

    def save_network(self):
        if os.path.exists(self.abs_path):
            self.last_update_unix = time.time()
            with open(self.abs_path, "w") as f:
                json.dump(self.__dict__, f, indent=4)
            return f"{self.name} is saved"
        else:
            return f"{self.name} doesn't exist"

    def add_device(self, device: Device):
        self.devices.append(device.uuid)
        self.last_update_unix = time.time()
        with open(self.abs_path, "w") as f:
            json.dump(self.__dict__, f, indent=4)
        return f"{device.name} is added to {self.name}"

    def remove_device(self, device: Device):
        self.devices.remove(device.uuid)
        self.last_update_unix = time.time()
        device.delete_device()
        with open(self.abs_path, "w") as f:
            json.dump(self.__dict__, f, indent=4)
        return f"{device.name} is removed from {self.name}"


class LanAudacity:
    def __init__(
        self,
        software_name: str,
        version_software: str,
        project_name: str,
        save_path: str,
        author: str = None,
    ):
        self.software = software_name
        self.version = version_software
        self.save_path = save_path
        self.char_table = "utf-8"
        self.project_name = project_name
        self.date_unix: float = time.time()
        self.last_update_unix: float = time.time()
        self.author = author
        self.abs_paths = {
            "conf": {"path": "conf", "folders": [], "files": []},
            "db": {
                "path": "db",
                "folders": ["interfaces", "desktop"],
                "files": [],
            },
            "logs": {"path": "logs", "folders": [], "files": ["lan_audacity.log"]},
            "pixmap": {"path": "pixmap", "folders": [], "files": []},
        }
        self.networks = None
        self.links = None
        self.devices = None
        self.pixmap = None

    def create_project(self) -> str:
        if not os.path.exists(f"{self.save_path}/{self.project_name}"):
            os.mkdir(f"{self.save_path}/{self.project_name}")
            with open(
                f"{self.save_path}/{self.project_name}/lan_audacity.json", "w"
            ) as f:
                json.dump(self.__dict__, f, indent=4)
            for key, value in self.abs_paths.items():
                os.mkdir(f"{self.save_path}/{self.project_name}/{value['path']}")
                if value["folders"]:
                    for folder in value["folders"]:
                        os.mkdir(
                            f"{self.save_path}/{self.project_name}/{value['path']}/{folder}"
                        )
                if value["files"]:
                    for file in value["files"]:
                        with open(
                            f"{self.save_path}/{self.project_name}/{value['path']}/{file}",
                            "w",
                        ) as f:
                            f.write("")
            return f"{self.project_name} is created"
        else:
            return f"{self.project_name} already exists"

    def delete_project(self) -> str:
        if os.path.exists(f"{self.save_path}/{self.project_name}"):
            try:
                shutil.rmtree(f"{self.save_path}/{self.project_name}")
                return f"{self.project_name} is deleted"
            except OSError as e:
                return f"Error remove {self.project_name} : {e}"
        else:
            return f"{self.project_name} doesn't exist"

    def add_network(self, network: Network) -> str:
        if self.networks is None:
            self.networks = {"path": "interfaces", "obj_ls": []}
        self.networks["obj_ls"].append(
            {
                "uuid": network.uuid,
                "name": network.name,
                "path": network.abs_path,
                "ls_devices": [],
            }
        )
        self.last_update_unix = time.time()
        with open(f"{self.save_path}/{self.project_name}/lan_audacity.json", "w") as f:
            json.dump(self.__dict__, f, indent=4)
        return f"{network.name} is added to {self.project_name}"

    def remove_network(self, network: Network) -> str:
        if self.networks is not None:
            self.networks["obj_ls"].remove(network.uuid)
            self.last_update_unix = time.time()
            with open(
                f"{self.save_path}/{self.project_name}/lan_audacity.json", "w"
            ) as f:
                json.dump(self.__dict__, f, indent=4)
            return f"{network.name} is removed from {self.project_name}"
        else:
            return f"{network.name} doesn't exist in {self.project_name}"

    def open_project(self) -> str:
        if os.path.exists(self.project_name):
            with open(
                f"{self.save_path}/{self.project_name}/lan_audacity.json", "r"
            ) as f:
                datas = json.load(f)
                self.software = datas["software"]
                self.version = datas["version"]
                self.save_path = datas["save_path"]
                self.char_table = datas["char_table"]
                self.project_name = datas["project_name"]
                self.date_unix = datas["date_unix"]
                self.last_update_unix = datas["last_update_unix"]
                self.author = datas["author"]
                self.abs_paths = datas["abs_paths"]
                # Construct all datas
            return f"{self.project_name} does exist"
        else:
            return f"{self.project_name} doesn't exist"

    def save_project(self) -> str:
        if os.path.exists(self.project_name):
            self.last_update_unix = time.time()
            with open(
                f"{self.save_path}/{self.project_name}/lan_audacity.json", "w"
            ) as f:
                json.dump(self.__dict__, f, indent=4)
            return f"{self.project_name} is saved"
        else:
            return f"{self.project_name} doesn't exist"

    def save_as_project(self, new_path: str, new_project_name: str) -> str:
        if os.path.exists(new_path):
            self.save_path = new_path
            os.rename(self.project_name, new_project_name)
            self.project_name = new_project_name
            with open(f"{new_path}/{self.project_name}/lan_audacity.json", "w") as f:
                json.dump(self.__dict__, f, indent=4)
            return f"{self.project_name} is saved as {new_project_name}"
        else:
            return f"{self.project_name} doesn't exist"


class NProjectDock(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Project")

        # layout
        layout = QGridLayout()
        self.setLayout(layout)

        # Title
        self.title = QLabel("New Project")
        self.title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(self.title, 0, 0, 1, 3)

        sep = QFrame(self)
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        layout.addWidget(sep, 1, 0, 1, 3)

        # Project Name
        self.project_name_label = QLabel("Name:")
        self.project_name = QLineEdit(self)
        self.project_name.setPlaceholderText("Project Name")
        layout.addWidget(self.project_name_label, 2, 0)
        layout.addWidget(self.project_name, 2, 1)

        # Author
        self.author_label = QLabel("Author:")
        self.author = QLineEdit(self)
        self.author.setPlaceholderText("Author")
        layout.addWidget(self.author_label, 3, 0)
        layout.addWidget(self.author, 3, 1)

        # Save Path
        self.save_path_label = QLabel("Path:")
        self.save_path_button = QPushButton(self)
        self.save_path_button.setIcon(qta.icon("mdi6.folder-open-outline", color="orange"))
        self.save_path_button.setToolTip("Select Save Path")
        self.save_path_text = QLineEdit()
        self.save_path_text.setReadOnly(True)
        layout.addWidget(self.save_path_label, 4, 0)
        layout.addWidget(self.save_path_text, 4, 1)
        layout.addWidget(self.save_path_button, 4, 2)
        self.save_path_button.clicked.connect(self.select_save_path)
        self.save_path = ""

        # Validate button
        self.validate_button = QPushButton("Validate")
        layout.addWidget(self.validate_button, 5, 2, alignment=Qt.AlignCenter)
        self.validate_button.clicked.connect(self.validate_form)

        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        layout.addWidget(self.cancel_button, 5, 0, alignment=Qt.AlignCenter)
        self.cancel_button.clicked.connect(self.reject)

    def select_save_path(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        directory = QFileDialog.getExistingDirectory(self, "Select Save Path", "", options=options)
        if directory:
            self.save_path = directory
            self.save_path_text.setText(self.save_path)
            print("Save Path selected: ", self.save_path)

    def validate_form(self):
        if self.project_name.text() and self.author.text() and self.save_path:
            QMessageBox.information(self, "Confirmation", "All fields are filled in.")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")

    def get_data(self):
        return {
            "project_name": self.project_name.text(),
            "author": self.author.text(),
            "save_path": self.save_path,
        }


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


class TabFactoryWidget(QTabWidget):
    def __init__(self, lang_manager: LanguageApp, parent=None):
        super().__init__(parent)
        self.langManager = lang_manager
        self.setMovable(True)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)

    def close_tab(self, index):
        self.removeTab(index)

    def add_tab(self, tab: QWidget, title="Non Renseigné"):
        self.addTab(tab, title)
        self.setCurrentWidget(tab)
        tab.show()
        return tab

    def get_current_tab(self):
        return self.currentWidget()

    def get_tab(self, index):
        return self.widget(index)


# General View for Primary Side Panel
class GeneralSidePanel(QWidget):
    extObjChanged = Signal()

    def __init__(
            self,
            title_panel: str,
            tab_connect: TabFactoryWidget = None,
            lang_manager: LanguageApp = None,
            icon_manager: IconsApp = None,
            keys_manager: ShortcutApp = None,
            parent=None
    ):
        super().__init__(parent)
        print(parent)
        self.titlePanel = title_panel
        self.extObj = None
        self.langManager = lang_manager
        self.iconManager = icon_manager
        self.keysManager = keys_manager
        self.tabConnect = tab_connect

        self.glbLayout = QVBoxLayout(self)
        self.setLayout(self.glbLayout)

        self.initUI()
        self.initDisplayObj()
        self.btn_null = QPushButton("Open Project")
        self.btn_null.clicked.connect(parent.openProjectAction)
        self.glbLayout.addWidget(self.btn_null)
        self.set_extObjDisplay()

        self.extObjChanged.connect(self.set_extObjDisplay)

    def set_extObjDisplay(self):
        if self.extObj is None:
            self.treeView.hide()
            self.btn_null.show()
        else:
            self.btn_null.hide()
            self.treeView.show()
            self.loadDisplayObj()

    def setExtendsLs(self) -> list:
        ls_btn = [
            {
                "icon": qta.icon('fa5s.flag'),
                "tooltip": "flag",
                "action": None
            },
        ]
        return ls_btn

    def initUI(self):
        hwidget = QWidget(self)
        hbar = QHBoxLayout()
        # hbar.setContentsMargins(0, 0, 0, 0)
        hwidget.setLayout(hbar)
        self.glbLayout.addWidget(hwidget)

        titleUI = QLabel(self.titlePanel.upper())
        titleUI.setFont(QFont("Arial", 12, QFont.Bold))
        hbar.addWidget(titleUI)

        hbar.addStretch()

        for infos in self.setExtendsLs():
            btn = QPushButton(self)
            btn.setIcon(infos['icon'])
            btn.setToolTip(infos['tooltip'])
            if infos['action'] is not None:
                btn.clicked.connect(infos['action'])
            hbar.addWidget(btn)

        sep = QFrame(self)
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        self.glbLayout.addWidget(sep)

    def initDisplayObj(self):
        self.treeView = QTreeView()
        self.treeView.setHeaderHidden(True)
        self.treeView.setAnimated(True)
        self.glbLayout.addWidget(self.treeView)

    def loadDisplayObj(self):
        model = QFileSystemModel()
        model.setRootPath(self.extObj)
        self.treeView.setModel(model)
        self.treeView.setRootIndex(model.index(self.extObj))
        self.treeView.setSortingEnabled(True)
        self.treeView.sortByColumn(0, Qt.AscendingOrder)
        self.treeView.setColumnHidden(1, True)
        self.treeView.setColumnHidden(2, True)
        self.treeView.setColumnHidden(3, True)

    def openTabObj(self, index):
        logging.info("Open Tab for Obj in Tree")
        item = self.treeView.model().itemFromIndex(index)
        if item is not None:
            logging.info(f"Item: {item.text()}")


# Files Explorer Primary Side Panel
class FlsExpl(GeneralSidePanel):
    def __init__(
            self,
            title_panel: str,
            path: str = None,
            tab_connect: TabFactoryWidget = None,
            lang_manager: any = None,
            icon_manager: IconsApp = None,
            keys_manager: ShortcutApp = None,
            parent=None
    ):
        super().__init__(title_panel, tab_connect, lang_manager, icon_manager, keys_manager, parent)
        self.extObj = path

    def setExtendsLs(self) -> list:
        ls_btn = [
            {
                "icon": qta.icon("fa5s.file", "fa5s.plus",
                                 options=[{"scale_factor": 1}, {"scale_factor": 0.5, "color": "White"}]),
                "tooltip": "Add File",
                "action": self.addFile
            },
            {
                "icon": qta.icon("fa5s.folder", "fa5s.plus",
                                 options=[{"scale_factor": 1}, {"scale_factor": 0.5, "color": "White"}]),
                "tooltip": "Add Folder",
                "action": self.addFolder
            },
        ]
        return ls_btn

    def loadObjects(self):
        model = QFileSystemModel()
        model.setRootPath(self.opex)
        model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)
        self.treeView.setModel(model)
        self.treeView.setRootIndex(model.index(self.opex))
        self.treeView.setSortingEnabled(True)
        self.treeView.setColumnHidden(1, True)
        self.treeView.setColumnHidden(2, True)
        self.treeView.setColumnHidden(3, True)

        self.treeView.sortByColumn(0, Qt.AscendingOrder)
        self.treeView.setAnimated(True)
        self.treeView.setIndentation(20)
        self.treeView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.treeView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeView.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)

    def addFile(self):
        if self.extObj is None:
            self.extObj = os.getcwd()
        # Ouvrir une boîte de dialogue pour choisir l'emplacement et le nom du fichier
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Ajouter un fichier", self.extObj
        )
        if file_path:
            # Créer le fichier
            file = QFile(file_path)
            if file.open(QIODevice.WriteOnly):
                file.close()
                logging.info(f"File '{file_path}' created successfully.")
            else:
                logging.error(f"Failed to create file '{file_path}'.")

    def addFolder(self):
        if self.extObj is None:
            self.extObj = os.getcwd()
        # Ouvrir une boîte de dialogue pour choisir l'emplacement et le nom du dossier
        folder_path = QFileDialog.getExistingDirectory(
            self, "Ajouter un dossier", self.extObj
        )
        if folder_path:
            # Créer le dossier
            if QDir().mkdir(folder_path):
                logging.info(f"Folder '{folder_path}' created successfully.")
            else:
                logging.error(f"Failed to create folder '{folder_path}'.")


# Network Explorer Primary Side Panel
class NetExpl(GeneralSidePanel):
    def __init__(
            self,
            title_panel: str,
            lan_class: LanAudacity = None,
            tab_connect: TabFactoryWidget = None,
            lang_manager: any = None,
            icon_manager: IconsApp = None,
            keys_manager: ShortcutApp = None,
            parent=None
    ):
        super().__init__(title_panel, tab_connect, lang_manager, icon_manager, keys_manager, parent)
        self.extObj = lan_class

    def setExtendsLs(self) -> list:
        ls_btn = [
            {
                "icon": qta.icon("fa5s.network-wired", "fa5s.plus", options=[{"scale_factor": 1}, {"scale_factor": 0.5, "color": "Blue"}]),
                "tooltip": "Add Network",
                "action": self.addNetworkObj
            },
            {
                "icon": qta.icon("mdi6.server-plus"),
                "tooltip": "Add Device",
                "action": self.addDeviceObj
            },
        ]
        return ls_btn

    def loadDisplayObj(self):
        logging.info("Load network")
        model = QStandardItemModel()
        self.treeView.setModel(model)
        if self.extObj is not None and self.extObj.networks is not None:
            for network in self.extObj.networks:
                self.add_network_to_tree(network)
            if self.extObj.devices is not None:
                pass

    def addDeviceObj(self):
        logging.info("Add device")

    def addNetworkObj(self):
        logging.info("Add network")

    def add_network_to_tree(self, network):
        root = self.treeView.model().invisibleRootItem()
        item = QStandardItem(network.name)
        item.setIcon(qta.icon("mdi6.wan"))
        root.appendRow(item)

    def add_device_to_tree(self, selected_network, device):
        root = selected_network
        item = QStandardItem(device.name)
        item.setIcon(qta.icon("mdi6.cellphone"))
        root.appendRow(item)


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
        spacerI = QWidget(self)
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
                if menu["name"] == "edit_menu":
                    if action["name_low"] == "undo":
                        infobar.addAction(act_obj)
                    elif action["name_low"] == "redo":
                        infobar.addAction(act_obj)
                        infobar.addWidget(commandLine)
                        spacerO = QWidget()
                        spacerO.setSizePolicy(
                            QSizePolicy.Expanding, QSizePolicy.Expanding
                        )
                        infobar.addWidget(spacerO)
                if menu["name"] == "settings_menu":
                    if action["name_low"] == "notifications":
                        self.status_bar.addAction(act_obj)
                if menu["name"] == "view_menu":
                    if action["name_low"] == "extension":
                        toolsbar.addSeparator()
                    elif action["name_low"] == "user":
                        spacer = QWidget()
                        spacer.setSizePolicy(
                            QSizePolicy.Expanding, QSizePolicy.Expanding
                        )
                        toolsbar.addWidget(spacer)
                    toolsbar.addAction(act_obj)

        # Add Action to the infobar
        toggle_pSideBar = QAction(
            self.iconsManager.get_icon("toggleSideBar"),
            "Toggle Primary Side Bar",
            self,
        )
        toggle_pSideBar.setShortcut(
            self.shortcutManager.get_shortcut("toggleSidePanelView")
        )
        toggle_pSideBar.setStatusTip("Toggle Primary Side Bar")
        # toggle_pSideBar.triggered.connect(self.toggle_primary_side_bar)
        infobar.addAction(toggle_pSideBar)

        toggle_pPanel = QAction(
            self.iconsManager.get_icon("togglePanel"),
            "Toggle Primary Panel",
            self,
        )
        toggle_pPanel.setShortcut(
            self.shortcutManager.get_shortcut("toggleTerminalView")
        )
        toggle_pPanel.setStatusTip("Toggle Primary Panel")
        # toggle_pPanel.triggered.connect(self.toggle_primary_panel)
        infobar.addAction(toggle_pPanel)

    def initUI_central(self):
        # Central Widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Primary Side Bar (Left with QWidgets)
        self.primary_side_bar = QStackedWidget(self)
        self.primary_side_bar.setMinimumWidth(100)
        self.primary_side_bar.setMaximumWidth(400)
        # self.primary_side_bar.hide()

        # Primary Center Object (Center with Tab Widget)
        self.primary_center = QTabWidget(self)
        self.primary_center.setMinimumWidth(100)
        self.primary_center.setMinimumHeight(100)
        self.primary_center.setTabsClosable(True)
        self.primary_center.setMovable(True)

        # Primary Panel (Bottom with Tab Widget)
        self.primary_panel = QTabWidget(self)
        self.primary_panel.setMinimumHeight(100)
        self.primary_panel.setTabsClosable(True)
        self.primary_panel.setMovable(True)
        # self.primary_panel.hide()

        # Splitter between Primary Panel and Primary Center
        self.v_splitter = QSplitter(Qt.Vertical)
        self.v_splitter.addWidget(self.primary_center)
        self.v_splitter.addWidget(self.primary_panel)

        # Splitter between Primary Side Bar and V Splitter
        self.h_splitter = QSplitter(Qt.Horizontal)
        self.h_splitter.addWidget(self.primary_side_bar)
        self.h_splitter.addWidget(self.v_splitter)

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.h_splitter)
        self.central_widget.setLayout(layout)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Message",
            "Are you sure to quit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def toggle_primary_side_bar(self):
        if self.primary_side_bar.isVisible():
            self.primary_side_bar.hide()
        else:
            self.primary_side_bar.show()

    def toggle_primary_panel(self):
        if self.primary_panel.isVisible():
            self.primary_panel.hide()
        else:
            self.primary_panel.show()


if __name__ == "__main__":
    softw_manager = ConfigurationFile(current_dir() + "/conf/config_app.yaml")
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
