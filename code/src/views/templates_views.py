from qtpy.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QGridLayout, QFrame, QLineEdit
from qtpy.QtGui import QFont, QIcon, QImage, QPixmap
from qtpy.QtCore import Qt
import qtawesome as qta
from src.models.language_app import LanguageApp
from typing import Any, Optional


class Card(QWidget):
    def __init__(
            self,
            icon_card: Optional[QIcon] = None,
            title_card: Optional[QLabel] = None,
            img_card: Optional[QImage] = None,
            corps_card: Any = None,
            parent=None
    ):
        super().__init__(parent=parent)
        self.layout = QGridLayout(self)  # Initialisation de l'attribut layout
        self.setLayout(self.layout)

        if icon_card or title_card:
            self.setTitleUI(icon_card, title_card)

        if img_card:
            self.setImageUI(img_card)

        if corps_card:
            self.setBodyUI(corps_card)

    def setTitleUI(self, icon_card: Optional[QIcon] = None, title: Optional[QLabel] = None):
        """Sets the title UI with an optional icon and title label."""
        hbar_title = QHBoxLayout()
        if icon_card:
            icon_label = QLabel()
            icon_label.setPixmap(icon_card.pixmap(24, 24))
            hbar_title.addWidget(icon_label)

        if title:
            hbar_title.addWidget(title)

        hbar_title.addStretch(1)
        hbar_cnt = QWidget()
        hbar_cnt.setLayout(hbar_title)
        self.layout.addWidget(hbar_cnt, 0, 0, 1, 2, Qt.AlignTop)

        # set the separator
        sep = QFrame(self)
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(sep)

    def setImageUI(self, image_path: QImage):
        """Sets the image UI with the provided QImage."""
        image_label = QLabel()
        image_label.setPixmap(QPixmap.fromImage(image_path))
        image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(image_label, 1, 0, 1, 2, Qt.AlignHCenter)

    def setBodyUI(self, corps_card: QWidget):
        """Sets the body UI with the provided QWidget."""
        self.layout.addWidget(corps_card, 2, 0, 1, 2)


class CardStackGeneral(QWidget):
    def __init__(
            self,
            obj_title: str,
            obj_lang: LanguageApp,
            obj_view: Any,
            parent=None
    ):
        super().__init__(parent=parent)
        self.stackTitle = obj_title
        self.langManager = obj_lang
        self.objManager = obj_view
        self.card_list = []

        # init User Interface
        self.initUI()
        # init the card list
        self.setCardList()
        # show the cards
        self.setCard()

    def initUI(self):
        # Set the general layout
        qlayout = QVBoxLayout(self)
        qlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(qlayout)

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
        self.card_container = QWidget(self)
        scroll_area.setWidget(self.card_container)

        self.card_layout = QGridLayout(self.card_container)
        self.card_layout.setContentsMargins(0, 0, 0, 0)

    def setCardList(self):
        self.card_list = [
            {
                "icon_card": None,
                "title": QLabel(self.stackTitle),
                "image_path": None,
                "corps_card": QLineEdit(self),
            },
        ]

    def setCard(self, nb_column: int = 5):
        self.clear_card_layout()
        for i, card in enumerate(self.card_list):
            self.card_layout.addWidget(Card(**card), i // nb_column, i % nb_column)

    def clearCardLayout(self):
        while self.card_layout.count():
            child = self.card_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_card_layout(child.layout())
