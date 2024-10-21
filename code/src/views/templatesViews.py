from typing import Any, Optional
from qtpy.QtCore import Qt, QObject
from qtpy.QtGui import QIcon, QImage, QPixmap, QFont
from qtpy.QtWidgets import *
import qtawesome as qta
from src.classes.languageApp import LanguageApp
from src.classes.iconsApp import IconsApp



class Card(QWidget):
    def __init__(
            self,
            icon_card: Optional[QIcon] = None,
            title_card: Optional[QObject] = None,
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

    def setTitleUI(self, icon_card: Optional[QIcon] = None, title: Optional[QObject] = None):
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
            obj_icon: Optional[IconsApp] = None,
            obj_img: Optional[QImage] = None,
            parent=None
    ):
        super().__init__(parent=parent)
        self.stackTitle = obj_title
        self.langManager = obj_lang
        self.objManager = obj_view
        self.iconsManager = obj_icon
        self.imgManager = obj_img
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
        btn_grid5_view.clicked.connect(lambda: self.setCard(3))
        ttl_wdg_cnt.addWidget(btn_grid5_view)
        btn_grid3_view = QPushButton(qta.icon("fa5s.th-large"), "")
        btn_grid3_view.clicked.connect(lambda: self.setCard(2))
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
                "icon_card": None,
                "title_card": QLabel(self.stackTitle),
                "img_card": None,
                "corps_card": QLineEdit(self),
            },
        ]

    def setCard(self, nb_column: int = 5):
        self.clearCardLayout()
        for i, card in enumerate(self.card_list):
            self.card_layout.addWidget(Card(**card), i // nb_column, i % nb_column)

    def clearCardLayout(self):
        while self.card_layout.count():
            child = self.card_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_card_layout(child.layout())


class RoundedBtn(QPushButton):
    def __init__(self, 
                 icon: Optional[QIcon] = None,
                 text: Optional[str] = None,
                 parent=None):
        super().__init__(parent=parent)

        if icon is not None:
            self.setIcon(icon)

        if text is not None:
            self.setText(text)

        self.setMinimumSize(12, 12)
        self.setMaximumSize(24, 24)


class LineUpdate(QWidget):
    def __init__(self,
                 label_obj: Optional[QLabel] = None,
                 input_obj: Optional[QLineEdit] = None,
                 action_obj: Optional[QPushButton | RoundedBtn] = None,
                 parent=None):
        super().__init__(parent=parent)

        self.layout = QFormLayout(self)
        self.setLayout(self.layout)

        # Créez un QHBoxLayout pour contenir input_obj et action_obj
        input_action_layout = QHBoxLayout()
        if input_obj is not None:
            input_action_layout.addWidget(input_obj)
        if action_obj is not None:
            input_action_layout.addWidget(action_obj)

        # Ajoutez label_obj et le QHBoxLayout au QFormLayout
        self.layout.addRow(label_obj, input_action_layout)

    def update_input(self):
        pass


class TitleWithAction(QWidget):
    def __init__(self, 
                 title: str, 
                 stretch_ttl: int = 1,
                 action: Optional[list[QPushButton]] = None,
                 parent=None):
        super().__init__(parent=parent)

        # Initialisation des composants de l'interface
        self.title_label = QLabel(title)  # Le titre est un QLabel
        self.action_buttons = action if action else []  # Liste des actions sous forme de QPushButton

        # Layout principal
        self.main_layout = QHBoxLayout(self)  # Utilise un layout horizontal

        # Ajoute le titre
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addStretch(stretch_ttl)

        # Ajoute les boutons d'action (s'il y en a)
        if self.action_buttons:
            for button in self.action_buttons:
                self.main_layout.addWidget(button)

        # Aligne le layout à gauche
        self.setLayout(self.main_layout)