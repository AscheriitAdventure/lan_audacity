from default_var import VAR_CardCSS
from qtpy.QtWidgets import QWidget, QGridLayout, QVBoxLayout
from qtpy.QtCore import Qt, QRectF, QPointF, QSizeF, QRect
from qtpy.QtGui import *
import sys
import logging
from typing import Optional

"""
    Etape 1:
    Avec pyqt6.
    Création d'un objet qui créer un support pour inserér des widgets.
    l'objet en question doit afficher quand il est vide un carré vide.
    En gros, l'objet doit afficher les bordures du carré.

    Etape 2:
    En suivant, il doit proposer des méthodes pour modifier la forme du carré.
    Exemple:
        - Modifier les bordures (couleur, taille, forme)
        - Ajouter une ombre
        - Ajouter une image de fond
        - Modifier la couleur de fond
"""


class StyleableCard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Default style properties
        self.border_color = QColor(0, 0, 0)  # Black
        self.border_width = 2
        self.bg_color = QColor(255, 255, 255)  # White
        self.border_radius = 0
        self.shadow_blur = 0
        self.bg_image = None

        # Set minimum size
        self.setMinimumSize(100, 100)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw background
        painter.setBrush(self.bg_color)
        painter.setPen(QPen(self.border_color, self.border_width))
        painter.drawRect(self.rect())

    def set_border_style(self, color=None, width=None):
        if color:
            self.border_color = QColor(color)
        if width is not None:
            self.border_width = width
        self.update()

    def set_background_color(self, color):
        self.bg_color = QColor(color)
        self.update()


"""
    Commenataire:
        Je suis bon pour recommencer à zéro.
    Consignes:
        Nom Complet: Custom Card Widget
        Outils de support:
            - QtPy(PyQt6)
            - logging
            - sys
            - nom de la Classe: CCWStyleable
        Etape 1:
            - Créer un objet qui affiche un carré vide. [OK]
            - L'objet doit afficher les bordures du carré. [OK]
            - L'objet doit avoir un minimum de 100x100. [OK]
"""

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CCWStyleable(QWidget):
    def __init__(
            self,
            border_color: Optional[QColor] = QColor(0, 0, 0),
            border_width: Optional[int] = 2,
            bg_color: Optional[QColor] = None,
            border_radius: Optional[int] = None,
            shadow_blur: Optional[int] = None,
            bg_image: Optional[str | QImage] = None,
            parent=None):
        super().__init__(parent)
        logger.info("Initializing CCWStyleable widget")
        """
        Custom Card Widget that can be styled with various properties.
        :param border_color: Border color of the card.
        :param border_width: Border width of the card.
        :param bg_color: Background color of the card.
        :param border_radius: Border radius of the card.
        :param shadow_blur: Shadow blur radius of the card.
        :param bg_image: Background image of the card.
        """

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Default properties
        self.paintProperties: dict = {
            "border_color": border_color,
            "border_width": border_width,
            "bg_color": bg_color,
            "border_radius": border_radius,
            "shadow_blur": shadow_blur,
            "bg_image": QPixmap(bg_image) if isinstance(bg_image, str) else bg_image,
        }

        # Set minimum size
        self.setMinimumSize(100, 100)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Retrieve paint properties
        border_color = self.paintProperties["border_color"]
        border_width = self.paintProperties["border_width"]
        bg_color = self.paintProperties["bg_color"]
        border_radius = self.paintProperties["border_radius"] or 0
        shadow_blur = self.paintProperties["shadow_blur"] or 0
        bg_image = self.paintProperties["bg_image"]

        # Define the rect for painting
        rect = QRectF(self.rect())

        # Draw background color with rounded corners if specified
        if bg_color:
            painter.setBrush(QBrush(bg_color))
            path = QPainterPath()
            path.addRoundedRect(rect, border_radius, border_radius)
            painter.fillPath(path, bg_color)

        # Draw background image if provided
        if bg_image:
            if isinstance(bg_image, QPixmap):
                painter.drawPixmap(rect, bg_image)
            elif isinstance(bg_image, QImage):
                painter.drawImage(rect, bg_image)
            elif isinstance(bg_image, str):
                # Load image from file
                image = QImage(bg_image)
                if image.isNull():
                    logger.warning(
                        f"Failed to load image from file: {bg_image}")
                else:
                    painter.drawImage(rect, image)
            else:
                logger.warning(f"Invalid background image type: {type(bg_image)}")

        # Draw border if specified
        if border_width > 0 and border_color:
            painter.setPen(Qt.PenStyle.SolidLine)
            pen = QPen(QColor(border_color), border_width)
            painter.setPen(pen)
            if border_radius:
                painter.drawRoundedRect(rect, border_radius, border_radius)
            else:
                painter.drawRect(rect)

        # Apply shadow effect if specified
        if shadow_blur:
            # This can be implemented with QGraphicsDropShadowEffect if this widget
            # is placed in a QGraphicsScene or similar environment.
            pass  # Shadow handling left for further extension if needed

        painter.end()

    def setBorderStyle(self, color=None, width=None):
        if color:
            self.paintProperties["border_color"] = QColor(color)
        if width is not None:
            self.paintProperties["border_width"] = width
        self.update()

    def set_background_color(self, color):
        self.paintProperties["bg_color"] = QColor(color)
        self.update()


"""
    Commenataire:
        Que je suis Doué... passons à la suite.
    Consignes:
        Nom Complet: Custom Card Widget Version Upgrade 1
        Outils de support:
            - QtPy(PyQt6)
            - logging
            - sys
            - nom de la Classe: CCWVU1
        Etape 2:
            - Modifier paintEvent pour prendre en compte les différentes sections de la carte tout en utilisant "VAR_CardCSS". [OK]
            - Ajouter des sections pour les cartes du haut, du bas, de gauche, de droite et du centre. [OK]
            - Ajouter des méthodes pour modifier les sections de la carte. [OK]
            - Ajouter des méthodes pour modifier les styles de bordure et de fond de la carte. [OK]
"""


class CCWVU1(QWidget):
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
        super(CCWVU1, self).__init__(parent)
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
    

"""
    Commentaire:
        C'est un bon début. Mais c'est pas encore ça.
    Consignes:
        Nom Complet: Custom Card Widget Version Upgrade 2
        Outils de support:
            - QtPy(PyQt6)
            - logging
            - sys
            - nom de la Classe: CCWVU2
        Etape 3:
            - Trouver une solution pour gérer CORRECTEMENT les widgets qui sont ajoutés aux différentes sections de la carte. [OK]
            - Ajouter des méthodes pour "Peindre" les sections de la carte. [OK]
"""

"""
    Commentaire:
        Nous sommes sur la bonne voie. Passons à la suite.
    Consignes:
        Nom Complet: Custom Card Widget Version Upgrade 3
        Outils de support:
            - QtPy(PyQt6)
            - logging
            - sys
            - nom de la Classe: CCWVU3
        Etape 4:
            - Ajouter des méthodes pour gérer l'ombre de la carte. 
"""