from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.models.worker import Worker
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
        self.opex: any = None
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
            if infos['action'] is not None:
                btn.clicked.connect(infos['action'])
            hbar.addWidget(btn)
        
        self.btn_thread = QPushButton(self)
        hbar.addWidget(self.btn_thread)
        self.spin_anm = qta.Spin(self.btn_thread, autostart=False)
        ico_th = qta.icon('fa5s.circle-notch', color='RoyalBlue', animation=self.spin_anm)
        self.btn_thread.setIcon(ico_th)
        self.btn_thread.hide()
        
        self.treeView = QTreeView()
        self.treeView.setHeaderHidden(True)
        self.treeView.setAnimated(True)
        self.layout.addWidget(self.treeView)
        self.loadObjects()
    
    def runThreadFunc(self, method) -> None:
        # Démarrer l'animation de l'icône spinner
        self.start_spinner()
        # Utiliser QTimer pour démarrer le thread après un délai
        QTimer.singleShot(50, lambda: self.start_thread(method))
    
    def start_thread(self, method):
        self.thread = Worker(method)
        self.thread.finished.connect(self.stop_spinner)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def start_spinner(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate_spinner)
        self.angle = 0
        self.timer.start(50)  # Déclencher toutes les 50 ms

    def stop_spinner(self):
        self.timer.stop()
        self.rotate_spinner(rotate=False)

    def rotate_spinner(self, rotate=True):
        if rotate:
            self.spin_anm.start()
        else:
            self.spin_anm.stop()
    
    def loadObjects(self):
        model = QStandardItemModel()
        self.treeView.setModel(model)
    
    def openTabObjTree(self, index):
        logging.info("Open tab object tree")
        item = self.treeView.model().itemFromIndex(index)
        if item is not None:
            logging.info(f"Item: {item.text()}")


class FilesExplorerWidget(GeneralExplorerWidget):
    def __init__(
        self,
        name_explorer: str,
        path: str,
        qtabconnect: TabWidgetFactory,
        lang_manager: LanguageApp,
        parent=None,
    ):
        super().__init__(name_explorer, qtabconnect, lang_manager, parent)
        self.opex = path
    
    def set_listbtn(self) -> list:
        ls_btn = [
            {
                "icon": qta.icon("fa5s.file", "fa5s.plus", options=[{"scale_factor": 1}, {"scale_factor": 0.5, "color": "White"}]),
                "tooltip": "Add File",
                "action": self.runThreadFunc(self.addFile)
            },
            {
                "icon": qta.icon("fa5s.folder", "fa5s.plus", options=[{"scale_factor": 1}, {"scale_factor": 0.5, "color": "White"}]),
                "tooltip": "Add Folder",
                "action": self.runThreadFunc(self.addFolder)
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


class NetExplorerWidget(GeneralExplorerWidget):
    def __init__(
        self,
        name_explorer: str,
        qtabconnect: TabWidgetFactory,
        lang_manager: LanguageApp,
        parent=None,
    ):
        super().__init__(name_explorer, qtabconnect, lang_manager, parent)
        self.siteManager = NetworkMapManager()
    
    def set_listbtn(self) -> list:
        ls_btn = [
            {
                "icon": qta.icon("fa5s.network-wired", "fa5s.plus", options=[{"scale_factor": 1}, {"scale_factor": 0.5, "color": "Green"}]),
                "tooltip": "Add Network",
                "action": self.runThreadFunc(self.addNetwork)
            },
            {
                "icon": qta.icon("mdi6.server-plus"),
                "tooltip": "Add Device",
                "action": self.runThreadFunc(self.addDevice)
            },
        ]
        return ls_btn

    def loadObjects(self):
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


class DLCExplorerWidget(GeneralExplorerWidget):
    def __init__(
        self,
        name_explorer: str,
        qtabconnect: TabWidgetFactory,
        lang_manager: LanguageApp,
        parent=None,
    ):
        super().__init__(name_explorer, qtabconnect, lang_manager, parent)
    
    def set_listbtn(self) -> list:
        ls_btn = [
            {
                "icon": qta.icon("fa5s.plus", color="GreenForest"),
                "tooltip": "Add DLC",
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
            if infos['action'] is not None:
                btn.clicked.connect(infos['action'])
            hbar.addWidget(btn)

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


class SearchExplorerWidget(GeneralExplorerWidget):
    def __init__(
        self,
        name_explorer: str,
        qtabconnect: TabWidgetFactory,
        lang_manager: LanguageApp,
        parent=None,
    ):
        super().__init__(name_explorer, qtabconnect, lang_manager, parent)
