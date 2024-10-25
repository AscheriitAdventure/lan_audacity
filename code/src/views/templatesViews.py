from typing import Any, Optional, List
from qtpy.QtCore import Qt
from qtpy.QtGui import QIcon, QImage, QPixmap, QFont
from qtpy.QtWidgets import *
import qtawesome as qta
from src.classes.languageApp import LanguageApp
from src.classes.iconsApp import IconsApp


class Card(QWidget):
    def __init__(
            self,
            icon_card: Optional[QIcon] = None,
            title_card: Optional[QWidget] = None,
            img_card: Optional[QImage] = None,
            corps_card: Any = None,
            parent=None
    ):
        super().__init__(parent=parent)
        # Container for the card
        self.mainLayout = QVBoxLayout(self)
        self.setLayout(self.mainLayout)

        # VARIABLES
        self.iconCardLabel = icon_card
        self.titleCardLabel = title_card
        self.imgCardLabel = img_card
        self.bodyCardLabel = corps_card

        # Head Title Layout
        self.titleLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.titleLayout)

        # Set the card UI
        self.set_headTitle()
        self.mainLayout.addStretch(1)
        self.set_imageCard(align=Qt.AlignCenter)
        self.set_bodyCard()
        self.mainLayout.addStretch(1)

        # self.set_cssParameters()

    def set_headTitle(self, icon_card: Optional[QIcon] = None, title: Optional[QWidget] = None):
        
        if icon_card is not None:
            self.iconCardLabel = icon_card
        
        if title is not None:
            self.titleCardLabel = title
        
        if self.iconCardLabel or self.titleCardLabel:
            if self.iconCardLabel:
                icon_label = QLabel()
                icon_label.setPixmap(self.iconCardLabel.pixmap(24, 24))
                self.titleLayout.addWidget(icon_label)
            
            if self.titleCardLabel and isinstance(self.titleCardLabel, QWidget):
                self.titleLayout.addWidget(self.titleCardLabel)
                self.titleLayout.addStretch(1)

            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Sunken)
            self.mainLayout.addWidget(separator)

    def set_imageCard(self, image_path: Optional[QImage] = None, legend: Optional[QWidget] = None, align: Optional[Qt.AlignmentFlag] = None):
        if image_path is not None:
            self.imgCardLabel = image_path
        
        legendImgLabel = legend
        
        if self.imgCardLabel:
            image_label = QLabel()
            image_label.setPixmap(QPixmap.fromImage(self.imgCardLabel))
            if align is not None:
                image_label.setAlignment(align)
            
            self.mainLayout.addWidget(image_label)
            
    def set_bodyCard(self, corps_card: Optional[QWidget] = None):
        if corps_card is not None:
            self.bodyCardLabel = corps_card
            
        if self.bodyCardLabel:
            self.mainLayout.addWidget(self.bodyCardLabel)

    def set_cssParameters(self, css_params: Optional[List[str]] = None):
        """Sets the CSS parameters for the Card widget."""
        if css_params is None:
            css_params = [
                "background-color: #e7ebed;",
                "border: 1px solid black;",
                "border-radius: 4px;"
            ]
        self.setStyleSheet("".join(css_params))


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
            input_obj.setReadOnly(True)
            
        if action_obj is not None:
            input_action_layout.addWidget(action_obj)

        # Ajoutez label_obj et le QHBoxLayout au QFormLayout
        self.layout.addRow(label_obj, input_action_layout)

    def update_input(self):
        """
        Méthode pour mettre à jour le contenu de l'objet QLineEdit.
        Si action_obj existe et activé alors passez de readOnly à False.
        Si input_obj est modifié et validé alors envoyé le signal pour mettre à jour le contenu et passer à readOnly.
        """
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

