# Global imports
from qtpy.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QGridLayout, QFrame, QLineEdit, QHBoxLayout
from qtpy.QtCore import Qt
from qtpy.QtGui import QFont, QImage
import qtawesome as qta
from typing import Optional, Any

# Components imports
from src.components.card.cl_card import Card

# Classes imports
from src.classes.languageApp import LanguageApp
from src.classes.iconsApp import IconsApp

"""
    'DynamicsMosaicsCards' est une mise à jour de 'CardStackGeneral'
"""
class DynamicsMosaicsCards(QWidget):
    def __init__(
        self,
        obj_title: str,
        obj_lang: LanguageApp,
        obj_view: Any,
        obj_icon: Optional[IconsApp] = None,
        obj_img: Optional[QImage] = None,
        parent=None,
    ):
        super().__init__(parent=parent)
        self.stackTitle = obj_title
        self.langManager = obj_lang
        self.objManager = obj_view
        self.iconsManager = obj_icon
        self.imgManager = obj_img       # <--- ?? 
        self.card_list = []

        # init User Interface
        self.initUI()
        # init the card list
        self.setCardList()
        # show the cards
        self.setCard()

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
        # Set the btn view
        btn_grid5_view = QPushButton(qta.icon("fa5s.th"), "")
        btn_grid5_view.clicked.connect(lambda: self.setCard(5))
        ttl_wdg_cnt.addWidget(btn_grid5_view)
        btn_grid3_view = QPushButton(qta.icon("fa5s.th-large"), "")
        btn_grid3_view.clicked.connect(lambda: self.setCard(3))
        ttl_wdg_cnt.addWidget(btn_grid3_view)
        btn_list_view = QPushButton(qta.icon("fa5s.th-list"), "")
        btn_list_view.clicked.connect(lambda: self.setCard(1))
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
        self.card_container = QWidget(self)
        scroll_area.setWidget(self.card_container)

        self.card_layout = QGridLayout(self.card_container)
        self.card_layout.setContentsMargins(0, 0, 0, 0)

    def setCardList(self):
        self.card_list = [
            {
                "top_card": QLabel(self.stackTitle),
                "left_card": None,
                "center_card": QLineEdit(self),
                "right_card": None,
                "bottom_card": None,
            },
        ]
    
    def setCard(self, nb_column: int = 3):
        self.clearCardLayout()
        for i, card in enumerate(self.card_list):
            self.card_layout.addWidget(Card(**card), i // nb_column, i % nb_column)
            self.card_layout.rowStretch(1)

    def clearCardLayout(self):
        while self.card_layout.count():
            child = self.card_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_card_layout(child.layout())
