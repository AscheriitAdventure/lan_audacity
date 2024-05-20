from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *
from src.views.tabs_view import TabWidgetFactory
from src.models.lang_app import LanguageApp
from src.views.general_tabs_view import NetworkMapTab, DeviceTab
from src.models.network_map import NetworkMap, NetworkMapManager
from src.models.device import Device
import qtawesome as qta
import logging
import ipaddress


class GeneralExplorerWidget(QWidget):
    def __init__(
        self,
        name_explorer: str,
        qtabconnect: TabWidgetFactory,
        lang_manager: LanguageApp,
        parent=None,
    ):
        super().__init__(parent)
        self.qtabconnect = qtabconnect
        self.langManager = lang_manager
        self.layout = QVBoxLayout(self)
        self.nameExplorer = name_explorer
        self.setLayout(self.layout)

        self.createUI()
    
    def set_listbtn(self) -> list:
        ls_btn = [
            {
                "icon": qta.icon('fa5s.flag'),
                "tooltip": "flag",
                "action": None
            },
        ]
        return ls_btn

    def createUI(self):
        hbar = QHBoxLayout()
        hbar.setContentsMargins(0, 0, 0, 0)
        self.layout.addLayout(hbar)

        titleUI = QLabel(self.nameExplorer.upper())
        titleUI.setFont(QFont("Arial", 12, QFont.Bold))
        titleUI.setAlignment(Qt.AlignLeft)
        hbar.addWidget(titleUI)

        hbar.addStretch()

        for infos in self.set_listbtn():
            btn = QPushButton(self)
            btn.setIcon(infos['icon'])
            btn.setToolTip(infos['tooltip'])
            btn.clicked.connect(infos['action'])
            hbar.addWidget(btn)
        
        self.treeView = QTreeView()
        self.treeView.setHeaderHidden(True)
        self.treeView.setAnimated(True)
        self.layout.addWidget(self.treeView)
        self.loadObjects()
    
    def loadObjects(self):
        model = QStandardItemModel()
        self.treeView.setModel(model)


class FilesExplorerWidget(QWidget):
    def __init__(
        self,
        name_explorer: str,
        path: str,
        qtabconnect: TabWidgetFactory,
        lang_manager: LanguageApp,
        parent=None,
    ):
        super().__init__(parent)
        self.qtabconnect = qtabconnect
        self.langManager = lang_manager
        self.absolutePath = path
        self.layout = QVBoxLayout(self)
        self.nameExplorer = name_explorer
        self.setLayout(self.layout)

        self.createUI()

    def createUI(self):
        hbar = QHBoxLayout()
        hbar.setContentsMargins(0, 0, 0, 0)
        self.layout.addLayout(hbar)

        titleUI = QLabel(self.nameExplorer.upper())
        titleUI.setFont(QFont("Arial", 12, QFont.Bold))
        titleUI.setAlignment(Qt.AlignLeft)
        hbar.addWidget(titleUI)

        hbar.addStretch()

        add_file = QPushButton(
            qta.icon(
                "fa5s.file",
                "fa5s.plus",
                options=[{"scale_factor": 1}, {"scale_factor": 0.5, "color": "White"}],
            ),
            "",
        )
        add_file.clicked.connect(self.addFile)
        hbar.addWidget(add_file)
        add_folder = QPushButton(
            qta.icon(
                "fa5s.folder",
                "fa5s.plus",
                options=[{"scale_factor": 1}, {"scale_factor": 0.5, "color": "White"}],
            ),
            "",
        )
        add_folder.clicked.connect(self.addFolder)
        hbar.addWidget(add_folder)

        self.treeView = QTreeView()
        self.treeView.setHeaderHidden(True)
        self.treeView.setAnimated(True)
        self.layout.addWidget(self.treeView)
        self.loadFiles()

    def loadFiles(self):
        model = QFileSystemModel()
        model.setRootPath(self.absolutePath)
        model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)
        self.treeView.setModel(model)
        self.treeView.setRootIndex(model.index(self.absolutePath))
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
        self.treeView.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)

    def addFile(self):
        # Ouvrir une boîte de dialogue pour choisir l'emplacement et le nom du fichier
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Ajouter un fichier", self.absolutePath
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
        # Ouvrir une boîte de dialogue pour choisir l'emplacement et le nom du dossier
        folder_path = QFileDialog.getExistingDirectory(
            self, "Ajouter un dossier", self.absolutePath
        )
        if folder_path:
            # Créer le dossier
            if QDir().mkdir(folder_path):
                logging.info(f"Folder '{folder_path}' created successfully.")
            else:
                logging.error(f"Failed to create folder '{folder_path}'.")

    def openTabObjTree(self, index):
        logging.info("Open tab object tree")
        item = self.treeView.model().itemFromIndex(index)
        if item is not None:
            logging.info(f"Item: {item.text()}")


class NetExplorerWidget(QWidget):
    def __init__(
        self,
        name_explorer: str,
        qtabconnect: TabWidgetFactory,
        lang_manager: LanguageApp,
        parent=None,
    ):
        super().__init__(parent)
        self.qtabconnect = qtabconnect
        self.siteManager = NetworkMapManager()
        self.langManager = lang_manager
        self.layout = QVBoxLayout(self)
        self.nameExplorer = name_explorer
        self.setLayout(self.layout)

        self.createUI()

    def createUI(self):
        hbar = QHBoxLayout()
        hbar.setContentsMargins(0, 0, 0, 0)
        self.layout.addLayout(hbar)

        titleUI = QLabel(self.nameExplorer.upper())
        titleUI.setFont(QFont("Arial", 12, QFont.Bold))
        titleUI.setAlignment(Qt.AlignLeft)
        hbar.addWidget(titleUI)

        hbar.addStretch()

        ico_nnet = qta.icon(
                "fa5s.network-wired",
                "fa5s.plus",
                options=[{"scale_factor": 1}, {"scale_factor": 0.5, "color": "Green"}],
            )
        new_network = QPushButton(self)
        new_network.setIcon(ico_nnet)
        new_network.clicked.connect(self.addNetwork)
        hbar.addWidget(new_network)

        new_device = QPushButton(self)
        new_device.setIcon(qta.icon("mdi6.server-plus"))
        new_device.clicked.connect(self.addDevice)
        hbar.addWidget(new_device)

        self.treeView = QTreeView()
        self.treeView.setHeaderHidden(True)
        self.treeView.setAnimated(True)
        self.layout.addWidget(self.treeView)
        self.loadNetwork()

    def loadNetwork(self):
        logging.info("Load network")
        model = QStandardItemModel()
        self.treeView.setModel(model)

    def addNetwork(self):
        logging.info("Add network")
        cidr, ok = QInputDialog.getText(self, "Address Settings", "Address CIDR")
        if ok and cidr:
            self.populateTree(self.cidr_info(cidr))
            self.treeView.clicked.connect(self.openTabObjTree)

    def populateTree(self, network: dict):
        map_icon = qta.icon(
            "fa5s.map",
            "fa5s.map-signs",
            options=[
                {"scale_factor": 1, "color": "grey"},
                {"scale_factor": 0.85, "color": "green"},
            ],
        )
        uc_icon = qta.icon(
            "fa5s.desktop",
            "fa5s.question",
            options=[
                {"scale_factor": 1, "color": "grey"},
                {"scale_factor": 0.85, "color": "blue"},
            ],
        )

        for key, values in network.items():
            stdout_key = f"{key} ({len(values)})"
            ip, mask = self.cidr_to_ip_mask(key)
            new_network = NetworkMap(ip, mask)
            new_network.setIconLan(map_icon)
            self.siteManager.add_network(new_network)
            parent_item = QStandardItem(stdout_key)
            parent_item.setIcon(map_icon)
            parent_item.setFlags(parent_item.flags() & ~Qt.ItemIsEditable)
            self.treeView.model().appendRow(parent_item)
            for value in values:
                new_device = Device(value, mask)
                new_device.setIconLan(uc_icon)
                new_network.add_device(new_device)
                child_item = QStandardItem(value)
                child_item.setIcon(uc_icon)
                child_item.setFlags(child_item.flags() & ~Qt.ItemIsEditable)
                parent_item.appendRow(child_item)

    def addDevice(self):
        logging.info("Add device")
        # select a NetworkMap if exist and add a device
        #   else generate a NetworkMap item and add the device

    def openTabObjTree(self, index):
        logging.info("Open tab object tree")
        item = self.treeView.model().itemFromIndex(index)
        if item is not None:
            if item.parent() is None:
                for network in self.siteManager.networksList:
                    txt_id = f"{network.ipv4_mask_to_cidr(network.ipv4, network.mask)} ({network.get_lenght_devices()})"
                    logging.debug(item.text() + " Networkmap open " + txt_id)
                    if item.text() == txt_id:
                        self.qtabconnect.add_tab(
                            NetworkMapTab(self.langManager, network), item.text()
                        )
            else:
                logging.debug("Device open")
                for network in self.siteManager.networksList:
                    for device in network.devicesList:
                        if item.text() == device.ipv4:
                            self.qtabconnect.add_tab(
                                DeviceTab(self.langManager, device), item.text()
                            )

    @staticmethod
    def cidr_info(address_cidr):
        try:
            # Séparer l'adresse IP et le préfixe CIDR
            ip_network = ipaddress.ip_network(address_cidr, strict=False)
            # Liste contenant l'adresse IP
            ip_address = [
                str(ip_network.network_address + i)
                for i in range(1, len(list(ip_network.hosts())) + 1)
            ]
            # Ajouter l'adresse réseau (CIDR) comme clé avec la liste des adresses IP comme valeur
            result = {str(ip_network): ip_address}
            return result
        except ValueError:
            logging.warning("Format CIDR invalide.")
            return None

    @staticmethod
    def cidr_to_ip_mask(cidr):
        try:
            # Séparer l'adresse CIDR en adresse IP et préfixe
            ip, prefix = cidr.split("/")
            # Convertir le préfixe en masque de sous-réseau
            subnet_mask = ipaddress.IPv4Network(cidr).netmask
            # Renvoyer l'adresse IP et le masque sous forme de tuple de chaînes de caractères
            return ip, str(subnet_mask)
        except ValueError:
            # En cas d'erreur de format CIDR
            logging.warning("Format CIDR invalide.")
            return None, None


class DLCExplorerWidget(QWidget):
    def __init__(
        self,
        name_explorer: str,
        qtabconnect: TabWidgetFactory,
        lang_manager: LanguageApp,
        parent=None,
    ):
        super().__init__(parent)
        self.langManager = lang_manager
        self.qtconnect = qtabconnect
        self.layout = QVBoxLayout(self)
        self.nameExplorer = name_explorer
        self.setLayout(self.layout)

        self.createUI()

    def createUI(self):
        hbar = QHBoxLayout()
        hbar.setContentsMargins(0, 0, 0, 0)
        self.layout.addLayout(hbar)

        titleUI = QLabel(self.nameExplorer.upper())
        titleUI.setFont(QFont("Arial", 12, QFont.Bold))
        titleUI.setAlignment(Qt.AlignLeft)
        hbar.addWidget(titleUI)

        hbar.addStretch()

        add_action = QPushButton(qta.icon("fa5s.plus"), "")
        hbar.addWidget(add_action)

        self.list_view = QListWidget(self)
        self.list_view.setAcceptDrops(True)
        self.list_view.setDragEnabled(True)
        self.layout.addWidget(self.list_view)
        self.loadDLC()

    def loadDLC(self):
        list_item = [
            {
                "icon": qta.icon("mdi6.language-c", color="RoyalBlue"),
                "name": "C",
            },
            {
                "icon": qta.icon("mdi6.language-cpp", color="RoyalBlue"),
                "name": "C++",
            },
            {
                "icon": qta.icon("mdi6.language-csharp", color="RoyalBlue"),
                "name": "C#",
            },
            {
                "icon": qta.icon("fa5b.docker", color="Cyan"),
                "name": "Docker",
            },
            {
                "icon": qta.icon("fa5b.java", color="Grey"),
                "name": "Java",
            },
            {
                "icon": qta.icon("fa5b.python", color="Grey"),
                "name": "Python",
            },
            {
                "icon": qta.icon("fa5b.html5", color="Orange"),
                "name": "HTML5",
            },
            {
                "icon": qta.icon("fa5b.css3-alt", color="Blue"),
                "name": "CSS3",
            },
            {
                "icon": qta.icon("fa5b.js", color="Yellow"),
                "name": "Javascript",
            },
            {
                "icon": qta.icon("mdi6.language-php", color="DarkOrchid"),
                "name": "PHP",
            },
        ]

        for item in list_item:
            itemUI = QListWidgetItem(item["icon"], item["name"])
            self.list_view.addItem(itemUI)


class SearchExplorerWidget(QWidget):
    def __init__(
        self,
        name_explorer: str,
        qtabconnect: TabWidgetFactory,
        lang_manager: LanguageApp,
        parent=None,
    ):
        super().__init__(parent)
        self.langManager = lang_manager
        self.qtconnect = qtabconnect
        self.layout = QVBoxLayout(self)
        self.nameExplorer = name_explorer
        self.setLayout(self.layout)

        self.createUI()

    def createUI(self):
        hbar = QHBoxLayout()
        hbar.setContentsMargins(0, 0, 0, 0)
        self.layout.addLayout(hbar)

        titleUI = QLabel(self.nameExplorer.upper())
        titleUI.setFont(QFont("Arial", 12, QFont.Bold))
        titleUI.setAlignment(Qt.AlignLeft)
        hbar.addWidget(titleUI)

        hbar.addStretch()

        add_action = QPushButton(qta.icon("fa5s.plus"), "")
        hbar.addWidget(add_action)

        self.treeView = QTreeView()
        self.treeView.setHeaderHidden(True)
        self.treeView.setAnimated(True)
        self.layout.addWidget(self.treeView)
