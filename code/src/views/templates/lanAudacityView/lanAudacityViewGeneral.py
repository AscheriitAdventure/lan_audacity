from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *

from typing import Optional, Any

from src.views.templates.WelcomeView.defaultTab import MonitorWD
from src.classes.classesExport import LanguageApp, IconsApp
from src.components.componentsExport import CLWIconText

"""
    Informations:
        'LanAudacityViewGeneral' est une mise à jour de 'GeneralTabsView'
    Commentaires:
        Nous avons optimisé le code :
            - en révisant l'initialisation de la classe et les typographies
            - en ajoutant la classe 'CLWIconText' pour la gestion des boutons
"""

class LanAudacityViewGeneral(QWidget):
    def __init__(
            self, 
            title_panel: str,
            external_object: Optional[Any] = None,
            language_manager: Optional[LanguageApp] = None,
            icons_manager: Optional[IconsApp] = None,
            parent = None
            ) -> None:
        super(LanAudacityViewGeneral, self).__init__(parent)

        self.viewTitle = title_panel
        self.externalObject = external_object
        self.languageManager = language_manager
        self.iconsManager = icons_manager
        self.btnList = self.setListBtn()

        # Layout principal (avec scroll)
        self.main_layout = QVBoxLayout(self)
        self.initScrollArea()

        # Ajout des autres composants
        self.initUI()
        self.initDisplay()

    def initScrollArea(self):
        """
        Encapsule le layout principal dans un QScrollArea
        """
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)

        # Conteneur interne pour le contenu défilable
        self.scroll_content = QWidget()
        self.scroll_area.setWidget(self.scroll_content)

        # Utilisation de QGridLayout existant
        self.layout = QGridLayout(self.scroll_content)
 
    def setListBtn(self) -> list[dict]:
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

    def initUI(self):
        btn_container = CLWIconText(
            toggle_icon=True,
            search_panel=True,
            parent=self
            )
        self.layout.addWidget(btn_container, 0, 0, Qt.AlignLeft | Qt.AlignTop)

        for btn in self.btnList:
            btn_obj = QPushButton(btn["name"])
            if self.iconsManager is not None:
                btn_obj.setIcon(self.iconsManager.get_icon(btn["icon"]))
            btn_obj.setToolTip(btn["tooltip"])
            btn_obj.clicked.connect(btn["action"])
            btn_container.add_btn(btn_obj)
        
        self.stackedFields = QStackedLayout()
        self.layout.addLayout(self.stackedFields, 0, 1, Qt.AlignmentFlag.AlignTop)

    def initDisplay(self):
        # Create views for each menu
        self.info_menu = MonitorWD(
            icons_manager=self.iconsManager,
            language_manager=self.languageManager,
            parent=self
        )
        self.stackedFields.addWidget(self.info_menu)

        self.notif_menu = MonitorWD(
            icons_manager=self.iconsManager,
            language_manager=self.languageManager,
            parent=self
        )
        self.stackedFields.addWidget(self.notif_menu)

    def notifications_btn(self):
        self.stackedFields.setCurrentWidget(self.notif_menu)

    def informations_btn(self):
        self.stackedFields.setCurrentWidget(self.info_menu)
    