from PyQt5.QtWidgets import QTabWidget, QWidget, QGridLayout, QVBoxLayout, QPushButton, QStackedLayout
from PyQt5.QtCore import Qt
from typing import Any

from src.models.language_app import LanguageApp
from src.models.icons_app import IconsApp


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
            ext_obj: Any = None,
            lang_manager: LanguageApp = None,
            icons_manager: IconsApp = None,
            parent=None
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
        self.layout.addWidget(btn_container, 0, 0, Qt.AlignLeft | Qt.AlignTop)

        for btn in self.btnList:
            btn_obj = QPushButton(btn["name"], self)
            btn_obj.setIcon(self.iconsManager.get_icon(btn["icon"]))
            btn_obj.setToolTip(btn["tooltip"])
            btn_obj.clicked.connect(btn["action"])
            btn_container_layout.addWidget(btn_obj)

        self.stackedFields = QStackedLayout()
        self.layout.addLayout(self.stackedFields, 0, 1, Qt.AlignTop)

    def initDisplay(self):
        # Create views for each menu
        self.info_menu = QWidget(self)
        self.stacked_layout.addWidget(self.info_menu)

        self.notif_menu = QWidget(self)
        self.stacked_layout.addWidget(self.notif_menu)

    def setListBtn(self) -> list:
        data = [
            {
                "name": "News",
                "tooltip": "News",
                "icon": "newspaperBtn",
                "action": self.notifications_btn
            },
            {
                "name": "&Preferences",
                "tooltip": "&Preferences",
                "icon": "newspaperBtn",
                "action": self.informations_btn
            }
        ]
        return data

    def notifications_btn(self):
        self.stackedFields.setCurrentWidget(self.notif_menu)

    def informations_btn(self):
        self.stackedFields.setCurrentWidget(self.info_menu)

