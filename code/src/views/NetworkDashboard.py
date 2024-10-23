import logging

import qtawesome as qta
from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *
from typing import Any

from src.classes.languageApp import LanguageApp
from src.classes.cl_network import Network
from src.classes.iconsApp import IconsApp

from src.views.templatesViews import TitleWithAction, Card, LineUpdate, RoundedBtn
from src.components.bakend_dialog import WorkerGetUcList, WDialogs, WorkerDevice


class DashboardCardTemplate(QWidget):
    def __init__(self,
                 obj_title: str,
                 obj_lang: LanguageApp,
                 obj_view: Any,
                 obj_icon: IconsApp,
                 parent=None):
        super().__init__(parent)
        # Préparation à l'environnement
        self.cardList: list = []
        # Préparation aux Data
        self.stackTitle = obj_title
        self.langManager = obj_lang
        self.objManager = obj_view
        self.iconsManager = obj_icon

        self.worker = None
        self.progress_dialog = None

        self.initUI()           # init User Interface
        self.clearCardLayout()  # clear the cards space
        self.setCardsList()     # set the cards information
        self.setCardsView()     # show the cards

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

    def setCardsList(self):
        self.cardList = [
            {
                "layout": {
                    "row": 0,
                    "column": 0,
                    "rowSpan": None,
                    "columnSpan": None,
                    "alignement": None
                },
                "icon_card": self.iconsManager.get_icon("defaultIcon"),
                "title_card": QLabel("Hello World!"),
                "img_card": None,
                "corps_card": QLabel("Welcome!")
            }
        ]

    def setCardsView(self):
        for settings_card in self.cardList:
            layout_settings = settings_card["layout"]
            card_obj = Card(
                icon_card=settings_card["icon_card"],
                title_card=settings_card["title_card"],
                img_card=settings_card["img_card"],
                corps_card=settings_card["corps_card"],
            )
            if (layout_settings["rowSpan"] or layout_settings["columnSpan"]) is None:
                self.card_layout.addWidget(
                    card_obj,
                    layout_settings["row"],
                    layout_settings["column"]
                )
            else:
                self.card_layout.addWidget(
                card_obj,
                layout_settings["row"],
                layout_settings["column"],
                layout_settings["rowSpan"],
                layout_settings["columnSpan"]
            )


class LanDashboard(DashboardCardTemplate):
    def __init__(self, obj_title: str, obj_lang: LanguageApp, obj_view: Network, obj_icon: IconsApp, parent=None):
        """
        Initialise l'interface de tableau de bord LAN avec les cartes et les composants réseau.

        :param obj_title: Titre de l'objet.
        :param obj_lang: Instance de la gestion de la langue.
        :param obj_view: Instance représentant les informations réseau.
        :param obj_icon: Instance de gestion des icônes.
        :param parent: Widget parent, facultatif.
        """
        super().__init__(obj_title, obj_lang, obj_view, obj_icon, parent)
        self.setCardsList()  # Crée les cartes de l'interface
        self.setUCList()  # Crée la liste des périphériques
        self.setUCNetworkList()  # Crée la liste du réseau
        self.setInfoTableList()  # Crée la table d'informations
        

        # Initialiser les autres tables avec des listes vides
        self.updateUcListTable([])
        self.updateUcNetworkListTable([])
        self.updateInfoTableList([])

        # Met en place les cartes de l'interface utilisateur
        self.setCardsView()

    def setCardsList(self):
        wanBody = QWidget(self)
        wanLayout = QVBoxLayout(wanBody)

        domainNameTtl = "Domain Name"
        domainNameEdit = QLineEdit(self.objManager.dns)
        wanLayout.addWidget(LineUpdate(domainNameTtl, domainNameEdit))

        gateTtl = "Gateway"
        gateEdit = QLineEdit(self.objManager.gateway)
        wanLayout.addWidget(LineUpdate(gateTtl, gateEdit))

        # Exemple de personnalisation pour LanDashboard
        self.cardList = [
            {
                "layout": {
                    "row": 0,
                    "column": 0,
                    "rowSpan": None,
                    "columnSpan": None,
                    "alignement": None
                },
                "icon_card": self.iconsManager.get_icon("lanIcon"),
                "title_card": QLabel("WAN Status"),
                "img_card": None,
                "corps_card": wanBody
            }
        ]

    def setUCList(self):
        uc_listHeadband: list = ["IPv4", "Name", "Mac Address", "Status", "Vendor"]
        self.uc_listBody = QTableWidget(self)
        self.uc_listBody.setColumnCount(len(uc_listHeadband))
        self.uc_listBody.setHorizontalHeaderLabels(uc_listHeadband)
        
        self.scan_btn = RoundedBtn(icon=self.iconsManager.get_icon(
            "runIcon"), text=None, parent=self)
        self.scan_btn.clicked.connect(self.toggle_scan)
        self.scan_btn.setToolTip("Start the scan")
        self.scan_btn.setEnabled(True)

        self.pause_btn = RoundedBtn(icon=self.iconsManager.get_icon(
            "pauseIcon"), text=None, parent=self)
        self.pause_btn.clicked.connect(self.toggle_scan)
        self.pause_btn.setToolTip("Scan not loaded")
        self.pause_btn.setEnabled(False)

        self.trash_btn = RoundedBtn(
            icon=self.iconsManager.get_icon("trashIcon"), text=None, parent=self)
        self.trash_btn.setToolTip("Clean the scan")
        self.trash_btn.clicked.connect(self.trash_scan)

        ttls_btn = [self.scan_btn, self.pause_btn, self.trash_btn]
        uc_listTtl = TitleWithAction(f'LAN {self.objManager.dns}', 4, ttls_btn)

        uc_list_settings: dict = {
            "layout": {
                "row": 0,
                "column": 1,
                "rowSpan": 1,
                "columnSpan": 3,
                "alignement": None
            },
            "icon_card": self.iconsManager.get_icon("lanUcListIcon"),
            "title_card": uc_listTtl,
            "img_card": None,
            "corps_card": self.uc_listBody
        }
        self.cardList.append(uc_list_settings)

    def updateUcListTable(self, uc_list: list):
        self.uc_listBody.setRowCount(len(uc_list))
        for i, uc in enumerate(uc_list):
            self.uc_listBody.setItem(i, 0, QTableWidgetItem(uc["ipv4"]))
            self.uc_listBody.setItem(i, 1, QTableWidgetItem(uc["name"]))
            self.uc_listBody.setItem(i, 2, QTableWidgetItem(uc["mac"]))
            self.uc_listBody.setItem(i, 3, QTableWidgetItem(uc["status"]))
            self.uc_listBody.setItem(i, 4, QTableWidgetItem(str(uc["vendor"])))

    def getUcList(self):
        """
        Démarre l'obtention de la liste des UC de manière asynchrone via un Worker.
        """
        # Crée la boîte de dialogue de progression
        self.progress_dialog = WDialogs()
        self.progress_dialog.set_maximum(len(self.objManager.devicesList))  # Indéfini (0) pour une tâche dont on ne connaît pas la durée
        self.progress_dialog.set_message("Fetching the list of devices...")

        # Crée un Worker pour récupérer les UC
        self.worker = WorkerGetUcList(self.objManager)

        # Connecte les signaux du Worker aux méthodes de la boîte de dialogue
        self.worker.signals.progress.connect(self.progress_dialog.update_progress)
        self.worker.signals.started.connect(lambda: self.progress_dialog.show())
        self.worker.signals.result.connect(self.on_getUcList_finished)
        self.worker.signals.finished.connect(self.progress_dialog.close)

        # Démarre le Worker dans un thread séparé
        QThreadPool.globalInstance().start(self.worker)

    def on_getUcList_finished(self, result):
        """
        Méthode appelée lorsque la récupération de la liste des UC est terminée.
        :param result: Liste des UC obtenus.
        """
        self.updateUcListTable(result)
        self.scan_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)

    def toggle_scan(self):
        """
        Vérifie si le scan est en cours et le démarre, le met en pause, ou le reprend.
        """
        if self.scan_btn.isEnabled():
            self.run_scan()
        elif self.scan_btn.isEnabled() and self.worker.is_paused:
            self.resume_scan()
        else:
            self.pause_scan()

    def run_scan(self):
        """
        Démarre le scan en lançant le WorkerDevice dans un thread avec une boîte de dialogue de progression.
        """
        # Crée la boîte de dialogue de progression
        self.progress_dialog = WDialogs()
        self.progress_dialog.set_maximum(100)
        self.progress_dialog.set_message("Scanning for devices...")

        # Crée les données réseau à scanner
        obj_data = {
            "ipv4": self.objManager.ipv4,  # Remplacez par les données réelles de votre objet
            "mask": self.objManager.maskIpv4  # Remplacez par le masque réel
        }

        # Crée un WorkerDevice pour gérer le scan de périphériques
        worker = WorkerDevice(obj_data)

        # Connecte les signaux du Worker aux méthodes de la boîte de dialogue
        worker.signals.started.connect(lambda: self.progress_dialog.show())
        worker.signals.progress.connect(self.progress_dialog.update_progress)
        worker.signals.result.connect(self.on_scan_finished)
        worker.signals.finished.connect(self.progress_dialog.close)

        # Démarre le Worker dans un thread séparé
        QThreadPool.globalInstance().start(worker)

    def on_scan_finished(self, result):
        """
        Méthode appelée lorsque le scan est terminé.
        """
        logging.debug(result)
        self.updateUcListTable(result)
        self.scan_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)

    def pause_scan(self):
        """
        Met en pause le scan du réseau local.
        """
        if self.worker:  # Vérifie si un worker de scan est actif
            self.worker.pause()
            self.pause_btn.setEnabled(False)  # Désactive le bouton de pause
            self.pause_btn.setToolTip("Scan paused")
            self.scan_btn.setEnabled(True)  # Réactive le bouton de reprise
            self.scan_btn.setToolTip("Resume the scan")

    def resume_scan(self):
        """
        Reprend le scan du réseau local après une pause.
        """
        if self.worker:  # Vérifie si un worker de scan est actif
            self.worker.resume()
            self.scan_btn.setEnabled(False)  # Désactive le bouton de reprise
            self.scan_btn.setToolTip("Scanning in Progress")
            self.pause_btn.setEnabled(True)  # Active le bouton de pause
            self.pause_btn.setToolTip("Pause the scan")

    def trash_scan(self):
        """
        Supprime les données (inutiles, les doublons, etc...) de uc_listBody
        """
        pass

    def setUCNetworkList(self):
        ucNetwork_listHeadband: list = ["Name/IPv4", "Emit", "Send"]
        self.ucNetwork_listBody = QTableWidget(self)
        self.ucNetwork_listBody.setColumnCount(len(ucNetwork_listHeadband))
        self.ucNetwork_listBody.setHorizontalHeaderLabels(
            ucNetwork_listHeadband)

        ucNetwork_list_settings: dict = {
            "layout": {
                "row": 1,
                "column": 0,
                "rowSpan": 1,
                "columnSpan": 2,
                "alignement": None
            },
            "icon_card": qta.icon('mdi6.clipboard-text-multiple'),
            "title_card": QLabel("List of network equipment"),
            "img_card": None,
            "corps_card": self.ucNetwork_listBody
        }
        self.cardList.append(ucNetwork_list_settings)

    def updateUcNetworkListTable(self, ucNetwork_list: list):
        self.ucNetwork_listBody.setRowCount(len(ucNetwork_list))
        for i, uc in enumerate(ucNetwork_list):
            self.ucNetwork_listBody.setItem(
                i, 0, QTableWidgetItem(uc["name"] or uc["ipv4"]))
            self.ucNetwork_listBody.setItem(i, 1, QTableWidgetItem(uc["emit"]))
            self.ucNetwork_listBody.setItem(i, 2, QTableWidgetItem(uc["send"]))

    # Asynchrone function return a list of dict
    async def getUcNetworkList(self):
        # return await self.objManager.get_lan_uc_network_list()
        return []

    def setInfoTableList(self):
        infoTable_listHeadband: list = ["Time", "Hostname/IPv4", "Message"]
        self.infoTable_listBody = QTableWidget(self)
        self.infoTable_listBody.setColumnCount(len(infoTable_listHeadband))
        self.infoTable_listBody.setHorizontalHeaderLabels(
            infoTable_listHeadband)

        infoTable_list_settings: dict = {
            "layout": {
                "row": 1,
                "column": 2,
                "rowSpan": 1,
                "columnSpan": 2,
                "alignement": None
            },
            "icon_card": qta.icon('mdi6.clipboard-alert'),
            "title_card": QLabel('Current Problems'),
            "img_card": None,
            "corps_card": self.infoTable_listBody
        }
        self.cardList.append(infoTable_list_settings)

    def updateInfoTableList(self, infoTable_list: list):
        self.infoTable_listBody.setRowCount(len(infoTable_list))
        for i, info in enumerate(infoTable_list):
            self.infoTable_listBody.setItem(
                i, 0, QTableWidgetItem(info["time"]))
            self.infoTable_listBody.setItem(
                i, 1, QTableWidgetItem(info["name"] or info["ipv4"]))
            self.infoTable_listBody.setItem(
                i, 2, QTableWidgetItem(info["message"]))

    # Asynchrone function return a list of dict
    async def getInfoTableList(self):
        # return await self.objManager.get_lan_info_table_list()
        return []


class UCDashboard(DashboardCardTemplate):
    def __init__(self, obj_title: str, obj_lang: LanguageApp, obj_view: Any, obj_icon: IconsApp, parent=None):
        super().__init__(obj_title, obj_lang, obj_view, obj_icon, parent)

    def setCardsList(self):
        # Exemple de personnalisation pour UCDashboard
        self.cardList = [
            {
                "layout": {
                    "row": 0,
                    "column": 0,
                    "rowSpan": None,
                    "columnSpan": None,
                    "alignement": None
                },
                "icon_card": self.iconsManager.get_icon("ucIcon"),
                "title_card": QLabel("User Control"),
                "img_card": None,
                "corps_card": QLabel("Manage your users and permissions here.")
            }
        ]
