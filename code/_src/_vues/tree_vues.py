from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import ipaddress
from _src._mdl.mdl_managers import *
from _src._mdl.mdl_itm import *


class TreeviewDefault(QWidget):
    def __init__(self, network_manager: NetworkManager, obj_manager: SettingsModel, txt_manager: TextTranslateManager, parent=None):
        super().__init__(parent)
        self.networkManager = network_manager
        self.txtManager = txt_manager
        self.objManager = obj_manager
        dflt_layout = QGridLayout(self)

        # Création du label
        self.dflt_label = QLabel(self.txtManager.get_txt('Net Explorer').textTranslate.upper())
        # Ajout du label et du bouton au layout
        dflt_layout.addWidget(self.dflt_label, 0, 0)
        run_action = QPushButton(self.objManager.get_1_icon('run_icon').objIcon, '')
        run_action.setFixedSize(26, 26)
        dflt_layout.addWidget(run_action, 0, 1)
        add_action = QPushButton(self.objManager.get_1_icon('add_icon').objIcon, '')
        add_action.setFixedSize(26, 26)
        add_action.clicked.connect(self.add_parent_treeview)
        dflt_layout.addWidget(add_action, 0, 2)
        filter_action = QPushButton(self.objManager.get_1_icon('sort_icon').objIcon, '')
        filter_action.setFixedSize(26, 26)
        filter_action.clicked.connect(self.sorting_treeview)
        dflt_layout.addWidget(filter_action, 0, 3)

        # Création du modèle pour le treeview
        self.netTreeModel = QStandardItemModel()
        # Création du treeview
        self.netd_tree = QTreeView(self)
        self.netd_tree.setHeaderHidden(True)
        self.netd_tree.setAnimated(True)
        self.netd_tree.setModel(self.netTreeModel)
        dflt_layout.addWidget(self.netd_tree, 1, 0, 10, 4)

        # Définition du layout principal
        self.setLayout(dflt_layout)

    def sorting_treeview(self):
        if self.netTreeModel.rowCount() > 0:
            if self.netd_tree.isSortingEnabled():
                self.netd_tree.setSortingEnabled(False)
            else:
                self.netd_tree.setSortingEnabled(True)
                print('Enable sorting')

    def add_parent_treeview(self):
        cidr, ok = QInputDialog.getText(self, 'Address Settings', 'Address CIDR')
        if ok and cidr:
            # Ajouter un élément avec l'adresse CIDR à l'arbre
            self.add_treeview_entry(self.cidr_info(cidr))
            self.netd_tree.clicked.connect(self.parent().parent().openTabObjTree)

    def add_treeview_entry(self, cidr: dict):
        map_icon = self.objManager.get_1_icon('map_icon').objIcon
        obj_icon = self.objManager.get_1_icon('uc-question-mark_icon').objIcon

        for key, values in cidr.items():
            stdout_key = f"{key} ({len(values)})"
            ip, masque = self.cidr_to_ip_mask(key)
            new_network = Network(ip, masque)
            new_network.set_statusNetwork(map_icon, f'Map {key}')
            parent_item = QStandardItem(stdout_key)
            parent_item.setIcon(map_icon)
            parent_item.setFlags(parent_item.flags() & ~Qt.ItemIsEditable)
            self.netTreeModel.appendRow(parent_item)
            for value in values:
                new_device = Device(value, masque)
                child_item = QStandardItem(f"{value}")
                new_device.set_statusDevice(obj_icon, 'UC Unknown')
                child_item.setIcon(obj_icon)
                child_item.setFlags(child_item.flags() & ~Qt.ItemIsEditable)
                parent_item.appendRow(child_item)
                new_network.lsDevices.append(new_device)

            self.networkManager.add_network(new_network)

    @staticmethod
    def cidr_info(address_cidr):
        try:
            # Séparer l'adresse IP et le préfixe CIDR
            ip_network = ipaddress.ip_network(address_cidr, strict=False)

            # Liste contenant l'adresse IP
            ip_address = [str(ip_network.network_address + i) for i in range(1, len(list(ip_network.hosts())) + 1)]

            # Ajouter l'adresse réseau (CIDR) comme clé avec la liste des adresses IP comme valeur
            result = {str(ip_network): ip_address}

            return result

        except ValueError:
            return None

    @staticmethod
    def cidr_to_ip_mask(cidr):
        try:
            # Séparer l'adresse CIDR en adresse IP et préfixe
            ip, prefix = cidr.split('/')

            # Convertir le préfixe en masque de sous-réseau
            subnet_mask = ipaddress.IPv4Network(cidr).netmask

            # Renvoyer l'adresse IP et le masque sous forme de tuple de chaînes de caractères
            return ip, str(subnet_mask)
        except ValueError:
            # En cas d'erreur de format CIDR
            print("Format CIDR invalide.")
            return None, None