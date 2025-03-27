from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *
from typing import *
import logging
import inspect

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


class Card(QWidget):
    def __init__(self, css_params: Optional[dict] = VAR_CardCSS, debug: Optional[bool] = False, parent=None):
        super(Card, self).__init__(parent)

        self.debug = debug
        self.activeSections: list = ["global"]

        self.paintProperties: dict = {}
        self.dirtyRects: Dict[str, bool] = {
            "global": True, 
            "top": False, 
            "left": False,
            "center": False, 
            "right": False, 
            "bottom": False
        }
        self.cssParameters(css_params)

        self.topCard: Optional[QWidget] = None
        self.leftCard: Optional[QWidget] = None
        self.centerCard: Optional[QWidget] = None
        self.rightCard: Optional[QWidget] = None
        self.bottomCard: Optional[QWidget] = None

        self.initUI()

    def initUI(self, rebuild=False):
        """Initialise ou réinitialise la mise en page
    
        Args:
            rebuild (bool): Si True, supprime d'abord tous les widgets existants
        """
        
        if rebuild and self.mainLayout is not None:
            self._clearLayout()
        else:
            self.mainLayout = QGridLayout(self)
            self.setLayout(self.mainLayout)
        
        self._arrangeWidgets(0, 0, 3)
        self.markAllDirty()

    def cssParameters(self, css_params: Optional[dict] = None):
        """Sets the CSS parameters for the CardUI widget."""
        old_props = self.paintProperties
        self.paintProperties = css_params
        
        # Marquer les sections modifiées
        for section in css_params:
            if section not in old_props or css_params[section] != old_props.get(section):
                self.dirtyRects[section] = True
        
        self.update()

    def setTopCard(self, top_card: Optional[QWidget] = None):
        """Sets the top card widget."""
        oldCard = self.topCard
        self.topCard = top_card
        
        if oldCard is not None and oldCard != top_card:
            oldCard.setParent(None)
    
        self.dirtyRects["top"] = True
        self.initUI(rebuild=True)

    def setLeftCard(self, left_card: Optional[QWidget] = None):
        """Sets the left card widget."""
        oldCard = self.leftCard
        self.leftCard = left_card
    
        if oldCard is not None and oldCard != left_card:
            oldCard.setParent(None)
    
        self.dirtyRects["left"] = True
        self.initUI(rebuild=True)

    def setCenterCard(self, center_card: Optional[QWidget] = None):
        """Sets the center card widget."""
        oldCart = self.centerCard
        self.centerCard = center_card

        if oldCart is not None and oldCart != center_card:
            oldCart.setParent(None)
        
        self.dirtyRects["center"] = True
        self.initUI(rebuild=True)

    def setRightCard(self, right_card: Optional[QWidget] = None):
        """Sets the right card widget."""
        oldCard = self.rightCard
        self.rightCard = right_card

        if oldCard is not None and oldCard != right_card:
            oldCard.setParent(None)

        self.dirtyRects["right"] = True
        self.initUI(rebuild=True)

    def setBottomCard(self, bottom_card: Optional[QWidget] = None):
        """Sets the bottom card widget."""
        oldCard = self.bottomCard
        self.bottomCard = bottom_card

        if oldCard is not None and oldCard != bottom_card:
            oldCard.setParent(None)

        self.dirtyRects["bottom"] = True
        self.initUI(rebuild=True)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        sct: Dict = {"global": QRectF(self.rect())}

        if self.topCard is not None:
            sct["top"] = self.getTruePosition(self.topCard, "Top")
        if self.leftCard is not None:
            sct["left"] = self.getTruePosition(self.leftCard)
        if self.centerCard is not None:
            sct["center"] = self.getTruePosition(self.centerCard)
        if self.rightCard is not None:
            sct["right"] = self.getTruePosition(self.rightCard)
        if self.bottomCard is not None:
            sct["bottom"] = self.getTruePosition(self.bottomCard, "Bottom")
        
        # Dessiner uniquement les sections marquées comme "dirty"
        for section in sct:
            rect = sct[section]
            if self.debug:
                logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Drawing {section}: {rect}")
            
            styles = self.paintProperties.get(section, {})
            if styles:
                self.paintSection(painter, rect, styles)
                
            self.dirtyRects[section] = False
        
        painter.end()

    def getTruePosition(self, widget: QWidget, top_bottom:Optional[str] = None) -> QRectF:
        """Récupère la position absolue du widget dans la fenêtre."""
        vqo = widget.rect() # Variable QRectF Object
        wdt = vqo.width()   # width
        hgt = vqo.height()  # height
        vpo = widget.pos()  # Variable Position Object
        x = vpo.x()         # x
        y = vpo.y()         # y

        lm, tm, rm, bm = self.mainLayout.getContentsMargins()
        tbm = bm * 0.75 + tm * 0.75 # Top/Bottom Margin
        tbw = self.rect().width()   # Top/Bottom Width
        
        if top_bottom == "Bottom":
            return QRectF(x-lm, y-0.25*tm, tbw, hgt+tbm)
        elif top_bottom == "Top":
            return QRectF(x-lm, y-tm, tbw, hgt+tbm)
        else:
            return QRectF(x, y, wdt, hgt)
    
    def paintSection(self, painter: QPainter, rect: QRectF, styles: dict):
        """Dessine une section de la carte avec les styles spécifiés."""
        bcko = styles.get("background", {}) # Background Object
        brdo = styles.get("border", {})     # Border Object
        sdwo = styles.get("shadow", {})     # Shadow Object

        borderRadius = brdo["radius"] if brdo.get("radius") else 0
        borderWidth = brdo["width"] if brdo.get("width") else 0

        # Dessiner le fond
        if bcko.get("color"):
            bckc = self._parseColor(bcko["color"])    # Background Color
            painter.setBrush(QBrush(bckc))
            qpp = QPainterPath()
            qpp.addRoundedRect(rect, borderRadius, borderRadius)
            painter.fillPath(qpp, bckc)
        
        if bcko.get("image"):
            bcki = self._parseImage(bcko["image"])  # Background Image
            painter.drawImage(rect, bcki)

        # Dessiner la bordure
        if brdo.get("color"):
            brdc = self._parseColor(brdo["color"])  # Border Color
            
        if brdo.get("style") == "solid":
            borderStyle = Qt.PenStyle.SolidLine
        elif brdo.get("style") == "dash":
            borderStyle = Qt.PenStyle.DashLine
        elif brdo.get("style") == "dot":
            borderStyle = Qt.PenStyle.DotLine
        else:
            borderStyle = Qt.PenStyle.NoPen

        if borderWidth > 0:
            painter.setPen(QPen(brdc, borderWidth, borderStyle))
            if brdo.get("top"):
                painter.drawLine(rect.topLeft(), rect.topRight())
            elif brdo.get("right"):
                painter.drawLine(rect.topRight(), rect.bottomRight())
            elif brdo.get("bottom"):
                painter.drawLine(rect.bottomLeft(), rect.bottomRight())
            elif brdo.get("left"):
                painter.drawLine(rect.topLeft(), rect.bottomLeft())
            else:
                pen = QPen(brdc, borderWidth, borderStyle)
                painter.setPen(pen)
                if borderRadius:
                    painter.drawRoundedRect(rect, borderRadius, borderRadius)
                else:
                    painter.drawRect(rect)
                                
    def setBorderStyle(self, **kwargs):
        """ 
            Modifie le style de bordure de la section spécifiée.
            Args:
                section (str): les différentes sections sont: ["global", "top", "left", "center", "right", "bottom"]
                color (Optional[QColor], optional): _description_. Defaults to None.
                width (Optional[int], optional): _description_. Defaults to None.
                radius (Optional[int], optional): _description_. Defaults to None.
                style (Optional[str], optional): _description_. Defaults to None.
        """
        section = kwargs.get("section")
        if section and section in self.dirtyRects:
            self.dirtyRects[section] = True
            
            # Préparation des paramètres
            params = {}
            if kwargs.get("width") is not None:
                params["width"] = int(kwargs["width"])
            if kwargs.get("radius") is not None:
                params["radius"] = int(kwargs["radius"])
            if kwargs.get("style") is not None:
                params["style"] = kwargs["style"]
            if kwargs.get("color") is not None:
                params["color"] = self._parseColor(kwargs["color"])
            
            # Mise à jour des propriétés
            if section not in self.paintProperties:
                self.paintProperties[section] = {}
            if "border" not in self.paintProperties[section]:
                self.paintProperties[section]["border"] = {}
                
            for key, value in params.items():
                self.paintProperties[section]["border"][key] = value
                
            self.update()
    
    def _parseColor(self, color: Union[str, QColor, tuple]) -> QColor:
        """Convertit une couleur en objet QColor."""
        if isinstance(color, QColor):
            return color
        elif isinstance(color, tuple):
            return QColor(*color)
        elif isinstance(color, str):
            c = QColor()
            c.setNamedColor(color)
            return c
        return QColor("black")  # Valeur par défaut

    def _parseImage(self, image: Union[str, QImage, QPixmap]) -> QImage:
        """Convertit une image en objet QImage."""
        if isinstance(image, QImage):
            return image
        elif isinstance(image, QPixmap):
            return image.toImage()
        elif isinstance(image, str):
            img = QImage(image)
            if not img.isNull():
                return img
            elif self.debug:
                logging.warning(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Image not found: {image}")
        elif self.debug:
            logging.warning(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Invalid image type: {image}")
        return QImage()
    
    def markAllDirty(self):
        """Marque toutes les sections comme nécessitant une mise à jour."""
        for section in self.dirtyRects:
            self.dirtyRects[section] = True
        self.update()
    
    def markSectionDirty(self, section: str):
        """Marque une section spécifique comme nécessitant une mise à jour."""
        if section in self.dirtyRects:
            self.dirtyRects[section] = True
            self.update()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        
        self.markAllDirty()
        self.update()

    def _clearLayout(self):
        """Supprime tous les widgets du layout"""
        if self.mainLayout is None:
            return
        
        while self.mainLayout.count():
            item = self.mainLayout.takeAt(0)
            if item.widget():
                if item.widget() in [self.topCard, self.leftCard, self.centerCard, self.rightCard, self.bottomCard]:
                    item.widget().setParent(None)
                else:
                    item.widget().deleteLater()

    def _arrangeWidgets(self, rowStart=0, colStart=0, colSpan=3):
        """
        Arrange les widgets dans le layout
    
        Args:
            rowStart (int): Ligne de départ
            colStart (int): Colonne de départ
            colSpan (int): Nombre de colonnes à occuper
        """
        if self.topCard is not None:
            if self.debug:
                logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Setting top card")
            self.mainLayout.addWidget(self.topCard, rowStart, colStart, 1, colSpan, Qt.AlignmentFlag.AlignTop)
            rowStart += 1

        if self.bottomCard is not None:
            if self.debug:
                logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Setting bottom card")
            self.mainLayout.addWidget(self.bottomCard, 2, 0, 1, 3)

        if self.leftCard is not None:
            if self.debug:
                logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Setting left card")
            self.mainLayout.addWidget(self.leftCard, rowStart, colStart, 1, 1)
            colStart += 1
            colSpan -= 1

        if self.rightCard is not None:
            if self.debug:
                logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Setting right card")
            self.mainLayout.addWidget(self.rightCard, rowStart, 2, 1, 1)
            colSpan -= 1

        if self.centerCard is not None:
            if self.debug:
                logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Setting center card")
            self.mainLayout.addWidget(self.centerCard, rowStart, colStart, 1, colSpan)

    def setAllCards(self, top=None, left=None, center=None, right=None, bottom=None):
        """Met à jour tous les widgets d'un coup pour éviter plusieurs rebuilds
    
        Args:
            top (QWidget, optional): Widget supérieur
            left (QWidget, optional): Widget gauche
            center (QWidget, optional): Widget central
            right (QWidget, optional): Widget droit
            bottom (QWidget, optional): Widget inférieur
        """
        old_widgets = [self.topCard, self.leftCard, self.centerCard, self.rightCard, self.bottomCard]
        
        if top is not None:
            self.topCard = top
            self.dirtyRects["top"] = True
    
        if left is not None:
            self.leftCard = left
            self.dirtyRects["left"] = True
    
        if center is not None:
            self.centerCard = center
            self.dirtyRects["center"] = True
    
        if right is not None:
            self.rightCard = right
            self.dirtyRects["right"] = True
    
        if bottom is not None:
            self.bottomCard = bottom
            self.dirtyRects["bottom"] = True
        
        self.initUI(rebuild=True)
        for widget in old_widgets:
            if widget is not None and widget not in [self.topCard, self.leftCard, self.centerCard, self.rightCard, self.bottomCard]:
                widget.setParent(None)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.exec_(Qt.DropAction.MoveAction)
