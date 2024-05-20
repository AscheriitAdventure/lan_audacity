from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from src.models.worker import Worker
from src.models.lang_app import LanguageApp
from src.models.shortcut_app import ShortcutApp
from src.models.device import Device
from src.models.conf_file import ConfigurationFile
from src.models.network_map import NetworkMap
from src.views.network_menu import *
import qtawesome as qta
import logging


class GeneralTabsView(QWidget):
    def __init__(self, lang_manager: LanguageApp, model_obj: any = None, parent=None):
        super().__init__(parent)
        self.langManager = lang_manager
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.model_obj = model_obj
        self.set_list_btn()
        self.setUI()

    def set_list_btn(self):
        self.welcomeBtnList = [
            {
                "name_btn": self.langManager.get_textTranslate("News"),
                "tooltip": self.langManager.get_textTranslate("News"),
                "icon": qta.icon("fa5s.bell"),
                "action": self.notifications_btn,
            },
            {
                "name_btn": self.langManager.get_textTranslate("&Preferences"),
                "tooltip": self.langManager.get_textTranslate("&Preferences"),
                "icon": qta.icon("fa5s.info"),
                "action": self.informations_btn,
            },
        ]

    def setUI(self):
        # Set list button
        btn_container = QWidget(self)
        btn_container_layout = QVBoxLayout(btn_container)
        btn_container_layout.setContentsMargins(0, 0, 0, 0)
        btn_container.setLayout(btn_container_layout)
        self.layout.addWidget(btn_container, 0, 0, Qt.AlignLeft | Qt.AlignTop)

        for btn in self.welcomeBtnList:
            btn_obj = QPushButton(btn["icon"], btn["name_btn"], self)
            btn_obj.setToolTip(btn["tooltip"])
            btn_obj.clicked.connect(btn["action"])
            btn_container_layout.addWidget(btn_obj)

        self.stacked_layout = QStackedLayout()
        self.layout.addLayout(self.stacked_layout, 0, 1, Qt.AlignTop)
        self.set_menu()

        self.btn_thread = QPushButton(self)
        btn_container_layout.addWidget(self.btn_thread)
        self.spin_anm = qta.Spin(self.btn_thread, autostart=False)
        ico_th = qta.icon('fa5s.circle-notch', color='RoyalBlue', animation=self.spin_anm)
        self.btn_thread.setIcon(ico_th)
        self.btn_thread.hide()
    
    def runThreadFunc(self, method) -> None:
        self.btn_thread.show()
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
            self.btn_thread.show()
        else:
            self.spin_anm.stop()
            self.btn_thread.hide()
     
    def set_menu(self):
        # Create views for each menu
        self.info_menu = QWidget(self)
        self.stacked_layout.addWidget(self.info_menu)

        self.notif_menu = QWidget(self)
        self.stacked_layout.addWidget(self.notif_menu)

    def notifications_btn(self):
        self.runThreadFunc(self.stacked_layout.setCurrentWidget(self.notif_menu))

    def informations_btn(self):
        self.runThreadFunc(self.stacked_layout.setCurrentWidget(self.info_menu))


class NetworkMapTab(GeneralTabsView):
    def __init__(self, lang_manager: LanguageApp, model_obj: NetworkMap, parent=None):
        super().__init__(lang_manager, model_obj, parent)
        logging.debug(self.model_obj)
        self.set_list_btn()
        self.setUI()

    def set_list_btn(self):
        super().set_list_btn()
        self.welcomeBtnList.extend(
            [
                {
                    "name_btn": self.langManager.get_textTranslate("Edit Network Map"),
                    "tooltip": self.langManager.get_textTranslate("Edit Network Map"),
                    "icon": qta.icon("fa5s.paint-brush"),
                    "action": self.edit_device_btn,
                },
                {
                    "name_btn": self.langManager.get_textTranslate("Device List"),
                    "tooltip": self.langManager.get_textTranslate("Device List"),
                    "icon": qta.icon("fa5s.list"),
                    "action": self.device_list_btn,
                },
                {
                    "name_btn": self.langManager.get_textTranslate("Map Network Drive"),
                    "tooltip": self.langManager.get_textTranslate("Map Network Drive"),
                    "icon": qta.icon("fa5s.network-wired"),
                    "action": self.map_network_drive_btn,
                },
            ]
        )

    def set_menu(self):
        super().set_menu()
        # Create views for each menu
        self.info_menu = NetworkMenu(self.model_obj, self.langManager)
        self.stacked_layout.addWidget(self.info_menu)

        self.edit_device_menu = QWidget(self)
        self.stacked_layout.addWidget(self.edit_device_menu)

        self.device_list_menu = NetworkDeviceList(self.model_obj, self.langManager)
        self.stacked_layout.addWidget(self.device_list_menu)

        self.map_network_drive_menu = QWidget(self)
        self.stacked_layout.addWidget(self.map_network_drive_menu)

    def edit_device_btn(self):
        self.runThreadFunc(self.stacked_layout.setCurrentWidget(self.edit_device_menu))

    def device_list_btn(self):
        self.runThreadFunc(self.stacked_layout.setCurrentWidget(self.device_list_menu))

    def map_network_drive_btn(self):
        self.runThreadFunc(self.stacked_layout.setCurrentWidget(self.map_network_drive_menu))


class DeviceTab(GeneralTabsView):
    def __init__(self, lang_manager: LanguageApp, model_obj: Device, parent=None):
        super().__init__(lang_manager, model_obj, parent)
        self.set_list_btn()
        self.setUI()

    def set_list_btn(self):
        self.welcomeBtnList = [
            {
                "name_btn": self.langManager.get_textTranslate("Edit Device"),
                "tooltip": self.langManager.get_textTranslate("Edit Device"),
                "icon": qta.icon("fa5s.paint-brush"),
                "action": self.edit_device_btn,
            },
            {
                "name_btn": self.langManager.get_textTranslate("Map Network Drive"),
                "tooltip": self.langManager.get_textTranslate("Map Network Drive"),
                "icon": qta.icon("fa5s.network-wired"),
                "action": self.map_network_drive_btn,
            },
        ]

    def set_menu(self):
        # Create views for each menu
        self.info_menu = QWidget(self)
        self.stacked_layout.addWidget(self.info_menu)

        self.edit_device_menu = QWidget(self)
        self.stacked_layout.addWidget(self.edit_device_menu)

        self.map_network_drive_menu = QWidget(self)
        self.stacked_layout.addWidget(self.map_network_drive_menu)

    def edit_device_btn(self):
        self.runThreadFunc(self.stacked_layout.setCurrentWidget(self.edit_device_menu))

    def map_network_drive_btn(self):
        self.runThreadFunc(self.stacked_layout.setCurrentWidget(self.map_network_drive_menu))


class PreferencesTab(GeneralTabsView):
    def __init__(
        self,
        lang_manager: LanguageApp,
        key_manager: ConfigurationFile,
        parent=None,
    ):
        super().__init__(lang_manager, key_manager, parent)
        self.set_list_btn()
        logging.debug(self.model_obj)
        self.setUI()

    def set_list_btn(self):
        self.welcomeBtnList = [
            {
                "name_btn": self.langManager.get_textTranslate("General"),
                "tooltip": self.langManager.get_textTranslate("General"),
                "icon": qta.icon("mdi6.trello"),
                "action": self.general_btn,
            },
            {
                "name_btn": self.langManager.get_textTranslate("Language"),
                "tooltip": self.langManager.get_textTranslate("Language"),
                "icon": qta.icon("mdi6.translate"),
                "action": self.language_btn,
            },
            {
                "name_btn": self.langManager.get_textTranslate("Palette Shortcut"),
                "tooltip": self.langManager.get_textTranslate("Palette Shortcut"),
                "icon": qta.icon("mdi6.keyboard-variant"),
                "action": self.palette_shortcut_btn,
            },
            {
                "name_btn": self.langManager.get_textTranslate("License"),
                "tooltip": self.langManager.get_textTranslate("License"),
                "icon": qta.icon("mdi6.certificate"),
                "action": self.about_btn,
            },
            {
                "name_btn": self.langManager.get_textTranslate("Theme"),
                "tooltip": self.langManager.get_textTranslate("Theme"),
                "icon": qta.icon("fa5s.palette"),
                "action": self.theme_btn,
            },
            {
                "name_btn": self.langManager.get_textTranslate("Update"),
                "tooltip": self.langManager.get_textTranslate("Update"),
                "icon": qta.icon("fa5s.sync-alt"),
                "action": self.update_btn,
            },
        ]

    def set_menu(self):
        # Create views for each menu
        self.general_menu = PreferencesGeneral("General Informations", self.langManager, self.model_obj)
        self.stacked_layout.addWidget(self.general_menu)

        self.language_menu = PreferencesLangues("Languages Informations", self.langManager)
        self.stacked_layout.addWidget(self.language_menu)

        self.palette_shortcut_menu = QWidget(self)
        self.stacked_layout.addWidget(self.palette_shortcut_menu)

        self.about_menu = QWidget(self)
        self.stacked_layout.addWidget(self.about_menu)

        self.theme_menu = QWidget(self)
        self.stacked_layout.addWidget(self.theme_menu)

        self.update_menu = PreferencesUpdate("General Informations", self.langManager, self.model_obj)
        self.stacked_layout.addWidget(self.update_menu)

    def general_btn(self):
        self.runThreadFunc(self.stacked_layout.setCurrentWidget(self.general_menu))

    def language_btn(self):
        self.runThreadFunc(self.stacked_layout.setCurrentWidget(self.language_menu))

    def palette_shortcut_btn(self):
        self.runThreadFunc(self.stacked_layout.setCurrentWidget(self.palette_shortcut_menu))

    def about_btn(self):
        self.runThreadFunc(self.stacked_layout.setCurrentWidget(self.about_menu))

    def theme_btn(self):
        self.runThreadFunc(self.stacked_layout.setCurrentWidget(self.theme_menu))

    def update_btn(self):
        self.runThreadFunc(self.stacked_layout.setCurrentWidget(self.update_menu))


class LogSignInTab(GeneralTabsView):
    def __init__(self, lang_manager: LanguageApp, parent=None):
        super().__init__(lang_manager, parent)
        self.set_list_btn()
        self.setUI()

    def set_list_btn(self):
        self.welcomeBtnList = [
            {
                "name_btn": self.langManager.get_textTranslate("Log In"),
                "tooltip": self.langManager.get_textTranslate("Log In"),
                "icon": qta.icon("fa5s.sign-in-alt"),
                "action": self.log_in_btn,
            },
            {
                "name_btn": self.langManager.get_textTranslate("Sign In"),
                "tooltip": self.langManager.get_textTranslate("Sign In"),
                "icon": qta.icon("fa5s.sign-in-alt"),
                "action": self.sign_in_btn,
            },
        ]

    def set_menu(self):
        # Create views for each menu
        self.sign_in_menu = QWidget(self)
        self.stacked_layout.addWidget(self.sign_in_menu)

        self.log_in_menu = QWidget(self)
        self.stacked_layout.addWidget(self.log_in_menu)

    def sign_in_btn(self):
        self.runThreadFunc(self.stacked_layout.setCurrentWidget(self.sign_in_menu))

    def log_in_btn(self):
        self.runThreadFunc(self.stacked_layout.setCurrentWidget(self.log_in_menu))
