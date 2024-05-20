import logging
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import qtawesome as qta
import nmap

from src.models.conf_file import ConfigurationFile
from src.views.card_view import Card
from src.models.network_map import NetworkMap
from src.models.lang_app import LanguageApp


class NetworkMenu(QWidget):
    def __init__(self, net_obj: NetworkMap, lang_manager: LanguageApp, parent=None):
        super(NetworkMenu, self).__init__(parent)
        self.net_obj = net_obj
        self.langManager = lang_manager
        self.title_stack = "Network"
        self.initUI()

    def initUI(self):
        # Set the general layout
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Set the top widget
        title_widget = QWidget(self)
        self.layout.addWidget(title_widget, alignment=Qt.AlignTop)

        ttl_wdg_cnt = QHBoxLayout(title_widget)
        # Set the title
        title = QLabel(self.langManager.get_textTranslate(self.title_stack))
        title.setFont(QFont("Arial", 12, QFont.Bold))
        ttl_wdg_cnt.addWidget(title, alignment=Qt.AlignCenter)
        ttl_wdg_cnt.addStretch()
        # Set the btn view
        btn_grid5_view = QPushButton(qta.icon("fa5s.th"), "")
        btn_grid5_view.clicked.connect(lambda: self.set_card(5))
        ttl_wdg_cnt.addWidget(btn_grid5_view)
        btn_grid3_view = QPushButton(qta.icon("fa5s.th-large"), "")
        btn_grid3_view.clicked.connect(lambda: self.set_card(3))
        ttl_wdg_cnt.addWidget(btn_grid3_view)
        btn_list_view = QPushButton(qta.icon("fa5s.th-list"), "")
        btn_list_view.clicked.connect(lambda: self.set_card(1))
        ttl_wdg_cnt.addWidget(btn_list_view)

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
        self.card_container = QWidget()
        scroll_area.setWidget(self.card_container)

        self.card_layout = QGridLayout(self.card_container)
        self.card_layout.setContentsMargins(0, 0, 0, 0)

        self.set_card()

    def set_title_stack(self, var: str):
        if var:
            self.title_stack = var

    def set_card(self, nb_column: int = 5):
        self.clear_card_layout()
        card_ls = [
            {
                "icon_card": None,
                "title": QLabel(self.langManager.get_textTranslate("Network Name")),
                "image_path": None,
                "corps_card": QLineEdit(self.net_obj.networkName),
            },
            {
                "icon_card": None,
                "title": QLabel(self.langManager.get_textTranslate("IPv4")),
                "image_path": None,
                "corps_card": QLineEdit(self.net_obj.ipv4),
            },
            {
                "icon_card": None,
                "title": QLabel(self.langManager.get_textTranslate("Mask")),
                "image_path": None,
                "corps_card": QLineEdit(self.net_obj.mask),
            },
            {
                "icon_card": None,
                "title": QLabel(self.langManager.get_textTranslate("CIDR")),
                "image_path": None,
                "corps_card": QLineEdit(
                    self.net_obj.ipv4_mask_to_cidr(self.net_obj.ipv4, self.net_obj.mask)
                ),
            },
            {
                "icon_card": None,
                "title": QLabel(
                    self.langManager.get_textTranslate("Number of devices")
                ),
                "image_path": None,
                "corps_card": QLineEdit(str(self.net_obj.get_lenght_devices())),
            },
            {
                "icon_card": None,
                "title": QLabel(
                    self.langManager.get_textTranslate("Number of addresses")
                ),
                "image_path": None,
                "corps_card": QLineEdit(str(self.net_obj.get_nb_addr_max())),
            },
            {
                "icon_card": None,
                "title": QLabel(
                    self.langManager.get_textTranslate("Number of usable addresses")
                ),
                "image_path": None,
                "corps_card": QLineEdit(str(self.net_obj.get_nb_addr_usable())),
            },
            {
                "icon_card": None,
                "title": QLabel(
                    self.langManager.get_textTranslate("Number of occupied addresses")
                ),
                "image_path": None,
                "corps_card": QLineEdit(str(self.net_obj.get_nb_addr_occuped())),
            },
            {
                "icon_card": None,
                "title": QLabel(
                    self.langManager.get_textTranslate("Number of free addresses")
                ),
                "image_path": None,
                "corps_card": QLineEdit(str(self.net_obj.get_nb_addr_free())),
            },
        ]
        for i, card in enumerate(card_ls):
            self.card_layout.addWidget(Card(**card), i // nb_column, i % nb_column)

    def clear_card_layout(self):
        while self.card_layout.count():
            child = self.card_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_card_layout(child.layout())


class NetworkDeviceList(NetworkMenu):
    def __init__(self, net_obj: NetworkMap, lang_manager: LanguageApp, parent=None):
        super().__init__(net_obj, lang_manager, parent)
        self.set_title_stack("Device List")

    def set_card(self, nb_column: int = 5):
        self.clear_card_layout()
        nm = nmap.PortScanner()
        nm.scan(hosts=self.net_obj.ipv4_mask_to_cidr(self.net_obj.ipv4, self.net_obj.mask), arguments='-sP')
        device_ls = nm.all_hosts()
        i = 0
        for device in enumerate(self.net_obj.devicesList):
            if isinstance(device, tuple):
                logging.debug(device[0])
                device_ipv4 = device[0]
            else:
                device_ipv4 = device.ipv4

            if device_ipv4 in device_ls:
                card_obj = {
                    "icon_card": device.iconLan,
                    "title": QLabel(device.deviceName),
                    "image_path": None,
                    "corps_card": QLineEdit(f"IP: {device.ipv4}, Vendor: {device.vendor}"),
                }
                self.card_layout.addWidget(Card(**card_obj), i // nb_column, i % nb_column)
                i += 1
            else:
                pass


class CardStackGeneral(QWidget):
    def __init__(self, object_title: str, object_language: LanguageApp, object_view: any, parent=None):
        super().__init__(parent)
        self.stackTitle = object_title
        self.langManager = object_language
        self.objectManager = object_view
        self.card_list = []
        self.initUI()

    def initUI(self):
        # Set the general layout
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Set the top widget
        title_widget = QWidget(self)
        self.layout.addWidget(title_widget, alignment=Qt.AlignTop)

        ttl_wdg_cnt = QHBoxLayout(title_widget)
        # Set the title
        title = QLabel(self.stackTitle)
        title.setFont(QFont("Arial", 12, QFont.Bold))
        ttl_wdg_cnt.addWidget(title, alignment=Qt.AlignCenter)
        ttl_wdg_cnt.addStretch()
        # Set the btn view
        btn_grid5_view = QPushButton(qta.icon("fa5s.th"), "")
        btn_grid5_view.clicked.connect(lambda: self.set_card(5))
        ttl_wdg_cnt.addWidget(btn_grid5_view)
        btn_grid3_view = QPushButton(qta.icon("fa5s.th-large"), "")
        btn_grid3_view.clicked.connect(lambda: self.set_card(3))
        ttl_wdg_cnt.addWidget(btn_grid3_view)
        btn_list_view = QPushButton(qta.icon("fa5s.th-list"), "")
        btn_list_view.clicked.connect(lambda: self.set_card(1))
        ttl_wdg_cnt.addWidget(btn_list_view)

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
        self.card_container = QWidget()
        scroll_area.setWidget(self.card_container)

        self.card_layout = QGridLayout(self.card_container)
        self.card_layout.setContentsMargins(0, 0, 0, 0)

        self.set_card_list()
        self.set_card()

    def set_card_list(self):
        self.card_list = [
            {
                "icon_card": None,
                "title": QLabel(self.stackTitle),
                "image_path": None,
                "corps_card": QLineEdit(self),
            },
        ]

    def set_card(self, nb_column: int = 5):
        self.clear_card_layout()
        for i, card in enumerate(self.card_list):
            self.card_layout.addWidget(Card(**card), i // nb_column, i % nb_column)

    def clear_card_layout(self):
        while self.card_layout.count():
            child = self.card_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_card_layout(child.layout())


class PreferencesGeneral(CardStackGeneral):
    def __init__(self, object_title: str, object_language: LanguageApp, object_view: ConfigurationFile, parent=None):
        super().__init__(object_title, object_language, object_view, parent)
        logging.debug(self.objectManager.data)
        """self.confData = self.objectManager.data['software']
        self.certificatesData = self.objectManager.data['licences']
        self.updateData = self.objectManager.data['repository']"""

    def set_card_list(self):
        self.card_list = [
            {
                "icon_card": None,
                "title": QLabel("Name Software"),
                "image_path": None,
                "corps_card": QLineEdit(self.objectManager.data['system']['name']),
            },
            {
                "icon_card": None,
                "title": QLabel("Description Software"),
                "image_path": None,
                "corps_card": QTextEdit(self.objectManager.data['system']['description']),
            },
            {
                "icon_card": None,
                "title": QLabel("Version Software"),
                "image_path": None,
                "corps_card": QLineEdit(self.objectManager.data['system']['version']),
            },
            {
                "icon_card": None,
                "title": QLabel("Authors Software"),
                "image_path": None,
                "corps_card": QLineEdit(self.objectManager.data['system']['authors']),
            },
            {
                "icon_card": None,
                "title": QLabel("Organisation"),
                "image_path": None,
                "corps_card": QLineEdit(self.objectManager.data['system']['organization']),
            },
            {
                "icon_card": None,
                "title": QLabel("Type Software"),
                "image_path": None,
                "corps_card": QLineEdit(self.objectManager.data['system']['type']),
            },
            {
                "icon_card": None,
                "title": QLabel("Version Date"),
                "image_path": None,
                "corps_card": QLineEdit(str(self.objectManager.data['system']['version_date'])),
            },
            {
                "icon_card": None,
                "title": QLabel("Python Language Version"),
                "image_path": None,
                "corps_card": QLineEdit(str(self.objectManager.data['system']['version_python'])),
            },
            {
                "icon_card": None,
                "title": QLabel("PyQT Version"),
                "image_path": None,
                "corps_card": QLineEdit(str(self.objectManager.data['system']['version_pyqt'])),
            },
            {
                "icon_card": None,
                "title": QLabel("NMAP Version"),
                "image_path": None,
                "corps_card": QLineEdit(str(self.objectManager.data['system']['version_nmap'])),
            },
        ]


class PreferencesLangues(QWidget):
    def __init__(self, object_title: str, object_language: LanguageApp, parent=None):
        super().__init__(parent)
        self.stackTitle = object_title
        self.langManager = object_language
        self.initUI()

    def initUI(self):
        # Set the general layout
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Set the top widget
        title_widget = QWidget(self)
        self.layout.addWidget(title_widget, alignment=Qt.AlignTop)

        ttl_wdg_cnt = QHBoxLayout(title_widget)
        # Set the title
        title = QLabel(self.stackTitle)
        title.setFont(QFont("Arial", 12, QFont.Bold))
        ttl_wdg_cnt.addWidget(title, alignment=Qt.AlignCenter)
        ttl_wdg_cnt.addStretch()
        # Set the language
        lbl_ttl = QLabel(f"{self.langManager.get_textTranslate("Language")}: {self.langManager.language}")

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
        self.card_container = QWidget()
        scroll_area.setWidget(self.card_container)

        self.card_layout = QGridLayout(self.card_container)
        self.card_layout.setContentsMargins(0, 0, 0, 0)


class PreferencesUpdate(CardStackGeneral):
    def __init__(self, object_title: str, object_language: LanguageApp, object_view: ConfigurationFile, parent=None):
        super().__init__(object_title, object_language, object_view, parent)
        """
        self.certificatesData = self.objectManager.data['licences']"""

    def set_card_list(self):
        self.card_list = [
            {
                "icon_card": None,
                "title": QLabel("Repository"),
                "image_path": None,
                "corps_card": QLineEdit(self.objectManager.data['repository']['url']),
            },
            {
                "icon_card": None,
                "title": QLabel("Last Update"),
                "image_path": None,
                "corps_card": QDateEdit(self),
            },
            {
                "icon_card": None,
                "title": QLabel("Update"),
                "image_path": None,
                "corps_card": QLineEdit("Update to v1.2.1"),
            },
        ]
