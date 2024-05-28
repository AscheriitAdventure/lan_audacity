import os
import sys
import logging
import logging.config
import json
import qtawesome as qta
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
    QLabel,
    QFrame,
    QTabWidget,
    QPushButton,
    QFileDialog,
    QTreeView,
    QFileSystemModel,
    QStatusBar,
    QLineEdit,
    QToolBar,
    QAction,
    QStackedWidget,
    QVBoxLayout,
    QSizePolicy,
    QAbstractItemView,
    QSizePolicy,
    QDialog,
    QMessageBox,
    QHBoxLayout,
    QSplitter
)
from PyQt5.QtCore import Qt, pyqtSignal as Signal, QDir, QFile, QIODevice
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont


from src.models.configuration_file import ConfigurationFile
from src.models.device import Device
from src.models.network import Network
from src.models.language_app import LanguageApp
from src.models.shortcut_app import ShortcutApp
from src.models.icons_app import IconsApp
from src.models.lan_audacity import LanAudacity

from src.views.forms_app import NNetwork, NProject

def current_dir():
    try:
        curr_path = os.getcwd()
        return curr_path
    except Exception as e:
        logging.error(
            f"Une erreur s'est produite lors de l'obtention du répertoire de travail actuel : {e}"
        )
        return "Analyse Erreur"


def get_spcValue(liste_add: list, arg_1: str, obj_src: str) -> dict:
    for obj_dict in liste_add:
        if obj_dict[arg_1] == obj_src:
            return obj_dict
    return {}


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


class NDevice(QDialog):
    def __init__(
            self,
            dialog_title: str,
            lan_audacity: LanAudacity,
            lang_manager: LanguageApp = None,
            icon_manager: IconsApp = None,
            parent=None
    ):
        super().__init__(parent)
        self.langManager = lang_manager
        self.iconManager = icon_manager
        self.setWindowTitle(dialog_title)

        # layout
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        # Title
        self.title = QLabel(dialog_title)
        self.title.setFont(QFont("Arial", 16, QFont.Bold))
        self.layout.addWidget(self.title, 0, 0, 1, 3)

        sep = QFrame(self)
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(sep, 1, 0, 1, 3)

        self.formUI()

    def formUI(self):
        obj_ls = [
            {
                "n_label": "Device Name:",
                "n_obj": "device_name",
                "n_text": "Device 1",
                "n_placeholder": "Device Name",
                "required": False
            },
            {
                "n_label": "Device IPv4:",
                "n_obj": "ipv4",
                "n_text": None,
                "n_placeholder": "127.0.0.1",
                "required": True
            },
            {
                "n_label": "Device Mask IPv4:",
                "n_obj": "mask_ipv4",
                "n_text": None,
                "n_placeholder": "255.0.0.0",
                "required": True
            },
            {
                "n_label": "Device IPv6:",
                "n_obj": "ipv6",
                "n_text": None,
                "n_placeholder": "::1",
                "required": False
            },
            {
                "n_label": "Device Mask IPv6:",
                "n_obj": "mask_ipv6",
                "n_text": None,
                "n_placeholder": "ffff:ffff:ffff:ffff::",
                "required": False
            },
            {
                "n_label": "Device Type:",
                "n_obj": "device_type",
                "n_text": None,
                "n_placeholder": "Router",
                "required": False
            },
            {
                "n_label": "Device Model:",
                "n_obj": "device_model",
                "n_text": None,
                "n_placeholder": "Cisco",
                "required": False
            },
            {
                "n_label": "Device Brand:",
                "n_obj": "device_brand",
                "n_text": None,
                "n_placeholder": "Linksys",
                "required": False
            },
            {
                "n_label": "Device MAC:",
                "n_obj": "device_mac",
                "n_text": None,
                "n_placeholder": "00:00:00:00:00:00",
                "required": False
            },
            {
                "n_label": "Device Gateway:",
                "n_obj": "device_gateway",
                "n_text": None,
                "n_placeholder": "127.0.0.1",
                "required": False
            },
            {
                "n_label": "Device DNS:",
                "n_obj": "device_dns",
                "n_text": None,
                "n_placeholder": "127.0.0.1",
                "required": False
            },
            {
                "n_label": "Device DHCP:",
                "n_obj": "device_dhcp",
                "n_text": None,
                "n_placeholder": "127.0.0.1",
                "required": False
            },
        ]

        self.fields = {}

        for i, obj in enumerate(obj_ls):
            label = QLabel(obj["n_label"])
            self.layout.addWidget(label, i + 2, 0)
            field = QLineEdit(self)
            field.setPlaceholderText(obj["n_placeholder"])
            if obj["n_text"]:
                field.setText(obj["n_text"])
            if obj["required"]:
                field.setStyleSheet("border: 1px solid red;")
            self.layout.addWidget(field, i + 2, 1)
            self.fields[obj["n_obj"]] = field

        # Validate button
        self.validate_button = QPushButton("Validate")
        self.layout.addWidget(self.validate_button, len(obj_ls) + 2, 2, alignment=Qt.AlignCenter)
        self.validate_button.clicked.connect(self.validate_form)

        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.layout.addWidget(self.cancel_button, len(obj_ls) + 2, 0, alignment=Qt.AlignCenter)
        self.cancel_button.clicked.connect(self.reject)

    def validate_form(self):
        if self.fields["ipv4"].text() and self.fields["mask_ipv4"].text():
            QMessageBox.information(self, "Confirmation", "All required fields are filled in.")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Please fill in all required fields (Device IPv4 and Device Mask IPv4).")

    def get_data(self):
        data = {key: field.text() for key, field in self.fields.items()}
        return data


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
        logging.info(f"parent:{parent}")
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
        logging.debug(f"{self.extObj}")
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
                "icon": self.iconManager.get_icon("defaultIcon"),
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
            lang_manager: LanguageApp = None,
            icon_manager: IconsApp = None,
            keys_manager: ShortcutApp = None,
            parent=None
    ):
        super().__init__(title_panel, tab_connect, lang_manager, icon_manager, keys_manager, parent)
        self.extObj = path

    def setExtendsLs(self) -> list:
        ls_btn = [
            {
                "icon": self.iconManager.get_icon("newFileAction"),
                "tooltip": "New File",
                "action": self.addFile
            },
            {
                "icon": self.iconManager.get_icon("newFolderAction"),
                "tooltip": "New Folder",
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
            lang_manager: LanguageApp = None,
            icon_manager: IconsApp = None,
            keys_manager: ShortcutApp = None,
            parent=None
    ):
        super().__init__(title_panel, tab_connect, lang_manager, icon_manager, keys_manager, parent)
        self.extObj = lan_class

    def setExtendsLs(self) -> list:
        ls_btn = [
            {
                "icon": self.iconManager.get_icon("newLanAction"),
                "tooltip": "New Network",
                "action": self.addNetworkObj
            },
            {
                "icon": self.iconManager.get_icon("newDeviceAction"),
                "tooltip": "New Device",
                "action": self.addDeviceObj
            },
        ]
        return ls_btn

    def loadDisplayObj(self) -> None:
        logging.info("Load network")
        model = QStandardItemModel()
        self.treeView.setModel(model)
        if self.extObj is not None and hasattr(self.extObj, 'networks'):
            for network in self.extObj.networks:
                logging.debug(network)
                self.add_network_to_tree(network)
            if hasattr(self.extObj, 'devices') and self.extObj.devices is not None:
                pass

    def addDeviceObj(self, network: Network = None):
        logging.info("Add device")
        new_device = NDevice("New Device", self.extObj, self.langManager, self.iconManager)
        if new_device.exec_() == QDialog.Accepted:
            device_data = new_device.get_data()
            device0 = Device(
                device_ipv4=device_data["ipv4"],
                mask_ipv4=device_data["mask_ipv4"],
                save_path=self.extObj.save_path,
                device_name=device_data["device_name"],
                device_ipv6=device_data.get("ipv6"),
                mask_ipv6=device_data.get("mask_ipv6"),
                device_type=device_data.get("device_type"),
                device_model=device_data.get("device_model"),
                device_brand=device_data.get("device_brand"),
                device_mac=device_data.get("device_mac"),
                device_gateway=device_data.get("device_gateway"),
                device_dns=device_data.get("device_dns"),
                device_dhcp=device_data.get("device_dhcp")
            )
            device0.create_device()
            if network:
                network.add_device(device0)
                network.save_network()
                self.add_device_to_tree(network, device0)

    def addNetworkObj(self):
        logging.info("Add network")
        new_network = NNetwork("New Network", self.extObj, self.langManager, self.iconManager)
        if new_network.exec_() == QDialog.Accepted:
            network_data = new_network.get_data()
            network = Network(
                network_ipv4=network_data["ipv4"],
                network_mask_ipv4=network_data["mask_ipv4"],
                save_path=network_data["path"],
                network_name=network_data.get("network_name"),
                network_ipv6=network_data.get("ipv6"),
                network_gateway=network_data.get("gateway"),
                network_dns=network_data.get("dns"),
                network_dhcp=network_data.get("dhcp")
            )
            network.create_network()
            self.extObj.add_network(network)
            self.extObj.save_project()

            self.add_network_to_tree(network)
        # Add Network to Tree

    def add_network_to_tree(self, network: Network):
        root = self.treeView.model().invisibleRootItem()
        logging.debug(network.name)
        if network.name is None:
            network.name = f"Network {len(root)}"
        item = QStandardItem(network.name)
        item.setIcon(self.iconManager.get_icon("networkDefaultIcon"))
        root.appendRow(item)

    def add_device_to_tree(self, selected_network, device):
        item = QStandardItem(device.name)
        item.setIcon(qta.icon("mdi6.cellphone"))
        selected_network.appendRow(item)


class MainApp(QMainWindow):
    def __init__(self, software_manager: ConfigurationFile, parent=None) -> None:
        super().__init__(parent)
        # Other Information
        self.prj_ls = []
        self.link_action = self.setLinkAction()
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

    def setLinkAction(self) -> list:
        return [
            {
                "name_acte": "new_project",
                "trigger": self.newProjectAction
            },
            {
                "name_acte": "open_project",
                "trigger": self.openProjectAction
            },
            {
                "name_acte": "save_project",
                "trigger": self.saveProjectAction
            },
            {
                "name_acte": "save_as_project",
                "trigger": self.saveAsProjectAction
            },
            {
                "name_acte": "close_project",
                "trigger": self.closeProjectAction
            },
            {
                "name_acte": "exit",
                "trigger": self.quitAction
            },
            {
                "name_acte": "file_explorer",
                "trigger": self.fileExplorerAction
            },
            {
                "name_acte": "net_explorer",
                "trigger": self.netExplorerAction
            },
            {
                "name_acte": "extension",
                "trigger": self.extensionAction
            },
            {
                "name_acte": "user",
                "trigger": self.userAction
            },
            {
                "name_acte": "preferences",
                "trigger": self.preferencesAction
            },
            # {
            #     "name_acte": "language",
            #     "trigger": self.openLanguage
            # },
            # {
            #     "name_acte": "shortcut_key",
            #     "trigger": self.openShortcutKey
            # },
            # {
            #     "name_acte": "notification",
            #     "trigger": self.openNotification
            # },
            # {
            #     "name_acte": "open_terminal",
            #     "trigger": self.openTerminal
            # },
        ]

    def centerWindow(self) -> None:
        # Obtenir la géométrie de l'écran
        screen_geometry = QApplication.desktop().screenGeometry()

        # Obtenir la géométrie de la fenêtre
        window_geometry = self.geometry()

        # Calculer la position pour centrer la fenêtre
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2

        # Déplacer la fenêtre
        self.move(x, y)

    def initUI_menu(self) -> None:
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
                dict_trig = get_spcValue(self.link_action, "name_acte", action["name_low"])
                if dict_trig != {}:
                    act_obj.triggered.connect(dict_trig['trigger'])
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
        toggle_pSideBar.triggered.connect(self.toggle_primary_side_bar)
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
        toggle_pPanel.triggered.connect(self.toggle_primary_panel)
        infobar.addAction(toggle_pPanel)

    def initUI_central(self) -> None:
        # Central Widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Primary Side Bar (Left with QWidgets)
        self.primary_side_bar = QStackedWidget(self)
        self.primary_side_bar.setMinimumWidth(100)
        self.primary_side_bar.setMaximumWidth(400)

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

        # stack widget
        self.file_explorer = FlsExpl(
            "Explorer",
            lang_manager=self.langManager,
            icon_manager=self.iconsManager,
            keys_manager=self.shortcutManager,
            parent=self
        )
        self.network_explorer = NetExpl(
            "Networks",
            lang_manager=self.langManager,
            icon_manager=self.iconsManager,
            keys_manager=self.shortcutManager,
            parent=self
        )
        self.extends_explorer = GeneralSidePanel(
            "Extensions",
            lang_manager=self.langManager,
            icon_manager=self.iconsManager,
            keys_manager=self.shortcutManager,
            parent=self
        )
        self.primary_side_bar.addWidget(self.file_explorer)
        self.primary_side_bar.addWidget(self.network_explorer)
        self.primary_side_bar.addWidget(self.extends_explorer)

    def closeEvent(self, event) -> None:
        reply = QMessageBox.question(
            self,
            "Message",
            "Are you sure to quit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            event.accept()
            logging.info("End of Application")
        else:
            event.ignore()

    def toggle_primary_side_bar(self) -> None:
        if self.primary_side_bar.isVisible():
            self.primary_side_bar.hide()
        else:
            self.primary_side_bar.show()

    def toggle_primary_panel(self) -> None:
        if self.primary_panel.isVisible():
            self.primary_panel.hide()
        else:
            self.primary_panel.show()

    # Actions
    def quitAction(self) -> None:
        self.close()

    def newProjectAction(self) -> None:
        newpa = NProject()
        if newpa.exec_() == QDialog.Accepted:
            data = newpa.get_data()
            nprjlan = LanAudacity(
                software_name=self.softwareManager.data['system']['name'],
                version_software=self.softwareManager.data['system']['version'],
                project_name=data["project_name"],
                save_path=data["save_path"],
                author=data["author"]
            )
            nprjlan.create_project()
            nprjlan.save_project()
            # Add the new project to the list
            self.prj_ls.append(nprjlan)
            # Add the new project to the file explorer
            self.file_explorer.extObj = f"{data["save_path"]}/{data["project_name"]}"
            self.file_explorer.set_extObjDisplay()
            self.primary_side_bar.setCurrentWidget(self.file_explorer)
            self.network_explorer.extObj = []
            self.network_explorer.set_extObjDisplay()
            # # Generate a new project

    def openProjectAction(self) -> None:
        directory_project = QFileDialog.getExistingDirectory(self, "Open Project", os.getcwd())
        if directory_project:
            project_file = os.path.join(directory_project, "lan_audacity.json")
            if os.path.exists(project_file):
                with open(project_file, "r") as file:
                    data = json.load(file)
                nprjlan = LanAudacity(
                    software_name=data["software"],
                    version_software=data["version"],
                    project_name=os.path.basename(directory_project),
                    save_path=directory_project,
                    author=data["author"]
                )
                if data["networks"] is not None:
                    logging.info(len(data["networks"]["obj_ls"]))
                    # add informations to nprjlan
                    for network in data["networks"]["obj_ls"]:
                        # open network file
                        network_file = os.path.join(network["path"])
                        if os.path.exists(network_file):
                            with open(network_file, "r") as file:
                                data_network = json.load(file)
                            net0X = Network(
                                    network_ipv4=data_network["ipv4"],
                                    network_mask_ipv4=data_network["mask_ipv4"],
                                    save_path=data_network["abs_path"],
                                    network_name=data_network["name"],
                                    network_ipv6=data_network["ipv6"],
                                    network_gateway=data_network["gateway"],
                                    network_dns=data_network["dns"],
                                    network_dhcp=data_network["dhcp"],
                                    uuid_str=data_network["uuid"]
                                )
                            net0X.date_unix = data_network["date_unix"]
                            nprjlan.add_network(net0X)

                nprjlan.open_project()
                nprjlan.save_project()
                self.prj_ls.append(nprjlan)

                self.file_explorer.extObj = directory_project
                self.file_explorer.set_extObjDisplay()
                self.primary_side_bar.setCurrentWidget(self.file_explorer)

                self.network_explorer.extObj = nprjlan
                self.network_explorer.set_extObjDisplay()
                # Charger l'arborescence dans le QTreeView
            else:
                QMessageBox.warning(self, "Error", "lan_audacity.json not found in the selected directory.")
        # Open a project

    def saveProjectAction(self) -> None:
        logging.debug("Save Action...")
        # Save the project

    def saveAsProjectAction(self) -> None:
        logging.debug("Save As Action...")
        # Save the project as

    def closeProjectAction(self) -> None:
        logging.debug("Close Project Action...")
        # Close the project

    def fileExplorerAction(self) -> None:
        if self.file_explorer.isVisible() is False:
            self.primary_side_bar.setCurrentWidget(self.file_explorer)
        # Open the file explorer

    def netExplorerAction(self) -> None:
        if self.network_explorer.isVisible() is False:
            self.primary_side_bar.setCurrentWidget(self.network_explorer)
        # Show the network explorer

    def extensionAction(self) -> None:
        if self.extends_explorer.isVisible() is False:
            self.primary_side_bar.setCurrentWidget(self.extends_explorer)
        # Open the extension library

    def preferencesAction(self) -> None:
        logging.debug("Preferences Action...")
        # Open the preferences window

    def userAction(self) -> None:
        logging.debug("User Action...")
        # Open the user window


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

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    app.setApplicationName(softw_manager.data["system"]["name"])
    app.setApplicationVersion(softw_manager.data["system"]["version"])
    app.setOrganizationName(softw_manager.data["system"]["organization"])

    main_window = MainApp(softw_manager)
    main_window.show()

    sys.exit(app.exec_())
