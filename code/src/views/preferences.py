import qtawesome
from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *
import logging
import os
import json

from src.classes.languageApp import LanguageApp
from src.classes.cl_network import Network
from src.views.templatesViews import Card, LineUpdate, RoundedBtn, CardStackGeneral, TitleWithAction
from src.classes.configurationFile import ConfigurationFile
from src.classes.iconsApp import IconsApp


class PreferencesGeneral(CardStackGeneral):
    def __init__(
            self,
            obj_title: str,
            obj_lang: LanguageApp,
            obj_view: ConfigurationFile,
            parent=None
    ):
        super().__init__(
            obj_title=obj_title,
            obj_lang=obj_lang,
            obj_view=obj_view,
            parent=parent
        )
        logging.info(self.objManager)

    def setCardList(self):
        self.card_list = [
            {
                "icon_card": None,
                "title_card": QLabel("Name Software"),
                "img_card": None,
                "corps_card": QLineEdit(self.objManager.data['system']['name']),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Description Software"),
                "img_card": None,
                "corps_card": QTextEdit(self.objManager.data['system']['description']),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Version Software"),
                "img_card": None,
                "corps_card": QLineEdit(self.objManager.data['system']['version']),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Authors Software"),
                "img_card": None,
                "corps_card": QLineEdit(self.objManager.data['system']['authors']),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Organisation"),
                "img_card": None,
                "corps_card": QLineEdit(self.objManager.data['system']['organization']),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Type Software"),
                "img_card": None,
                "corps_card": QLineEdit(self.objManager.data['system']['type']),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Version Date"),
                "img_card": None,
                "corps_card": QLineEdit(str(self.objManager.data['system']['version_date'])),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Python Language Version"),
                "img_card": None,
                "corps_card": QLineEdit(str(self.objManager.data['system']['version_python'])),
            },
            {
                "icon_card": None,
                "title_card": QLabel("PyQT Version"),
                "img_card": None,
                "corps_card": QLineEdit(str(self.objManager.data['system']['version_pyqt'])),
            },
            {
                "icon_card": None,
                "title_card": QLabel("NMAP Version"),
                "img_card": None,
                "corps_card": QLineEdit(str(self.objManager.data['system']['version_nmap'])),
            },
        ]


class NetworkGeneral(CardStackGeneral):
    def __init__(
            self, 
            obj_title: str, 
            obj_lang: LanguageApp, 
            obj_view: Network, 
            parent=None):
        super().__init__(obj_title, obj_lang, obj_view, parent)
        logging.info(self.objManager)
    
    def setCardList(self):
        self.card_list = [
            {
                "icon_card": None,
                "title_card": QLabel("IPv4 Address"),
                "img_card": None,
                "corps_card": LineUpdate(
                    input_obj=QLineEdit(self.objManager.ipv4),
                    action_obj=RoundedBtn(icon=qtawesome.icon('mdi6.pencil'), text=None, parent=self)),
            },
            {
                "icon_card": None,
                "title_card": QLabel("IPv4 Mask"),
                "img_card": None,
                "corps_card": LineUpdate(
                    input_obj=QLineEdit(self.objManager.maskIpv4),
                    action_obj=RoundedBtn(icon=qtawesome.icon('mdi6.pencil'), text=None, parent=self)),
            },
            {
                "icon_card": None,
                "title_card": QLabel("IPv6 Address"),
                "img_card": None,
                "corps_card": LineUpdate(
                    input_obj=QLineEdit(self.objManager.ipv6),
                    action_obj=RoundedBtn(icon=qtawesome.icon('mdi6.pencil'), text=None, parent=self)),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Gateway"),
                "img_card": None,
                "corps_card": LineUpdate(
                    input_obj=QLineEdit(self.objManager.gateway),
                    action_obj=RoundedBtn(icon=qtawesome.icon('mdi6.pencil'), text=None, parent=self)),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Nom de Domaine"),
                "img_card": None,
                "corps_card": LineUpdate(
                    input_obj=QLineEdit(self.objManager.dns),
                    action_obj=RoundedBtn(icon=qtawesome.icon('mdi6.pencil'), text=None, parent=self)),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Creation Date"),
                "img_card": None,
                "corps_card": QLineEdit(
                    self.objManager.clockManager.conv_unix_to_datetime(
                        self.objManager.clockManager.clockCreated)),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Update Date"),
                "img_card": None,
                "corps_card": QLineEdit(
                    self.objManager.clockManager.conv_unix_to_datetime(
                        self.objManager.clockManager.get_clock_last())),
            }
        ]


class LANDashboard(QWidget):
    def __init__(self,
                 obj_title: str,
                 obj_lang: LanguageApp,
                 obj_view: Network,
                 parent=None):
        super().__init__(parent)
        self.stackTitle = obj_title
        self.langManager = obj_lang
        self.objManager = obj_view

        # init User Interface
        self.initUI()
        # show the cards
        self.clearCardLayout()
        self.setCardsView()

    def initUI(self):
        # Set the general layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # Set the top widget
        title_widget = QWidget(self)
        self.layout.addWidget(title_widget, alignment=Qt.AlignTop)

        ttl_wdg_cnt = QHBoxLayout(title_widget)
        # Set the title
        title = QLabel(self.stackTitle)
        title.setFont(QFont("Arial", 12, QFont.Bold))
        ttl_wdg_cnt.addWidget(title, alignment=Qt.AlignCenter)
        ttl_wdg_cnt.addStretch()

        # set the separator
        sep = QFrame(self)
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(sep)

        # Set up the scroll area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        self.layout.addWidget(scroll_area)

        # Create a widget to contain the cards
        self.card_container = QWidget(self)
        scroll_area.setWidget(self.card_container)

        self.card_layout = QGridLayout(self.card_container)
        self.card_layout.setContentsMargins(0, 0, 0, 0)

    def clearCardLayout(self):
        while self.card_layout.count():
            child = self.card_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_card_layout(child.layout())

    def setCardsView(self):
        # WAN, card(Rang 0, Colonne 0)
        wan_body_card = QWidget(self)
        wan_body_card_layout = QVBoxLayout(wan_body_card)

        dns_edit = QLineEdit(self.objManager.dns)
        dns_edit.setReadOnly(True)
        wan_body_card_layout.addWidget(LineUpdate(QLabel('Nom de Domaine :'), dns_edit))

        gate_edit = QLineEdit(self.objManager.gateway)
        gate_edit.setReadOnly(True)
        wan_body_card_layout.addWidget(LineUpdate(QLabel('Gateway :'), gate_edit))

        ico_wan = qtawesome.icon('mdi6.web', options=[{'color': 'silver'}])
        wan_card = Card(
            icon_card=ico_wan,
            title_card=QLabel('WAN'),
            corps_card=wan_body_card)
        self.card_layout.addWidget(wan_card, 0, 0)

        lan_headband: list = ["IPv4", "Name", "Mac Address", "Status"]
        lan_body_card = QTableWidget(self)
        lan_body_card.setColumnCount(lan_headband.__len__())
        lan_body_card.setHorizontalHeaderLabels(lan_headband)

        if self.objManager.devicesList is not []:
            for device in self.objManager.devicesList:
                lan_body_card.insertRow(lan_body_card.rowCount())
                var_path = os.path.join(
                    os.path.dirname(os.path.dirname(self.objManager.absPath)),
                    "desktop", f"{device}.json")
                if os.path.exists(var_path):
                    with open(var_path, 'r') as f:
                        device_data = json.load(f)
                        ipv4 = device_data.get('ipv4', 'value unknown') or 'value unknown'
                        name = device_data.get('name', 'value unknown') or 'value unknown'
                        mac = device_data.get('mac', 'value unknown') or 'value unknown'
                        lan_body_card.setItem(lan_body_card.rowCount() - 1, 0, QTableWidgetItem(ipv4))
                        lan_body_card.setItem(lan_body_card.rowCount() - 1, 1, QTableWidgetItem(name))
                        lan_body_card.setItem(lan_body_card.rowCount() - 1, 2, QTableWidgetItem(mac))
                        lan_body_card.setItem(lan_body_card.rowCount() - 1, 3, QTableWidgetItem('Not Setted'))
        ico_lan = qtawesome.icon('mdi6.lan-connect', options=[{'color': 'silver'}])

        self.scan_btn = RoundedBtn(icon=qtawesome.icon('mdi6.refresh'), text=None, parent=self)
        self.scan_btn.clicked.connect(self.toggle_scan)

        self.trash_btn = RoundedBtn(icon=qtawesome.icon('mdi6.delete'), text=None, parent=self)
        self.trash_btn.clicked.connect(self.clean_lan)

        ttl_btn = [self.scan_btn, self.trash_btn]
        q_obj_lan_ttl = TitleWithAction(title=f'LAN {self.objManager.dns}', action=ttl_btn) 

        lan_card = Card(icon_card=ico_lan, title_card=q_obj_lan_ttl, corps_card=lan_body_card)
        self.card_layout.addWidget(lan_card, 0, 1, 1, 3)

        # Liste du matériel réseau, card(Rang 1, Colonne 0)
        lsdevice_body_card = QTableWidget(self)
        lsdevice_body_card.setColumnCount(3)
        lsdevice_body_card.setHorizontalHeaderLabels(["Name/IPv4", "Emit", "Send"])

        ico_lan_devices = qtawesome.icon('mdi6.clipboard-text-multiple')
        list_lan_device_card = Card(ico_lan_devices, QLabel('List of network equipment'), None, lsdevice_body_card)
        self.card_layout.addWidget(list_lan_device_card, 1, 0, 1, 2)

        # Anomalies en cours, card(Rang 1, Colonne 1)
        lspb_body_card = QTableWidget(self)
        lspb_body_card.setColumnCount(3)
        lspb_body_card.setHorizontalHeaderLabels(["Time", "Hostname/IPv4", "Message"])

        ico_lan_pb = qtawesome.icon('mdi6.clipboard-alert')
        curr_pbs_card = Card(ico_lan_pb, QLabel('Current Problems'), None, lspb_body_card)
        self.card_layout.addWidget(curr_pbs_card, 1, 2, 1, 2)

    def setLanTable(self):
        pass

    def setInfraDeviceTable(self):
        pass

    def setNewsProblemTable(self):
        pass
    
    def clean_lan(self):
        list_object = self.objManager.devicesList
        try:
            # Vérifier si la liste des appareils est vide
            if not list_object:
                pass  # Pas d'appareils à traiter
            else:
                ip_list = []
                # Pour chaque appareil dans la liste
                for device in list_object:
                    # Chemin vers le fichier JSON de l'appareil
                    var_path = os.path.join(os.path.dirname(os.path.dirname(self.objManager.absPath)), "desktop", f"{device}.json")
                
                    # Vérifier si le fichier JSON de l'appareil existe
                    if os.path.exists(var_path):
                        with open(var_path, 'r') as f:
                            # Charger les données de l'appareil
                            device_data = json.load(f)
                        
                            # Vérifier si l'appareil a une adresse IP valide et si elle est déjà dans la liste ip_list
                            ipv4 = device_data.get('ipv4')
                            if ipv4 and ipv4 not in ip_list:
                                ip_list.append(ipv4)  # Ajouter l'adresse IP à la liste si elle est unique
                            else:
                                # Si l'IP existe déjà dans la liste, on supprime l'appareil
                                self.objManager.remove_device(device=device)
                                self.objManager.save_network()  # Sauvegarder l'état du réseau après la suppression
        except Exception as e:
            # Loguer l'erreur en cas de problème
            logging.error(f"Erreur lors du nettoyage du réseau : {str(e)}")

    def toggle_scan(self):
        # si le scan n'est pas actif alors proposer la fonction run
        self.scan_btn.setIcon(qtawesome.icon('mdi6.play-speed'))
        # si le scan est lancé alors proposer la fonction stop
        self.scan_btn.setIcon(qtawesome.icon('mdi6.close-octagon'))

    def run_scan(self):
        pass

    def stop_scan(self):
        pass


class SyncDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Syncing Data")
        self.setFixedSize(300, 100)

        # Layout principal
        layout = QVBoxLayout(self)

        # Barre de progression
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)

        # Bouton d'annulation
        self.cancel_btn = QPushButton("Cancel", self)
        layout.addWidget(self.cancel_btn)
        self.cancel_btn.clicked.connect(self.reject)  # Rejet du dialogue

    def update_progress(self, value):
        self.progress_bar.setValue(value)


class DevicesCards(CardStackGeneral):
    def __init__(
            self, 
            obj_title: str, 
            obj_lang: LanguageApp, 
            obj_view: Network, 
            obj_icon: IconsApp,
            parent=None):
        super().__init__(obj_title, obj_lang, obj_view, parent)
        logging.info(self.objManager)
    
    def setCardList(self):
        self.card_list = []
        img_default = QImage("C:\\Users\\g.tronche\\Documents\\GitHub\\affinity\\svg\\circle\\gray\\c_client.svg")
        
        if self.objManager.devicesList is not []:
            for device in self.objManager.devicesList:
                var_path = os.path.join(os.path.dirname(os.path.dirname(self.objManager.absPath)), "desktop",f"{device}.json")
                if os.path.exists(var_path):
                    with open(var_path, 'r') as f:
                        device_data = json.load(f)
                        ipv4 = device_data.get('ipv4', 'value unknown') or 'value unknown'
                        name = device_data.get('name', 'value unknown') or 'value unknown'
                        self.card_list.append({
                            "icon_card": None,
                            "title_card": QLabel(f"{name}({ipv4})"),
                            "img_card": img_default.scaled(50, 50, Qt.KeepAspectRatio),
                            "corps_card": QLabel(f"Mac Address: {device_data.get('mac', 'value unknown') or 'value unknown'}"),
                        })
        else:
            self.card_list.append({
                "icon_card": None,
                "title_card": QLabel("No device found"),
                "img_card": None,
                "corps_card": QLabel("No device found"),
            })