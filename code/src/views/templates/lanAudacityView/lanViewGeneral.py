"""
    Informations:
        'LanViewGeneral' est une mise à jour de 'LanTabView'
    Commentaires:
        Suite à la modification de la classe mère 'GeneralTabsView' en 'LanAudacityViewGeneral',
        nous avons modifié certains paramètres pour cela nous avons créé une nouvelle classe.
        Nous avons également modifié la classe pour permettre aux enfants d'avoir les bonnes données.
"""
from qtpy.QtCore import QThreadPool

from typing import Optional

from src.classes.classesExport import ConfigurationFile, LanguageApp, IconsApp
from src.views.templates.WelcomeView.defaultTab import MonitorWD
from src.views.templates.templatesExport import LanAudacityViewGeneral
from src.views.templates.new_export import NetworkGeneralDMC, DevicesDMC, LanDashboardFMC
from src.views.mapTemplateViews import LANMap
from src.components.bakend_dialog import SyncWorker, WDialogs


class LanViewGeneral(LanAudacityViewGeneral):
    def __init__(
            self, 
            title_panel: str,
            external_object: ConfigurationFile,
            language_manager: Optional[LanguageApp] = None,
            icons_manager: Optional[IconsApp] = None,
            parent = None
            ) -> None:
        super(LanViewGeneral, self).__init__(title_panel, external_object, language_manager, icons_manager, parent)

    def setListBtn(self):
        data = [
            {
                "name": "General",
                "tooltip": "General",
                "icon": "dashboardBtn",
                "action": self.generalBtn,
            },
            {
                "name": "Preferences",
                "tooltip": "Preferences",
                "icon": "settingsBtn",
                "action": self.preferencesBtn,
            },
            {
                "name": "Network Map",
                "tooltip": "Network Map",
                "icon": "lan_audacity",
                "action": self.networkMapBtn,
            },
            {
                "name": "Devices",
                "tooltip": "List of configurable hardware on the network",
                "icon": "deviceListBtn",
                "action": self.devicesBtn,
            },
            {
                "name": "Network Road Map",
                "tooltip": "Network Road Map",
                "icon": "defaultIcon",
                "action": self.networkRoadMapBtn,
            },
            {
                "name": "Sync",
                "tooltip": "Sync",
                "icon": "refreshWebBtn",
                "action": self.syncBtn,
            },
        ]
        return data
    
    def initDisplay(self):
        self.general_menu = LanDashboardFMC(
            "Dashboard", self.languageManager, self.externalObject, self.iconsManager, self
        )
        self.stackedFields.addWidget(self.general_menu)

        self.preferences_menu = NetworkGeneralDMC(
            "Settings", self.languageManager, self.externalObject, self
        )
        self.stackedFields.addWidget(self.preferences_menu)

        self.network_map_menu = LANMap(
            "Network Map", self.languageManager, self.externalObject, self
        )
        self.stackedFields.addWidget(self.network_map_menu)

        self.devices_menu = DevicesDMC(
            "Devices List", self.languageManager, self.externalObject, self.iconsManager, self
        )
        self.stackedFields.addWidget(self.devices_menu)

        self.network_road_map_menu = MonitorWD(
            icons_manager=self.iconsManager,
            language_manager=self.languageManager,
            parent=self
        )
        self.stackedFields.addWidget(self.network_road_map_menu)

    def generalBtn(self):
        self.stackedFields.setCurrentWidget(self.general_menu)

    def preferencesBtn(self):
        self.stackedFields.setCurrentWidget(self.preferences_menu)

    def networkMapBtn(self):
        self.stackedFields.setCurrentWidget(self.network_map_menu)

    def devicesBtn(self):
        self.stackedFields.setCurrentWidget(self.devices_menu)

    def networkRoadMapBtn(self):
        self.stackedFields.setCurrentWidget(self.network_road_map_menu)

    def syncBtn(self):
        # Ouvrir la nouvelle fenêtre avec la progressBar
        self.sync_dialog = WDialogs()
        self.sync_dialog.show()

        # Initialiser SyncWorker
        self.sync_worker = SyncWorker(self.externalObject, self)
        self.sync_worker.signals.progress.connect(self.sync_dialog.update_progress)
        self.sync_worker.signals.finished.connect(self.sync_dialog.close)

        # Utiliser QThreadPool pour exécuter la tâche en arrière-plan
        QThreadPool.globalInstance().start(self.sync_worker)
