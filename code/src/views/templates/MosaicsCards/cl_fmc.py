# Global imports
from qtpy.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QGridLayout, QFrame, QHBoxLayout
from qtpy.QtCore import Qt
from qtpy.QtGui import QFont
from typing import Any

# Components imports
from src.components.card.cl_card import Card, CardHeader

# Classes imports
from src.classes.languageApp import LanguageApp
from src.classes.iconsApp import IconsApp


"""
    'FixedMosaicsCards' est une mise à jour de 'DashboardCardTemplate'
"""
class FixedMosaicsCards(QWidget):
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
                "top_card": CardHeader(
                    title_card=QLabel("Hello World!"),
                    icon_card=self.iconsManager.get_icon("defaultIcon")),
                "left_card": None,
                "center_card": QLabel("Welcome!"),
                "right_card": None,
                "bottom_card": QLabel("Bye!")
            }
        ]
    
    def setCardsView(self):
        for settings_card in self.cardList:
            layout_settings = settings_card["layout"]
            card_obj = Card(
                top_card=settings_card["top_card"],
                left_card=settings_card["left_card"],
                center_card=settings_card["center_card"],
                right_card=settings_card["right_card"],
                bottom_card=settings_card["bottom_card"]
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
                