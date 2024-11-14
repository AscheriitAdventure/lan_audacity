"""
    Card component:
    - "Card" est un composant qui permet d'afficher des informations sous forme de carte.
    - "Card" est composé de plusieurs parties:
        ✅- "CardHeader": La partie supérieure de la carte qui contient le titre de la carte et un icone.
        ⛔️- "CardBody": La partie centrale de la carte qui contient les informations à afficher.
        ✅- "CardFooter": La partie inférieure de la carte qui contient les actions à effectuer sur la carte.
        ⛔️- "CardActions": La partie droite ou gauche de la carte qui contient les actions à effectuer sur la carte.
        👷- "CardImage": Une image à afficher dans la carte, avec plein de paramètres.
    ✅- "Card" est un composant générique qui peut être utilisé dans plusieurs contextes.
"""

import logging
from typing import Optional
from qtpy.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QLabel, QFrame
from qtpy.QtGui import *
from qtpy.QtCore import Qt, QRectF

from src.components.card.default_var import VAR_CardCSS


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
        image_label = QLabel()
        image_label.setPixmap(QPixmap.fromImage(image_card))
        self.imageCard_layout.addWidget(image_label)
        self.imageCard_layout.addStretch(1)

    def setListImageUI(self, image_card: list[QImage]):
        """Sets the image UI with a list of images."""
        pass
