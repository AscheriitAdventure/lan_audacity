from src.views.new.templates_2 import FixedMosaicsCards as FMC

from qtpy.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTableWidget, QAbstractItemView, QTableWidgetItem, QSizePolicy, QLabel
from qtpy.QtCore import QThreadPool
import qtawesome as qta
import logging

from src.classes.languageApp import LanguageApp
from src.classes.iconsApp import IconsApp
from src.classes.cl_network import Network

from src.views.templatesViews import LineUpdate, RoundedBtn, TitleWithAction

from src.functionsExt import ip_to_cidr, conv_unix_to_datetime
from src.components.card.cl_card import CardHeader
from src.components.bakend_dialog import WorkerGetUcList, WDialogs

"""
    Nom complet: Lan Dashboard Fixed Mosaics Cards
    Description: Cette classe est une mise à jour de 'LanDashboard(DashboardCardTemplate)'
    Nouveau nom: LanDashboardFMC
"""


class LanDashboardFMC(FMC):
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

        domainProjectNameTtl = "Project Name"
        domainProjectNameEdit = QLineEdit(self.objManager.name)
        domainProjectNameEdit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        wanLayout.addWidget(LineUpdate(domainProjectNameTtl, domainProjectNameEdit))

        domainNameTtl = "Domain Name"
        domainNameEdit = QLineEdit(self.objManager.dns)
        domainNameEdit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        wanLayout.addWidget(LineUpdate(domainNameTtl, domainNameEdit))

        cidrTtl = "CIDR"
        cidrText = ip_to_cidr(self.objManager.ipv4, self.objManager.maskIpv4)
        cidrEdit = QLineEdit(cidrText)
        cidrEdit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        cidrEdit.setPlaceholderText("CIDR")

        if self.objManager.ipv6:
            cidrEdit.setToolTip(f"IPv6: {self.objManager.ipv6}")
        else:
            cidrEdit.setToolTip(f"IPv6: Not Setted")

        wanLayout.addWidget(LineUpdate(cidrTtl, cidrEdit))
        gateTtl = "Gateway"
        gateEdit = QLineEdit(self.objManager.gateway)
        gateEdit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        wanLayout.addWidget(LineUpdate(gateTtl, gateEdit))

        startDateTtl = "Start Date"
        startDateEdit = QLineEdit(conv_unix_to_datetime(self.objManager.clockManager.clockCreated))
        startDateEdit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        wanLayout.addWidget(LineUpdate(startDateTtl, startDateEdit))

        lastUpdateTtl = "Last Update"
        lastUpdateEdit = QLineEdit(conv_unix_to_datetime(self.objManager.clockManager.get_clock_last()))
        lastUpdateEdit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        wanLayout.addWidget(LineUpdate(lastUpdateTtl, lastUpdateEdit))

        wanLayout.addStretch()

        # Exemple de personnalisation pour LanDashboard
        self.cardList = [
            {
                "layout": {
                    "row": 0,
                    "column": 0,
                    "rowSpan": 1,
                    "columnSpan": 1,
                    "alignement": None
                },
                "top_card": CardHeader(
                    title_card=QLabel("WAN Status"),
                    icon_card=self.iconsManager.get_icon("lanIcon")),
                "center_card": wanBody,
            "left_card": None,
            "right_card": None,
            "bottom_card": None
            }
        ]

    def setUCList(self):
        uc_listHeadband: list = ["IPv4", "Name", "Mac Address", "Status", "Vendor"]
        self.uc_listBody = QTableWidget(self)
        self.uc_listBody.setColumnCount(len(uc_listHeadband))
        self.uc_listBody.setHorizontalHeaderLabels(uc_listHeadband)
        self.uc_listBody.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.uc_listBody.setSortingEnabled(True)
        
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

        ttls_btn = [self.scan_btn, self.pause_btn]
        uc_listTtl = TitleWithAction(f'LAN {self.objManager.dns}', 4, ttls_btn)

        uc_list_settings: dict = {
            "layout": {
                "row": 0,
                "column": 1,
                "rowSpan": 1,
                "columnSpan": 3,
                "alignement": None
            },
            "top_card": CardHeader(
                title_card=uc_listTtl,
                icon_card=self.iconsManager.get_icon("lanUcListIcon")),
            "center_card": self.uc_listBody,
            "left_card": None,
            "right_card": None,
            "bottom_card": None
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

    def run_scan(self):
        """
        Démarre l'obtention de la liste des UC de manière asynchrone via un Worker.
        """
        self.scan_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        # Crée la boîte de dialogue de progression
        self.progress_dialog = WDialogs()
        self.progress_dialog.set_maximum(len(self.objManager.devicesList))  # Indéfini (0) pour une tâche dont on ne connaît pas la durée
        self.progress_dialog.set_message("Fetching the list of devices...")

        # Crée un Worker pour récupérer les UC
        self.worker = WorkerGetUcList(self.objManager)

        # Connecte les signaux du Worker aux méthodes de la boîte de dialogue
        self.worker.signals.progress.connect(self.progress_dialog.update_progress)
        self.worker.signals.started.connect(lambda: self.progress_dialog.show())
        self.worker.signals.result.connect(self.on_scan_finished)
        self.worker.signals.finished.connect(self.progress_dialog.close)

        # Démarre le Worker dans un thread séparé
        QThreadPool.globalInstance().start(self.worker)

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

    def on_scan_finished(self, result):
        """
        Méthode appelée lorsque le scan est terminé.
        """
        logging.debug(f"303: {result}")
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
            "top_card": CardHeader(
                title_card=QLabel("List of network equipment"),
                icon_card=qta.icon('mdi6.clipboard-text-multiple')),
            "center_card": self.ucNetwork_listBody,
            "left_card": None,
            "right_card": None,
            "bottom_card": None
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
            "top_card": CardHeader(
                title_card=QLabel("Current Problems"),
                icon_card=qta.icon('mdi6.clipboard-alert')),
            "center_card": self.infoTable_listBody,
            "left_card": None,
            "right_card": None,
            "bottom_card": None
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

