import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal as Signal, QDir, QFile, QIODevice
from PyQt5.QtGui import *
import qtawesome as qta
import logging

from lan_audacity import LanAudacity
#from pyqt_views import MainWindow


class TabFactoryWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
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
            lang_manager: any = None,
            parent=None
    ):
        super().__init__(parent)
        print(parent)
        self.titlePanel = title_panel
        self.extObj = None
        self.langManager = lang_manager
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
            parent=None
    ):
        super().__init__(title_panel, tab_connect, lang_manager, parent)
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
            parent=None
    ):
        super().__init__(title_panel, tab_connect, lang_manager, parent)
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

# Extends Explorer Primary Side Panel
