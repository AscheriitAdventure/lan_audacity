# import logging

from typing import Any, Optional

from qtpy.QtCore import Qt, QThreadPool
from qtpy.QtWidgets import (
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QPushButton,
    QStackedLayout,
    QTabWidget,
)

# from src.functionsExt import ip_to_cidr
# from src.classes.cl_device import Device
from src.classes.cl_network import Network
from src.classes.languageApp import LanguageApp
from src.classes.iconsApp import IconsApp
from src.views.mapTemplateViews import LANMap
from src.views.preferences import (
    PreferencesGeneral,
    NetworkGeneral,
    DevicesCards,
    PaletteIconSettings,
)
from src.views.NetworkDashboard import LanDashboard
from src.components.bakend_dialog import SyncWorker, WDialogs


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


class GeneralTabsView(QWidget):
    def __init__(
        self,
        title_panel: str,
        ext_obj: Optional[Any] = None,
        lang_manager: Optional[LanguageApp] = None,
        icons_manager: Optional[IconsApp] = None,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.langManager = lang_manager
        self.iconsManager = icons_manager
        self.extObj = ext_obj
        self.viewTitle = title_panel

        self.glbLayout = QGridLayout(self)
        self.setLayout(self.glbLayout)

        self.btnList = self.setListBtn()
        self.initUI()
        self.initDisplay()

    def initUI(self):
        # Set list button
        btn_container = QWidget(self)
        btn_container_layout = QVBoxLayout(btn_container)
        btn_container_layout.setContentsMargins(0, 0, 0, 0)
        btn_container.setLayout(btn_container_layout)
        self.glbLayout.addWidget(btn_container, 0, 0, Qt.AlignLeft | Qt.AlignTop)

        for btn in self.btnList:
            btn_obj = QPushButton(btn["name"], self)
            btn_obj.setIcon(self.iconsManager.get_icon(btn["icon"]))
            btn_obj.setToolTip(btn["tooltip"])
            btn_obj.clicked.connect(btn["action"])
            btn_container_layout.addWidget(btn_obj)

        self.stackedFields = QStackedLayout()
        self.glbLayout.addLayout(self.stackedFields, 0, 1, Qt.AlignTop)

    def initDisplay(self):
        # Create views for each menu
        self.info_menu = QWidget(self)
        self.stackedFields.addWidget(self.info_menu)

        self.notif_menu = QWidget(self)
        self.stackedFields.addWidget(self.notif_menu)

    def setListBtn(self) -> list:
        data = [
            {
                "name": "News",
                "tooltip": "News",
                "icon": "defaultIcon",
                "action": self.notifications_btn,
            },
            {
                "name": "&Preferences",
                "tooltip": "&Preferences",
                "icon": "defaultIcon",
                "action": self.informations_btn,
            },
        ]
        return data

    def notifications_btn(self):
        self.stackedFields.setCurrentWidget(self.notif_menu)

    def informations_btn(self):
        self.stackedFields.setCurrentWidget(self.info_menu)


class PreferencesTabView(GeneralTabsView):
    def __init__(
        self,
        title_panel: str,
        ext_obj: Optional[Any] = None,
        lang_manager: Optional[LanguageApp] = None,
        icons_manager: Optional[IconsApp] = None,
        parent=None,
    ) -> None:
        super().__init__(title_panel, ext_obj, lang_manager, icons_manager, parent)

    def setListBtn(self) -> list:
        data = [
            {
                "name": "General",
                "tooltip": "General",
                "icon": "dashboardBtn",
                "action": self.general_btn,
            },
            {
                "name": "Language",
                "tooltip": "Language",
                "icon": "defaultIcon",
                "action": self.language_btn,
            },
            {
                "name": "Palette Shortcut",
                "tooltip": "Palette Shortcut",
                "icon": "defaultIcon",
                "action": self.palette_shortcut_btn,
            },
            {
                "name": "Palette Icon",
                "tooltip": "Palette Icon",
                "icon": "paletteSwatch",
                "action": self.palette_icon_btn,
            },
            {
                "name": "License",
                "tooltip": "License",
                "icon": "defaultIcon",
                "action": self.about_btn,
            },
            {
                "name": "Theme",
                "tooltip": "Theme",
                "icon": "defaultIcon",
                "action": self.theme_btn,
            },
            {
                "name": "Update",
                "tooltip": "Update",
                "icon": "defaultIcon",
                "action": self.update_btn,
            },
        ]
        return data

    def initDisplay(self):
        self.general_menu = PreferencesGeneral(
            obj_title="Dashboard",
            obj_lang=self.langManager,
            obj_view=self.extObj,
            parent=self,
        )
        self.stackedFields.addWidget(self.general_menu)

        self.language_menu = QWidget(self)
        self.stackedFields.addWidget(self.language_menu)

        self.palette_shortcut_menu = QWidget(self)
        self.stackedFields.addWidget(self.palette_shortcut_menu)

        self.about_menu = QWidget(self)
        self.stackedFields.addWidget(self.about_menu)

        self.theme_menu = QWidget(self)
        self.stackedFields.addWidget(self.theme_menu)

        self.update_menu = QWidget(self)
        self.stackedFields.addWidget(self.update_menu)

        self.palette_icon_menu = PaletteIconSettings(
            obj_title="Palette Icon",
            obj_lang=self.langManager,
            obj_view=self.iconsManager,
            obj_icon=self.iconsManager,
            parent=self,
        )
        self.stackedFields.addWidget(self.palette_icon_menu)

    def general_btn(self):
        self.stackedFields.setCurrentWidget(self.general_menu)

    def language_btn(self):
        self.stackedFields.setCurrentWidget(self.language_menu)

    def palette_shortcut_btn(self):
        self.stackedFields.setCurrentWidget(self.palette_shortcut_menu)

    def about_btn(self):
        self.stackedFields.setCurrentWidget(self.about_menu)

    def theme_btn(self):
        self.stackedFields.setCurrentWidget(self.theme_menu)

    def update_btn(self):
        self.stackedFields.setCurrentWidget(self.update_menu)

    def palette_icon_btn(self):
        self.stackedFields.setCurrentWidget(self.palette_icon_menu)


class LanTabView(GeneralTabsView):
    def __init__(
        self,
        title_panel: str,
        ext_obj: Optional[Network] = None,
        lang_manager: Optional[LanguageApp] = None,
        icons_manager: Optional[IconsApp] = None,
        parent=None,
    ) -> None:
        super().__init__(title_panel, ext_obj, lang_manager, icons_manager, parent)

    def setListBtn(self) -> list:
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
        self.general_menu = LanDashboard(
            "Dashboard", self.langManager, self.extObj, self.iconsManager, self
        )
        self.stackedFields.addWidget(self.general_menu)

        self.preferences_menu = NetworkGeneral(
            "Settings", self.langManager, self.extObj, self
        )
        self.stackedFields.addWidget(self.preferences_menu)

        self.network_map_menu = LANMap(
            "Network Map", self.langManager, self.extObj, self
        )
        self.stackedFields.addWidget(self.network_map_menu)

        self.devices_menu = DevicesCards(
            "Devices List", self.langManager, self.extObj, self.iconsManager, self
        )
        self.stackedFields.addWidget(self.devices_menu)

        self.network_road_map_menu = QWidget(self)
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
        self.sync_worker = SyncWorker(self.extObj, self)
        self.sync_worker.signals.progress.connect(self.sync_dialog.update_progress)
        self.sync_worker.signals.finished.connect(self.sync_dialog.close)

        # Utiliser QThreadPool pour exécuter la tâche en arrière-plan
        QThreadPool.globalInstance().start(self.sync_worker)
