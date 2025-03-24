# Global imports
from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *
from typing import Any, Optional
import logging
import inspect
import os
import json

import qtawesome as qta
from dev.project.src.classes.cl_extented import IconApp as IconsApp
# Description: Default variables for card component.
VAR_CardCSS: dict = {
    "global": {
        "background": {
            "color": "Gainsboro",
            "image": None,
        },
        "border": {
            "width": 1,
            "color": "Gainsboro",
            "radius": 10,
            "style": "solid",
        },
    },
    "top": {
        "border": {
            "bottom": True,
            "radius": 0,
            "width": 1,
            "color": "Gray",
            "style": "solid",
        },
    },
    "left": {},
    "center": {},
    "right": {},
    "bottom": {
        "border": {
            "top": True,
            "radius": 0,
            "width": 1,
            "color": "Gray",
            "style": "solid",
        },
    }
}

# Card Components

class Card(QWidget):
    def __init__(
        self,
        top_card: Optional[QWidget] = None,  # Optional[CardHeader],
        left_card: Optional[QWidget] = None,
        center_card: Optional[QWidget] = None,
        right_card: Optional[QWidget] = None,
        bottom_card: Optional[QWidget] = None,  # Optional[CardFooter],
        css_params: Optional[dict] = VAR_CardCSS,
        logger: Optional[bool] = False,
        parent=None,
    ):
        super(Card, self).__init__(parent)
        if logger:
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.DEBUG)

        # Une carte utilise un layout de type Grid
        self.card_layout = QGridLayout()
        self.setLayout(self.card_layout)

        self.activeSections: list = ["global"]

        self.paintProperties: dict = {}
        self.cssParameters(css_params)

        self.topCard: Optional[QWidget] = None
        self.leftCard: Optional[QWidget] = None
        self.centerCard: Optional[QWidget] = None
        self.rightCard: Optional[QWidget] = None
        self.bottomCard: Optional[QWidget] = None

        self.set_ui(top_card, left_card, center_card, right_card, bottom_card)

    def set_ui(
        self,
        top_card: Optional[QWidget],
        left_card: Optional[QWidget],
        center_card: Optional[QWidget],
        right_card: Optional[QWidget],
        bottom_card: Optional[QWidget],
    ):
        var_rowStart = 0
        var_colStart = 0
        var_colSpan = 3

        if top_card is not None:
            # Il occupera la première ligne de la grille
            self.topCard = top_card
            self.card_layout.addWidget(
                self.topCard, var_rowStart, var_colStart, 1, 3, Qt.AlignmentFlag.AlignLeft)
            var_rowStart = var_rowStart + 1

        if bottom_card is not None:
            # Il occupera la dernière ligne de la grille
            self.bottomCard = bottom_card
            self.card_layout.addWidget(self.bottomCard, 2, 0, 1, 3)

        if left_card is not None:
            # Il occupera la première colonne de la grille
            self.leftCard = left_card
            self.card_layout.addWidget(
                self.leftCard, var_rowStart, var_colStart, 1, 1)
            var_colStart = var_colStart + 1
            var_colSpan = var_colSpan - 1

        if right_card is not None:
            # Il occupera la dernière colonne de la grille
            self.rightCard = right_card
            self.card_layout.addWidget(self.rightCard, var_rowStart, 2, 1, 1)
            var_colSpan = var_colSpan - 1

        if center_card is not None:
            # center_card occupera tout l'espace restant
            self.centerCard = center_card
            self.card_layout.addWidget(
                self.centerCard, var_rowStart, var_colStart, 1, var_colSpan
            )

    def cssParameters(self, css_params: Optional[dict] = None):
        """Sets the CSS parameters for the CardUI widget."""
        self.paintProperties = css_params

    def paintSection(self, painter: QPainter, rect: QRectF, styles: dict):
        """Dessine une section de la carte avec les styles spécifiés."""
        background_obj = styles.get("background", {})
        border_obj = styles.get("border", {})
        shadow_obj = styles.get("shadow", {})

        borderRadius = border_obj["radius"] if border_obj.get("radius") else 0

        # Dessiner l'arrière-plan
        if background_obj.get("color"):
            backgroudColor = QColor(background_obj["color"])
            painter.setBrush(QBrush(backgroudColor))
            path = QPainterPath()
            path.addRoundedRect(rect, borderRadius, borderRadius)
            painter.fillPath(path, backgroudColor)

        if background_obj.get("image"):
            backgroundgImage = background_obj["image"]
            if isinstance(backgroundgImage, QPixmap):
                painter.drawPixmap(rect, backgroundgImage)
            elif isinstance(backgroundgImage, QImage):
                painter.drawImage(rect, backgroundgImage)
            elif isinstance(backgroundgImage, str):
                # Load image from file
                image = QImage(backgroundgImage)
                if image.isNull():
                    self.logger.warning(f"Failed to load image from file: {backgroundgImage}")
                else:
                    painter.drawImage(rect, image)
            else:
                self.logger.warning(f"Invalid background image type: {type(backgroundgImage)}")

        # Dessiner la bordure
        borderWidth = border_obj["width"] if border_obj.get("width") else 0

        if border_obj.get("color"):
            if isinstance(border_obj["color"], QColor):
                borderColor = border_obj["color"]
            elif isinstance(border_obj["color"], tuple):
                borderColor = QColor(*border_obj["color"])
            elif isinstance(border_obj["color"], str):
                borderColor = QColor()
                borderColor.setNamedColor(border_obj["color"])
            else:
                borderColor = QColor()
                borderColor.setNamedColor("Black")

        if border_obj.get("style") == "solid":
            borderStyle = Qt.PenStyle.SolidLine
        elif border_obj.get("style") == "dash":
            borderStyle = Qt.PenStyle.DashLine
        elif border_obj.get("style") == "dot":
            borderStyle = Qt.PenStyle.DotLine
        else:
            borderStyle = Qt.PenStyle.NoPen

        # Apply shadow effect if specified
        # shadow_blur = self.paintProperties["shadow_blur"] or 0

        # Si une bordure est spécifiée, dessiner UNIQUEMENT les bords spécifiés
        if borderWidth > 0:
            painter.setPen(QPen(borderColor, borderWidth, borderStyle))
            if border_obj.get("top"):
                painter.drawLine(rect.topLeft(), rect.topRight())
            elif border_obj.get("bottom"):
                painter.drawLine(rect.bottomLeft(), rect.bottomRight())
            elif border_obj.get("left"):
                painter.drawLine(rect.topLeft(), rect.bottomLeft())
            elif border_obj.get("right"):
                painter.drawLine(rect.topRight(), rect.bottomRight())
            else:
                pen = QPen(borderColor, borderWidth, borderStyle)
                painter.setPen(pen)
                if borderRadius:
                    painter.drawRoundedRect(rect, borderRadius, borderRadius)
                else:
                    painter.drawRect(rect)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        sections = {"global": QRectF(self.rect())}

        if self.topCard:
            sections["top"] = self.getTruePosition(self.topCard, "Top")
        if self.leftCard:
            sections["left"] = self.getTruePosition(self.leftCard)
        if self.centerCard:
            sections["center"] = self.getTruePosition(self.centerCard)
        if self.rightCard:
            sections["right"] = self.getTruePosition(self.rightCard)
        if self.bottomCard:
            sections["bottom"] = self.getTruePosition(self.bottomCard, "Bottom")
            
        # Peindre uniquement les sections actives
        for section in sections:
            rect = sections[section]
            # logging.info(f"{section}: {rect}")
            styles = self.paintProperties.get(section, {})
            if styles != {}:
                self.paintSection(painter, rect, styles)

        painter.end()

    def setBorderStyle(
            self,
            section: str,
            color: Optional[QColor] = None,
            width: Optional[int] = None,
            radius: Optional[int] = None,
            style: Optional[str] = None
    ):
        """
            Modifie le style de bordure de la section spécifiée.
            Args:
                section (str): les différentes sections sont: ["global", "top_card", "left_card", "center_card", "right_card", "bottom_card"]
                color (Optional[QColor], optional): _description_. Defaults to None.
                width (Optional[int], optional): _description_. Defaults to None.
                radius (Optional[int], optional): _description_. Defaults to None.
                style (Optional[str], optional): _description_. Defaults to None.
        """
        if color:
            self.paintProperties[section]["border"]["color"] = QColor(color)
        if width is not None:
            self.paintProperties[section]["border"]["width"] = width
        if radius is not None:
            self.paintProperties[section]["border"]["radius"] = radius
        if style:
            self.paintProperties[section]["border"]["style"] = style

        self.update()

    def setBackgroundStyle(self,section: str, color: Optional[QColor] = None, image: Optional[QImage] = None):
        """_summary_

        Args:
            section (str): les différentes sections sont: ["global", "top_card", "left_card", "center_card", "right_card", "bottom_card"]
            color (Optional[QColor], optional): _description_. Defaults to None.
            image (Optional[QImage], optional): _description_. Defaults to None.
        """
        if color:
            self.paintProperties[section]["background"]["color"] = QColor(color)
        if image:
            self.paintProperties[section]["background"]["image"] = QImage(image)
        self.update()

    def getTruePosition(self, widget: QWidget, top_bottom:Optional[str] = None) -> QRectF:
        """Récupère la position absolue du widget dans la fenêtre."""
        # Obtenez le rectangle de l'objet (widget)
        var_qrect_obj = widget.rect()
        width = var_qrect_obj.width()
        height = var_qrect_obj.height()
    
        # Récupérez la position de l'objet dans la mise en page
        var_position_obj = widget.pos()
    
        # Calculez les coordonnées corrigées pour l'objet
        # En tenant compte des marges et des positions relatives
        x = var_position_obj.x()
        y = var_position_obj.y()

        left_margin, top_margin, right_margin, bottom_margin = self.card_layout.getContentsMargins()
        topbot_margin = bottom_margin*0.75+top_margin*0.75
        topbot_width = self.rect().width()
        # Obtenez les marges de la disposition
        if top_bottom == "Bottom":
            return QRectF(x-left_margin, y-0.25*top_margin, topbot_width, height+topbot_margin)
        elif top_bottom == "Top":
            return QRectF(x-left_margin, y-top_margin, topbot_width, height+topbot_margin)
        else:
            return QRectF(x, y, width, height)
    

class CardHeader(QWidget):
    def __init__(
        self,
        icon_card: Optional[QIcon] = None,
        title_card: Optional[QWidget] = None,
        logger: Optional[bool] = False,
        parent=None,
    ):
        super(CardHeader, self).__init__(parent)
        if logger:
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.DEBUG)

        self.headerCard_layout = QHBoxLayout()
        self.setLayout(self.headerCard_layout)

        self.setTitleUI(icon_card, title_card)

        self.cssParameters()

    def setTitleUI(
        self, icon_card: Optional[QIcon] = None, title: Optional[QWidget] = None
    ):
        """Sets the title UI with an optional icon and title label."""
        if icon_card or title:
            if icon_card:
                icon_label = QLabel()
                icon_label.setPixmap(icon_card.pixmap(24, 24))
                self.headerCard_layout.addWidget(icon_label)

            if title and isinstance(title, QWidget):
                self.headerCard_layout.addWidget(title)
                self.headerCard_layout.addStretch(1)

    def cssParameters(self):
        """Sets the CSS parameters for the CardHeader widget."""
        pass


class CardFooter(QWidget):
    def __init__(
        self,
        content_card: Optional[QWidget] = None,
        logger: Optional[bool] = False,
        parent=None,
    ):
        super(CardFooter, self).__init__(parent)
        if logger:
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.DEBUG)

        self.headerCard_layout = QHBoxLayout()
        self.setLayout(self.headerCard_layout)

        # set the separator
        sep = QFrame(self)
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        self.headerCard_layout.addWidget(sep)

        if content_card is not None:
            self.headerCard_layout.addWidget(content_card)


class CardImage(QWidget):
    def __init__(
        self,
        image_card: Optional[list[QImage] | QImage] = None,
        logger: Optional[bool] = False,
        parent=None,
    ):
        super(CardImage, self).__init__(parent)
        if logger:
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.DEBUG)

        self.imageCard_layout = QHBoxLayout()
        self.setLayout(self.imageCard_layout)

        if image_card and isinstance(image_card, list):
            self.logger.warning("En cours de création")
            self.setListImageUI(image_card)

        elif image_card and isinstance(image_card, QImage):
            self.setImageUI(image_card)

        else:
            self.logger.error("Invalid image type or No Image.")

    def setImageUI(self, image_card: QImage):
        """Sets the image UI with an image."""
        self.imageCard_layout.addStretch(1)
        image_label = QLabel()
        image_label.setPixmap(QPixmap.fromImage(image_card))
        self.imageCard_layout.addWidget(image_label)
        self.imageCard_layout.addStretch(1)

    def setListImageUI(self, image_card: list[QImage]):
        """Sets the image UI with a list of images."""
        pass

# Templates Ext
class LineUpdate(QWidget):
    # Signal émis lorsque le contenu est modifié et validé
    contentChanged = Signal(str)

    def __init__(
        self,
        label_obj: Optional[QLabel] = None,
        input_obj: Optional[QLineEdit] = None,
        action_obj: Optional[QPushButton] = None,
        parent=None,
    ):
        super().__init__(parent=parent)

        self.input_obj = input_obj
        self.action_obj = action_obj

        self.layout = QFormLayout(self)
        self.setLayout(self.layout)

        # Créez un QHBoxLayout pour contenir input_obj et action_obj
        input_action_layout = QHBoxLayout()
        if input_obj is not None:
            input_action_layout.addWidget(input_obj)
            input_obj.setReadOnly(True)
            # Connecter le signal returnPressed à la validation
            input_obj.returnPressed.connect(self.validate_input)

        if action_obj is not None:
            input_action_layout.addWidget(action_obj)
            # Connecter le bouton d'action au toggle de l'édition
            action_obj.clicked.connect(self.update_input)

        # Ajoutez label_obj et le QHBoxLayout au QFormLayout
        self.layout.addRow(label_obj, input_action_layout)

    def update_input(self):
        """
        Méthode pour mettre à jour le contenu de l'objet QLineEdit.
        Si action_obj existe et activé alors passez de readOnly à False.
        Si input_obj est modifié et validé alors envoyé le signal pour mettre à jour le contenu et passer à readOnly.
        """
        if self.input_obj is not None:
            # Basculer l'état readOnly
            self.input_obj.setReadOnly(False)
            # Donner le focus au QLineEdit
            self.input_obj.setFocus()
            # Changer le texte du bouton si c'est un QPushButton
            if isinstance(self.action_obj, QPushButton):
                # self.action_obj.setText("Valider")
                # Déconnecter le signal clicked pour éviter les doubles connexions
                try:
                    self.action_obj.clicked.disconnect(self.update_input)
                except:
                    pass
                # Connecter le nouveau signal pour la validation
                self.action_obj.clicked.connect(self.validate_input)

    def validate_input(self):
        """
        Valide le contenu modifié et remet le QLineEdit en mode lecture seule
        """
        if self.input_obj is not None:
            # Émettre le signal avec le nouveau contenu
            self.contentChanged.emit(self.input_obj.text())
            # Remettre en mode lecture seule
            self.input_obj.setReadOnly(True)
            # Remettre le bouton dans son état initial si c'est un QPushButton
            if isinstance(self.action_obj, QPushButton):
                # self.action_obj.setText("Modifier")
                # Déconnecter le signal de validation
                try:
                    self.action_obj.clicked.disconnect(self.validate_input)
                except:
                    pass
                # Reconnecter le signal d'édition
                self.action_obj.clicked.connect(self.update_input)


class TitleWithAction(QWidget):
    def __init__(
        self,
        title: str,
        stretch_ttl: int = 1,
        action: Optional[list[QPushButton]] = None,
        parent=None,
    ):
        super().__init__(parent=parent)

        # Initialisation des composants de l'interface
        self.title_label = QLabel(title)  # Le titre est un QLabel
        self.action_buttons = (
            action if action else []
        )  # Liste des actions sous forme de QPushButton

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
        
# Mosaïcs Card
class FixedMosaicsCards(QWidget):
    """
        'FixedMosaicsCards' est une mise à jour de 'DashboardCardTemplate'
    """
    def __init__(self,
                 obj_title: str,
                 obj_view: Any,
                 obj_icon: IconsApp,
                 parent=None):
        super().__init__(parent)
        # Préparation à l'environnement
        self.cardList: list = []
        # Préparation aux Data
        self.stackTitle = obj_title
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
                self.clearCardLayout(child.layout())

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
  

class DynamicsMosaicsCards(QWidget):
    """
        'DynamicsMosaicsCards' est une mise à jour de 'CardStackGeneral'
    """
    def __init__(
        self,
        obj_title: str,
        obj_view: Any,
        obj_icon: Optional[IconsApp] = None,
        obj_img: Optional[QImage] = None,
        parent=None,
    ):
        super().__init__(parent=parent)
        self.stackTitle = obj_title
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
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        ttl_wdg_cnt.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
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
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFrameShadow(QFrame.Shadow.Sunken)
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
                self.clearCardLayout(child.layout())

# Extensions Mosaics Cards
class PaletteIconSettingsDMC(DynamicsMosaicsCards):
    """
        Nom complet: Palette Icon Settings Dynamics Mosaics Cards
        Description: Cette classe est une mise à jour de 'PaletteIconSettings(CardStackGeneral)'
        Nouveau nom: PaletteIconSettingsDMC
    """
    def __init__(
        self,
        obj_title: str,
        obj_view: IconsApp,
        obj_icon: Optional[IconsApp] = None,
        obj_img: Optional[QImage] = None,
        parent=None,
    ):
        super().__init__(obj_title, obj_view, obj_icon, obj_img, parent)

    def setCardList(self):
        self.card_list = []
        for icon in self.objManager.data_manager:
            # Titre de la carte
            cardTtl = QLabel(icon["name"])
            # Image de la carte
            cardImg = self.objManager.get_icon(icon["name"]).pixmap(64, 64).toImage()
            # Corps de la carte
            if icon.get("options") is not None:
                cardOpt = QWidget()
                cardOptLayout = QVBoxLayout()
                cardOpt.setLayout(cardOptLayout)

                len_options = len(icon["options"])
                data_options = icon["options"]

                for i, option in enumerate(data_options):
                    keys = option.keys()
                    if len_options > 1:
                        cardOptLayout.addWidget(
                            QLabel(f"{icon["platform_and_name"][i]} :")
                        )
                    for key in keys:
                        btn_options = QPushButton(self)
                        btn_options.setIcon(qta.icon("mdi6.pencil"))
                        if len_options > 1:
                            ttl_label = QLabel(f"    {key} :")
                        else:
                            ttl_label = QLabel(f"{key} :")

                        options_lineUpdate = LineUpdate(
                            label_obj=ttl_label,
                            input_obj=QLineEdit(str(option[key])),
                            action_obj=btn_options,
                        )
                        cardOptLayout.addWidget(options_lineUpdate)

            else:
                cardOpt = QLabel("No options")

            icon_dict: dict = {
                "top_card": CardHeader(
                    icon_card=qta.icon("mdi6.palette-advanced"),
                    title_card=cardTtl),
                "center_card": CardImage(image_card=cardImg),
                "right_card": cardOpt
            }

            self.card_list.append(icon_dict)
        logging.info(f"Card list: {len(self.card_list)} item(s)")

"""
    Commentaires:
        Bon travail, la classe est bien structurée et les noms des méthodes et des variables sont explicites.
        Toutefois la liste qui montre les paramètres des icônes est moche.
        Je vous propose de la rendre plus agréable en utilisant le principe d'accordéon du web.
    Consignes:
        - Nom complet: Palette Icon Settings Dynamics Mosaics Cards Accordion
        - Description: Cette classe est une mise à jour de 'PaletteIconSettingsDMC'
        - Nouveau nom: PISDMCAccordion
    Etape 1:
        - Implémentez la méthode 'setCardListAccordion' qui affiche les paramètres des icônes dans un accordéon.
    Aide:
    Une première recherche est à disposition en commentaire.
"""

class PISDMCAccordion(DynamicsMosaicsCards):
    def __init__(
        self,
        obj_title: str,
        obj_view: ConfigurationFile,
        obj_icon: Optional[IconsApp] = None,
        obj_img: Optional[QImage] = None,
        parent=None,
    ):
        super().__init__(obj_title, obj_view, obj_icon, obj_img, parent)

    def setCardList(self):
        self.card_list = []
        for icon in self.objManager.data:
            # Titre de la carte
            cardHeader = CardHeader(
                icon_card=qta.icon("mdi6.palette-advanced"),
                title_card=QLabel(icon["name"])
            )
            # Image de la carte
            cardImage = CardImage(
                image_card=self.iconsManager.get_icon(icon["name"]).pixmap(64, 64).toImage()
            )
            # Commentaires de la carte
            if icon.get("options") is not None:
                rightCard = QWidget()
                cardOptLayout = QVBoxLayout(rightCard)
                
                accordion = AccordionWidget()
                cardOptLayout.addWidget(accordion)

                len_options = len(icon["options"])
                data_options = icon["options"]

                for i, option in enumerate(data_options):
                    keys = option.keys()
                    content_obj = QWidget()
                    content_layout = QVBoxLayout(content_obj)

                    for key in keys:
                        btn_options = QPushButton(self)
                        btn_options.setIcon(qta.icon("mdi6.pencil"))
                        ttl_label = QLabel(f"{key} :")
                        options_lineUpdate = LineUpdate(
                            label_obj=ttl_label,
                            input_obj=QLineEdit(str(option[key])),
                            action_obj=btn_options,
                        )
                        content_layout.addWidget(options_lineUpdate)

                    accordion.add_section(f"{icon['platform_and_name'][i]}", content_obj)

            else:
                rightCard = QLabel("No options")

            # Dictionnaire
            icon_dict: dict = {
                "top_card": cardHeader,
                "center_card": cardImage,
                "right_card": rightCard
            }
            self.card_list.append(icon_dict)
        logging.info(f"Card list: {len(self.card_list)} item(s)")


class NetworkGeneralDMC(DynamicsMosaicsCards):
    """
        Nom complet: Nertwork General Dynamics Mosaics Cards
        Description: Cette classe est une mise à jour de 'NetworkGeneral(CardStackGeneral)'
        Nouveau nom: NetworkGeneralDMC
    """
    def __init__(
        self, obj_title: str, obj_view: Network, parent=None
    ):
        super().__init__(obj_title, obj_view, parent)

    def setCardList(self):
        btn_edit = QPushButton(self)
        btn_edit.setIcon(qta.icon("mdi6.pencil"))
        self.card_list = [
            {
                "top_card": QLabel("IPv4 Address"),
                "center_card": LineUpdate(
                    input_obj=QLineEdit(self.objManager.ipv4),
                    action_obj=btn_edit
                )
            },
            {
                "top_card": QLabel("IPv4 Mask"),
                "center_card": LineUpdate(
                    input_obj=QLineEdit(self.objManager.maskIpv4),
                    action_obj=btn_edit
                )
            },
            {
                "top_card": QLabel("IPv6 Address"),
                "center_card": LineUpdate(
                    input_obj=QLineEdit(self.objManager.ipv6),
                    action_obj=btn_edit
                )
            },
            {
                "top_card": QLabel("Gateway"),
                "center_card": LineUpdate(
                    input_obj=QLineEdit(self.objManager.gateway),
                    action_obj=btn_edit
                )
            },
            {
                "top_card": QLabel("Domain Name"),
                "center_card": LineUpdate(
                    input_obj=QLineEdit(self.objManager.dns),
                    action_obj=btn_edit
                )
            },
            {
                "top_card": QLabel("Creation Date"),
                "center_card": QLineEdit(
                    self.objManager.clockManager.conv_unix_to_datetime(
                        self.objManager.clockManager.clockCreated
                    )
                )
            },
            {
                "top_card": QLabel("Update Date"),
                "center_card": QLineEdit(
                    self.objManager.clockManager.conv_unix_to_datetime(
                        self.objManager.clockManager.get_clock_last()
                    )
                )
            },
        ]


class PreferencesGeneralDMC(DynamicsMosaicsCards):
    """
        Nom complet: Preferences General Dynamics Mosaics Cards
        Description: Cette classe est une mise à jour de 'PreferencesGeneral(CardStackGeneral)'
        Nouveau nom: PreferencesGeneralDMC
    """
    def __init__(
        self,
        obj_title: str,
        obj_view: ConfigurationFile,
        parent=None,
    ):
        super().__init__(
            obj_title=obj_title, obj_view=obj_view, parent=parent
        )

    def setCardList(self):
        self.card_list = [
            {
                "top_card": QLabel("Name Software"),
                "center_card": QLineEdit(self.objManager.data["system"]["name"])
            },
            {
                "top_card": QLabel("Description Software"),
                "center_card": QTextEdit(self.objManager.data["system"]["description"])
            },
            {
                "top_card": QLabel("Version Software"),
                "center_card": QLineEdit(self.objManager.data["system"]["version"])
            },
            {
                "top_card": QLabel("Authors Software"),
                "center_card": QLineEdit(self.objManager.data["system"]["authors"])
            },
            {
                "top_card": QLabel("Organization"),
                "center_card": QLineEdit(self.objManager.data["system"]["organization"])
            },
            {
                "top_card": QLabel("Type Software"),
                "center_card": QLineEdit(self.objManager.data["system"]["type"])
            },
            {
                "top_card": QLabel("Version Date"),
                "center_card": QLineEdit(str(self.objManager.data["system"]["version_date"]))
            },
            {
                "top_card": QLabel("Python Language Version"),
                "center_card": QLineEdit(str(self.objManager.data["system"]["version_python"]))
            },
            {
                "top_card": QLabel("PyQT Version"),
                "center_card": QLineEdit(str(self.objManager.data["system"]["version_pyqt"]))
            },
            {
                "top_card": QLabel("NMAP Version"),
                "center_card": QLineEdit(str(self.objManager.data["system"]["version_nmap"]))
            },
        ]


class DevicesDMC(DynamicsMosaicsCards):
    def __init__(
        self,
        obj_title: str,
        obj_view: Network,
        obj_icon: IconsApp,
        parent=None,
    ):
        super().__init__(obj_title, obj_view, parent)

    def setCardList(self):
        self.card_list = []
        img_default = QImage(
            "C:\\Users\\g.tronche\\Documents\\GitHub\\affinity\\svg\\circle\\gray\\c_client.svg"
        )

        if self.objManager.devicesList is not []:
            for device in self.objManager.devicesList:
                var_path = os.path.join(
                    os.path.dirname(os.path.dirname(self.objManager.absPath)),
                    "desktop",
                    f"{device}.json",
                )
                if os.path.exists(var_path):
                    with open(var_path, "r") as f:
                        device_data = json.load(f)
                        ipv4 = (
                            device_data.get("ipv4", "value unknown") or "value unknown"
                        )
                        name = (
                            device_data.get("name", "value unknown") or "value unknown"
                        )
                        self.card_list.append(
                            {
                                "top_card": QLabel(f"{name}({ipv4})"),
                                "left_card": CardImage(img_default.scaled(50, 50, Qt.KeepAspectRatio)),
                                "center_card": QLabel(
                                    f"Mac Address: {device_data.get('mac', 'value unknown') or 'value unknown'}"
                                ),
                            }
                        )
        else:
            self.card_list.append(
                {
                    "center_card": QLabel("No device found")
                }
            )


class UpdatesNewsDMC(DynamicsMosaicsCards):
    """
        Nom complet: Updates News Dynamics Mosaics Cards
        Description: Cette classe affiche un journal des mises à jour
        Nouveau nom: UpdatesNewsDMC
    """
    def __init__(self, obj_title: str, obj_view: ConfigurationFile, parent=None):
        super().__init__(obj_title=obj_title, obj_view=obj_view, parent=parent)
    
    def generateCard(self):
        data = self.objManager.data["news_update"]
        logging.debug(f"Lenght of data: {len(data)}")
        for obj in data:
            leftCard = None
            rightCard = None
            centerCard = None
            bottomCard = None
            logging.debug(f"Object: {obj}")
            topCard = QLabel(f"Version {obj['version']} - Date {obj['date']}")
            if obj.get("sources"):
                # Créer un lien qui permet d'ouvrir un onglet qui affiche le contenu du fichier en read-only
                logging.debug(f"Sources: {obj['sources']}")
                centerCard = QLabel(f"{obj['sources']}")

            if obj.get("authors"):
                logging.debug(f"Authors: {obj['authors']}")
                bottomCard = QLabel(f"{obj['authors']}")
            
            if obj.get("description"):
                logging.debug(f"Description: {obj['description']}")
                if centerCard is None:
                    centerCard = QLabel(f"{obj['description']}")
                else:
                    rightCard = QLabel(f"{obj['description']}")

            self.card_list.append(
                {
                    "top_card": topCard,
                    "left_card": leftCard,
                    "center_card": centerCard, # <--- Ajouter le texte de la description
                    "right_card": rightCard,
                    "bottom_card": bottomCard # <--- Ajouter les auteurs
                }
            )
    
    def setCardList(self):
        self.card_list = []
        self.generateCard()
   
""" 
    Informations:
        Ce fichier a pour but de présenter une nouvelle présentation de "Preferences/Dashboard".
        Il doit afficher ces cartes:
            - Un rapide aperçu des informations du logiciel
            - Choix des langues
            - Opion de mise à jour
            - Un Objet qui affichera (si ce n'est pas un fichier) les dernières fonctionnalités ajoutées sinon un lien.
    Outils:
        - QtPy(PyQt6)
        - logging
        - typing
        - nom complet: Preferences Dashboard Fixed Mosaics Cards
        - nom classe: PDashboardFMC
"""

class PDashboardFMC(FixedMosaicsCards):
    def __init__(
        self, 
        obj_title: str,
        obj_view: ConfigurationFile, 
        obj_icon: IconsApp, 
        parent=None):
        super().__init__(obj_title, obj_view, obj_icon, parent)
    
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
                    icon_card=self.iconsManager.get_icon("lan_audacity"),
                    title_card=QLabel("Software Information")),
                "left_card": None,
                "right_card": None,
                "bottom_card": None,
                "center_card": QLabel("Manage your software information here.") # <--- A Impléménter
            },
            {
                "layout": {
                    "row": 0,
                    "column": 1,
                    "rowSpan": None,
                    "columnSpan": None,
                    "alignement": None
                },
                "top_card": CardHeader(
                    icon_card=self.iconsManager.get_icon("languageAction"),
                    title_card=QLabel("Language Choice")),
                "left_card": None,
                "right_card": None,
                "bottom_card": None,
                "center_card": QLabel("Manage your Language here.") # <--- A Impléménter
            },
            {
                "layout": {
                    "row": 1,
                    "column": 0,
                    "rowSpan": None,
                    "columnSpan": None,
                    "alignement": None
                },
                "top_card": CardHeader(
                    icon_card=self.iconsManager.get_icon("updateAction"),
                    title_card=QLabel("Update Option")),
                    "left_card": None,
                "right_card": None,
                "bottom_card": None,
                "center_card": QLabel("Manage your update option here.") # <--- A Impléménter
            },
            {
                "layout": {
                    "row": 1,
                    "column": 1,
                    "rowSpan": None,
                    "columnSpan": None,
                    "alignement": None
                },
                "top_card": CardHeader(
                    icon_card=self.iconsManager.get_icon("newsUpgrade"),
                    title_card=QLabel("Feature Information")),
                "left_card": None,
                "right_card": None,
                "bottom_card": None,
                "center_card": QLabel("Manage your feature information here.") # <--- A Impléménter
            }
        ]


class LanDashboardFMC(FixedMosaicsCards):
    """
        Nom complet: Lan Dashboard Fixed Mosaics Cards
        Description: Cette classe est une mise à jour de 'LanDashboard(DashboardCardTemplate)'
        Nouveau nom: LanDashboardFMC
    """
    def __init__(self, obj_title: str, obj_view: Network, obj_icon: IconsApp, parent=None):
        """
        Initialise l'interface de tableau de bord LAN avec les cartes et les composants réseau.

        :param obj_title: Titre de l'objet.
        :param obj_lang: Instance de la gestion de la langue.
        :param obj_view: Instance représentant les informations réseau.
        :param obj_icon: Instance de gestion des icônes.
        :param parent: Widget parent, facultatif.
        """
        super().__init__(obj_title, obj_view, obj_icon, parent)
        self.setCardsList()  # Crée les cartes de l'interface
        self.setUCList()  # Crée la liste des périphériques
        self.setUCNetworkList()  # Crée la liste du réseau
        self.setInfoTableList()  # Crée la table d'informations

        # Initialiser les autres tables avec des listes vides
        self.updateUcListTable([])
        self.updateUcNetworkListTable([])
        self.updateInfoTableList([])

        # Met en place les cartes de l'interface utilisateur
        self.setCardsView()

    def setCardsList(self):
        wanBody = QWidget(self)
        wanLayout = QVBoxLayout(wanBody)

        domainProjectNameTtl = "Project Name"
        domainProjectNameEdit = QLineEdit(self.objManager.name)
        domainProjectNameEdit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        wanLayout.addWidget(LineUpdate(domainProjectNameTtl, domainProjectNameEdit))

        domainNameTtl = "Domain Name"
        domainNameEdit = QLineEdit(self.objManager.dns)
        domainNameEdit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        wanLayout.addWidget(LineUpdate(domainNameTtl, domainNameEdit))

        cidrTtl = "CIDR"
        cidrText = ip_to_cidr(self.objManager.ipv4, self.objManager.maskIpv4)
        cidrEdit = QLineEdit(cidrText)
        cidrEdit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        cidrEdit.setPlaceholderText("CIDR")

        if self.objManager.ipv6:
            cidrEdit.setToolTip(f"IPv6: {self.objManager.ipv6}")
        else:
            cidrEdit.setToolTip(f"IPv6: Not Setted")

        wanLayout.addWidget(LineUpdate(cidrTtl, cidrEdit))
        gateTtl = "Gateway"
        gateEdit = QLineEdit(self.objManager.gateway)
        gateEdit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        wanLayout.addWidget(LineUpdate(gateTtl, gateEdit))

        startDateTtl = "Start Date"
        startDateEdit = QLineEdit(conv_unix_to_datetime(self.objManager.clockManager.clockCreated))
        startDateEdit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        wanLayout.addWidget(LineUpdate(startDateTtl, startDateEdit))

        lastUpdateTtl = "Last Update"
        lastUpdateEdit = QLineEdit(conv_unix_to_datetime(self.objManager.clockManager.get_clock_last()))
        lastUpdateEdit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        wanLayout.addWidget(LineUpdate(lastUpdateTtl, lastUpdateEdit))

        wanLayout.addStretch()

        # Exemple de personnalisation pour LanDashboard
        self.cardList = [
            {
                "layout": {
                    "row": 0,
                    "column": 0,
                    "rowSpan": 1,
                    "columnSpan": 1,
                    "alignement": None
                },
                "top_card": CardHeader(
                    title_card=QLabel("WAN Status"),
                    icon_card=self.iconsManager.get_icon("lanIcon")),
                "center_card": wanBody,
            "left_card": None,
            "right_card": None,
            "bottom_card": None
            }
        ]

    def setUCList(self):
        uc_listHeadband: list = ["IPv4", "Name", "Mac Address", "Status", "Vendor"]
        self.uc_listBody = QTableWidget(self)
        self.uc_listBody.setColumnCount(len(uc_listHeadband))
        self.uc_listBody.setHorizontalHeaderLabels(uc_listHeadband)
        self.uc_listBody.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.uc_listBody.setSortingEnabled(True)
        
        self.scan_btn = QPushButton(self)
        self.scan_btn.setIcon(self.iconsManager.get_icon("runIcon"))
        self.scan_btn.clicked.connect(self.toggle_scan)
        self.scan_btn.setToolTip("Start the scan")
        self.scan_btn.setEnabled(True)

        self.pause_btn = QPushButton(self)
        self.pause_btn.setIcon(self.iconsManager.get_icon("pauseIcon"))
        self.pause_btn.clicked.connect(self.toggle_scan)
        self.pause_btn.setToolTip("Scan not loaded")
        self.pause_btn.setEnabled(False)

        ttls_btn = [self.scan_btn, self.pause_btn]
        uc_listTtl = TitleWithAction(f'LAN {self.objManager.dns}', 4, ttls_btn)

        uc_list_settings: dict = {
            "layout": {
                "row": 0,
                "column": 1,
                "rowSpan": 1,
                "columnSpan": 3,
                "alignement": None
            },
            "top_card": CardHeader(
                title_card=uc_listTtl,
                icon_card=self.iconsManager.get_icon("lanUcListIcon")),
            "center_card": self.uc_listBody,
            "left_card": None,
            "right_card": None,
            "bottom_card": None
        }
        self.cardList.append(uc_list_settings)

    def updateUcListTable(self, uc_list: list):
        self.uc_listBody.setRowCount(len(uc_list))
        for i, uc in enumerate(uc_list):
            self.uc_listBody.setItem(i, 0, QTableWidgetItem(uc["ipv4"]))
            self.uc_listBody.setItem(i, 1, QTableWidgetItem(uc["name"]))
            self.uc_listBody.setItem(i, 2, QTableWidgetItem(uc["mac"]))
            self.uc_listBody.setItem(i, 3, QTableWidgetItem(uc["status"]))
            self.uc_listBody.setItem(i, 4, QTableWidgetItem(str(uc["vendor"])))

    def run_scan(self):
        """
        Démarre l'obtention de la liste des UC de manière asynchrone via un Worker.
        """
        self.scan_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        # Crée la boîte de dialogue de progression
        self.progress_dialog = WDialogs()
        self.progress_dialog.set_maximum(len(self.objManager.devicesList))  # Indéfini (0) pour une tâche dont on ne connaît pas la durée
        self.progress_dialog.set_message("Fetching the list of devices...")

        # Crée un Worker pour récupérer les UC
        self.worker = WorkerGetUcList(self.objManager)

        # Connecte les signaux du Worker aux méthodes de la boîte de dialogue
        self.worker.signals.progress.connect(self.progress_dialog.update_progress)
        self.worker.signals.started.connect(lambda: self.progress_dialog.show())
        self.worker.signals.result.connect(self.on_scan_finished)
        self.worker.signals.finished.connect(self.progress_dialog.close)

        # Démarre le Worker dans un thread séparé
        QThreadPool.globalInstance().start(self.worker)

    def toggle_scan(self):
        """
        Vérifie si le scan est en cours et le démarre, le met en pause, ou le reprend.
        """
        if self.scan_btn.isEnabled():
            self.run_scan()
        elif self.scan_btn.isEnabled() and self.worker.is_paused:
            self.resume_scan()
        else:
            self.pause_scan()

    def on_scan_finished(self, result):
        """
        Méthode appelée lorsque le scan est terminé.
        """
        # logging.debug(f"303: {result}")
        self.updateUcListTable(result)
        self.scan_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)

    def pause_scan(self):
        """
        Met en pause le scan du réseau local.
        """
        if self.worker:  # Vérifie si un worker de scan est actif
            self.worker.pause()
            self.pause_btn.setEnabled(False)  # Désactive le bouton de pause
            self.pause_btn.setToolTip("Scan paused")
            self.scan_btn.setEnabled(True)  # Réactive le bouton de reprise
            self.scan_btn.setToolTip("Resume the scan")

    def resume_scan(self):
        """
        Reprend le scan du réseau local après une pause.
        """
        if self.worker:  # Vérifie si un worker de scan est actif
            self.worker.resume()
            self.scan_btn.setEnabled(False)  # Désactive le bouton de reprise
            self.scan_btn.setToolTip("Scanning in Progress")
            self.pause_btn.setEnabled(True)  # Active le bouton de pause
            self.pause_btn.setToolTip("Pause the scan")
    
    def setUCNetworkList(self):
        ucNetwork_listHeadband: list = ["Name/IPv4", "Emit", "Send"]
        self.ucNetwork_listBody = QTableWidget(self)
        self.ucNetwork_listBody.setColumnCount(len(ucNetwork_listHeadband))
        self.ucNetwork_listBody.setHorizontalHeaderLabels(
            ucNetwork_listHeadband)

        ucNetwork_list_settings: dict = {
            "layout": {
                "row": 1,
                "column": 0,
                "rowSpan": 1,
                "columnSpan": 2,
                "alignement": None
            },
            "top_card": CardHeader(
                title_card=QLabel("List of network equipment"),
                icon_card=qta.icon('mdi6.clipboard-text-multiple')),
            "center_card": self.ucNetwork_listBody,
            "left_card": None,
            "right_card": None,
            "bottom_card": None
        }
        self.cardList.append(ucNetwork_list_settings)

    def updateUcNetworkListTable(self, ucNetwork_list: list):
        self.ucNetwork_listBody.setRowCount(len(ucNetwork_list))
        for i, uc in enumerate(ucNetwork_list):
            self.ucNetwork_listBody.setItem(
                i, 0, QTableWidgetItem(uc["name"] or uc["ipv4"]))
            self.ucNetwork_listBody.setItem(i, 1, QTableWidgetItem(uc["emit"]))
            self.ucNetwork_listBody.setItem(i, 2, QTableWidgetItem(uc["send"]))

    # Asynchrone function return a list of dict
    async def getUcNetworkList(self):
        # return await self.objManager.get_lan_uc_network_list()
        return []

    def setInfoTableList(self):
        infoTable_listHeadband: list = ["Time", "Hostname/IPv4", "Message"]
        self.infoTable_listBody = QTableWidget(self)
        self.infoTable_listBody.setColumnCount(len(infoTable_listHeadband))
        self.infoTable_listBody.setHorizontalHeaderLabels(
            infoTable_listHeadband)

        infoTable_list_settings: dict = {
            "layout": {
                "row": 1,
                "column": 2,
                "rowSpan": 1,
                "columnSpan": 2,
                "alignement": None
            },
            "top_card": CardHeader(
                title_card=QLabel("Current Problems"),
                icon_card=qta.icon('mdi6.clipboard-alert')),
            "center_card": self.infoTable_listBody,
            "left_card": None,
            "right_card": None,
            "bottom_card": None
        }
        self.cardList.append(infoTable_list_settings)

    def updateInfoTableList(self, infoTable_list: list):
        self.infoTable_listBody.setRowCount(len(infoTable_list))
        for i, info in enumerate(infoTable_list):
            self.infoTable_listBody.setItem(
                i, 0, QTableWidgetItem(info["time"]))
            self.infoTable_listBody.setItem(
                i, 1, QTableWidgetItem(info["name"] or info["ipv4"]))
            self.infoTable_listBody.setItem(
                i, 2, QTableWidgetItem(info["message"]))

    # Asynchrone function return a list of dict
    async def getInfoTableList(self):
        # return await self.objManager.get_lan_info_table_list()
        return []


class UCDashboardFMC(FixedMosaicsCards):
    """
        Nom complet: Unit Central Dashboard Fixed Mosaics Cards
        Description: Cette classe est une mise à jour de 'UCDashboard(DashboardCardTemplate)'
        Nouveau nom: UCDashboardFMC
    """
    def __init__(self, obj_title: str, obj_view: Any, obj_icon: IconsApp, parent=None):
        super().__init__(obj_title, obj_view, obj_icon, parent)

    def setCardsList(self):
        # Exemple de personnalisation pour UCDashboard
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
                    icon_card=self.iconsManager.get_icon("ucIcon"),
                    title_card=QLabel("User Control")),
                "center_card": QLabel("Manage your users and permissions here.")
            }
        ]
