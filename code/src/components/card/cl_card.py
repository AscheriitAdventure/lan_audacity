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


class Card(QWidget):
    def __init__(
        self,
        top_card: Optional[QWidget] = None,  # Optional[CardHeader],
        left_card: Optional[QWidget] = None,
        center_card: Optional[QWidget] = None,
        right_card: Optional[QWidget] = None,
        bottom_card: Optional[QWidget] = None,  # Optional[CardFooter],
        css_params: Optional[dict] = None,
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
            self.card_layout.addWidget(self.topCard, var_rowStart, var_colStart, 1, 3, Qt.AlignmentFlag.AlignLeft)
            logging.debug(f"Top Card:({var_rowStart},{var_colStart},1,3)")
            var_rowStart = var_rowStart + 1

        if bottom_card is not None:
            # Il occupera la dernière ligne de la grille
            self.bottomCard = bottom_card
            self.card_layout.addWidget(self.bottomCard, 2, 0, 1, 3)
            logging.debug(f"Bottom Card:(2,0,1,3)")

        if left_card is not None:
            # Il occupera la première colonne de la grille
            self.leftCard = left_card
            self.card_layout.addWidget(self.leftCard, var_rowStart, var_colStart, 1, 1)
            logging.debug(f"Left Card:({var_rowStart},{var_colStart},1,1)")
            var_colStart = var_colStart + 1
            var_colSpan = var_colSpan - 1

        if right_card is not None:
            # Il occupera la dernière colonne de la grille
            self.rightCard = right_card
            self.card_layout.addWidget(self.rightCard, var_rowStart, 2, 1, 1)
            logging.debug(f"Right Card:({var_rowStart},2,1,1)")
            var_colSpan = var_colSpan - 1

        if center_card is not None:
            # center_card occupera tout l'espace restant
            self.centerCard = center_card
            self.card_layout.addWidget(
                self.centerCard, var_rowStart, var_colStart, 1, var_colSpan
            )
            logging.debug(f"Top Card:({var_rowStart},{var_colStart},1,{var_colSpan})")

    def cssParameters(self, css_params: Optional[dict] = None):
        """Sets the CSS parameters for the CardUI widget."""
        if css_params is None:
            css_params = {
                "background": {
                    "color": "Gainsboro",
                    "image": None,
                },
                "border": {
                    "width": 1,
                    "color": "DarkGray",
                    "radius": 4,
                    "style": "solid",
                },
            }
        
        self.paintProperties = css_params
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(self.rect())
        borderRadius = self.paintProperties["border"]["radius"] or 0

        # Draw Background
        if self.paintProperties["background"]["color"]:
            backgroudColor = QColor(self.paintProperties["background"]["color"])
            painter.setBrush(QBrush(backgroudColor))
            path = QPainterPath()
            path.addRoundedRect(rect, borderRadius, borderRadius)
            painter.fillPath(path, backgroudColor)
        
        if self.paintProperties["background"]["image"]:
            backgroundgImage = self.paintProperties["background"]["image"]
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
        
        # Draw Border
        # Largeur de la bordure
        borderWidth = self.paintProperties["border"]["width"] or 0
        # Couleur de la bordure
        if isinstance(self.paintProperties["border"]["color"], QColor):
            borderColor = self.paintProperties["border"]["color"]
        elif isinstance(self.paintProperties["border"]["color"], tuple):
            borderColor = QColor(*self.paintProperties["border"]["color"])
        elif isinstance(self.paintProperties["border"]["color"], str):
            borderColor = QColor()
            borderColor.setNamedColor(self.paintProperties["border"]["color"])
        else:
            borderColor = QColor()
            borderColor.setNamedColor("Black")
        # Style de la bordure
        if self.paintProperties["border"]["style"] == "solid":
            borderStyle = Qt.PenStyle.SolidLine
        elif self.paintProperties["border"]["style"] == "dash":
            borderStyle = Qt.PenStyle.DashLine
        elif self.paintProperties["border"]["style"] == "dot":
            borderStyle = Qt.PenStyle.DotLine
        else:
            borderStyle = Qt.PenStyle.NoPen
        
        if borderWidth > 0:
            painter.setPen(borderStyle)
            pen = QPen(borderColor, borderWidth)
            painter.setPen(pen)
            if borderRadius:
                painter.drawRoundedRect(rect, borderRadius, borderRadius)
            else:
                painter.drawRect(rect)

        # Apply shadow effect if specified
        # shadow_blur = self.paintProperties["shadow_blur"] or 0

        painter.end()
    
    def setBorderStyle(
            self, 
            color: Optional[QColor] = None, 
            width: Optional[int] = None,
            radius: Optional[int] = None,
            style: Optional[str] = None
            ):
        if color:
            self.paintProperties["border"]["color"] = QColor(color)
        if width is not None:
            self.paintProperties["border"]["width"] = width
        if radius is not None:
            self.paintProperties["border"]["radius"] = radius
        if style:
            self.paintProperties["border"]["style"] = style

        self.update()
    
    def setBackgroundStyle(self, color: Optional[QColor] = None, image: Optional[QImage] = None):
        if color:
            self.paintProperties["background"]["color"] = QColor(color)
        if image:
            self.paintProperties["background"]["image"] = QImage(image)
        self.update()
    

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
