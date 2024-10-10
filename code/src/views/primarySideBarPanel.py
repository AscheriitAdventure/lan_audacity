import os
import logging

from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *

from src.classes.languageApp import LanguageApp
from src.classes.iconsApp import IconsApp
from src.classes.shortcutApp import ShortcutApp
from src.classes.lanAudacity import LanAudacity
from src.classes.cl_network import Network
from src.classes.cl_device import Device
from src.views.tabsApp import TabFactoryWidget
from src.views.formsApp import NNetwork, NDevice


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
        super().__init__(parent=parent)
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
        # logging.debug(f"{self.extObj}")
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

    def loadDisplayObj(self) -> None:
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
    
    def getSelectedItem(self, index):
        model = self.treeView.model()
        item = model.itemFromIndex(index)

        if item is not None:
            return item.text()


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
        model = QStandardItemModel(self)
        self.treeView.setModel(model)
        logging.debug(f"obj 1: ({self.extObj}), obj 2: {self.extObj.networks}")
        if self.extObj is not None and isinstance(self.extObj, LanAudacity):
            if self.extObj.networks:
                logging.debug(self.extObj.networks)
                for network in self.extObj.networks.get('obj_ls', []):
                    logging.debug(network.get('name'))
                    self.add_network_to_tree(network.get('name'))
                    if network.get('devices'):
                        for device in network.get('devices'):
                            self.add_device_to_tree(network.get('name'), device)
                    

    def addDeviceObj(self, network: Network = None):
        logging.info("Add device")
        new_device = NDevice(
            ext_obj=self.extObj,
            lang_manager=self.langManager,
            icon_manager=self.iconManager,
        )
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
                device_dns=device_data.get("device_dns")
            )
            device0.create_device()
            if network:
                network.add_device(device0)
                network.save_network()
                self.add_device_to_tree(network, device0)

    def addNetworkObj(self):
        logging.info("Add network")
        new_network = NNetwork(
            ext_obj=self.extObj,
            lang_manager=self.langManager,
            icon_manager=self.iconManager,
            parent=self
        )
        if new_network.exec_() == QDialog.Accepted:
            network_data = new_network.get_data()
            logging.debug(network_data)
            network = Network(
                network_ipv4=network_data["ipv4"],
                network_mask_ipv4=network_data["mask_ipv4"],
                save_path=network_data["path"],
                network_name=network_data.get("network_name"),
                network_ipv6=network_data.get("ipv6"),
                network_gateway=network_data.get("gateway"),
                network_dns=network_data.get("dns")
            )
            network.create_network()
            self.extObj.add_network(network)
            self.extObj.updateLanAudacity()

            self.add_network_to_tree(network.name)
        # Add Network to Tree

    def add_network_to_tree(self, network: str):
        item = QStandardItem(network)
        item.setIcon(self.iconManager.get_icon("networkDefaultIcon"))
        self.treeView.model().invisibleRootItem().appendRow(item)

    def add_device_to_tree(self, selected_network, device):
        item = QStandardItem(device.name)
        item.setIcon(self.iconManager.get_icon("networkDefaultIcon"))
        selected_network.appendRow(item)
    
    def getSelectedItem(self, index):
        model = self.treeView.model()
        item = model.itemFromIndex(index)

        if item is not None:
            network_name = item.text()
            network = self.extObj.getObjNetwork(network_name)
            return network

        return None