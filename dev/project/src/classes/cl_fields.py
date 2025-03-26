from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *
from typing import *
import enum
import logging
import inspect


class NetworkField(QWidget):
    pass

    def addData(self, **kwargs) -> None:
        argl: List[tuple] = [
            ("title", str),
            ("form_list", str),
            ("icon", dict),
            ("separator", bool),
            ("collapsed", bool),
            ("actions", list),
            ("description", str),
            ("visible", bool)
        ]
        
        
        for arg in kwargs:
            pass

class WidgetField(QWidget):
    class GridForm(enum.Enum):
        GList = 1      # une colonne, 1 ligne
        CMosaics = 2   # Vue par colonnes
        RMosaics = 3   # Vue par lignes

    def __init__(self, debug: bool = False, parent=None):
        super(WidgetField, self).__init__(parent)

        self._debug = debug
        self._gridObjects: List[QWidget] = []
        self._gridForm: WidgetField.GridForm = WidgetField.GridForm.CMosaics
        self._grid_number: int = 3  # Par défaut : 3 colonnes ou 3 lignes
        self.items: dict = {}

        self.initUI()
    
    def setHeaderArea(self, widget: QWidget) -> None:
        # Supprimer l'ancien widget du layout s'il existe
        if hasattr(self, 'headerArea') and self.headerArea is not None:
            self.mainLayout.removeWidget(self.headerArea)
            self.headerArea.setParent(None)
    
        # Assigner et ajouter le nouveau widget
        self.headerArea = widget
        if widget is not None:
            # Insérer le widget en première position (index 0)
            self.mainLayout.insertWidget(0, widget)
    
        # Forcer une mise à jour visuelle
        self.mainLayout.update()

    def initUI(self):
        self.setAcceptDrops(True)
        # Main layout
        self.mainLayout = QVBoxLayout(self)
        self.setLayout(self.mainLayout)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.headerArea = QWidget()
        self.mainLayout.addWidget(self.headerArea)

        # Add Scroll Area
        self._loadScrollArea()
        
    def _loadScrollArea(self):
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.mainLayout.addWidget(self.scrollArea)

        # Create container widget for scroll area
        self.scrollContainer = QWidget()
        self.scrollContainer.setAcceptDrops(True)
        self.scrollArea.setWidget(self.scrollContainer)
        self.scrollLayout = QGridLayout(self.scrollContainer)
        self.scrollLayout.setContentsMargins(0, 0, 0, 0)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        event.acceptProposedAction()
        
    def dropEvent(self, event: QDropEvent):
        pos = event.pos()
        widget = event.source()

        if widget and isinstance(widget, QWidget) and widget in self.items:
            # Trouver la position dans la grille la plus proche
            for lbl, (row, col) in self.items.items():
                cell_widget = self.scrollLayout.itemAtPosition(row, col).widget()
                if cell_widget == widget:  # Éviter de repositionner le même widget
                    continue

                rect = cell_widget.geometry()
                if rect.contains(pos):
                    # Récupérer le rowSpan et columnSpan des deux widgets
                    old_row, old_col = self.items[widget]
                
                    # Récupérer les informations de disposition pour les deux widgets
                    widget_index = self.scrollLayout.indexOf(widget)
                    target_index = self.scrollLayout.indexOf(cell_widget)

                    # Utiliser getItemPosition qui retourne (row, column, rowSpan, columnSpan)
                    _, _, widget_row_span, widget_col_span = self.scrollLayout.getItemPosition(widget_index)
                    _, _, target_row_span, target_col_span = self.scrollLayout.getItemPosition(target_index)
                
                    # Supprimer les widgets actuels de la grille pour éviter les conflits
                    self.scrollLayout.removeWidget(widget)
                    self.scrollLayout.removeWidget(cell_widget)
                
                    # Ajouter les widgets aux nouvelles positions avec leurs spans respectifs
                    self.scrollLayout.addWidget(widget, row, col, target_row_span, target_col_span)
                    self.scrollLayout.addWidget(cell_widget, old_row, old_col, widget_row_span, widget_col_span)

                    # Mettre à jour le dictionnaire des positions
                    self.items[widget] = (row, col)
                    self.items[cell_widget] = (old_row, old_col)
                    break

        event.acceptProposedAction()
    
    def setGridForm(self, form: 'WidgetField.GridForm', grid_number: int = 1):
        """
        Définit la forme de la grille et le nombre de colonnes/lignes.
        
        Args:
            form: Type de grille (GList, CMosaics, RMosaics)
            grid_number: Nombre de colonnes ou de lignes selon le mode
        """
        self._gridForm = form
        if form == self.GridForm.GList:
            self._grid_number = 1  # Pour GList, toujours 1
        else:
            self._grid_number = max(1, grid_number)  # Au moins 1

    def isColumnMode(self) -> bool:
        return self._gridForm in {self.GridForm.GList, self.GridForm.CMosaics}
    
    def isRowMode(self) -> bool:
        return self._gridForm == self.GridForm.RMosaics
    
    def checkLayoutMode(self) -> str:
        if self.isColumnMode():
            return "column"
        
        if self.isRowMode():
            return "row"
    
    def refreshGrid(self):
        """
        Réorganise tous les widgets dans la grille selon la forme actuelle.
        À appeler après un changement de GridForm ou de grid_number.
        """
        if not self.items:
            return  # Rien à faire si la grille est vide
        
        # Sauvegarder l'état actuel
        widgets_info = []
        for widget in self._gridObjects:
            item_index = self.scrollLayout.indexOf(widget)
            if item_index != -1:
                pos = self.scrollLayout.getItemPosition(item_index)
                if pos:
                    r, c, rs, cs = pos
                    widgets_info.append((widget, rs, cs))
        
        # Vider la grille
        for widget, _, _ in widgets_info:
            self.scrollLayout.removeWidget(widget)
        
        # Effacer le dictionnaire des positions
        self.items.clear()
        
        # Replacer les widgets
        for widget, rs, cs in widgets_info:
            next_pos = self.getNextFreePosition(rs, cs)
            self.scrollLayout.addWidget(
                widget, 
                next_pos["row"],
                next_pos["column"],
                next_pos["rowSpan"],
                next_pos["columnSpan"]
            )
            self.items[widget] = (next_pos["row"], next_pos["column"])

    def addCard(self, widget: Optional[QWidget] = None, positions: Optional[dict] = None) -> None:
        """
        Ajoute une carte à la grille à la prochaine position libre.
        
        Args:
            widget: Widget à ajouter (si None, une carte par défaut est créée)
            positions: Dictionnaire de positions (si None, utilise les valeurs par défaut)
        """
        if positions is None:
            tmp_dict: dict = {
                "layout": {
                    "row": 0,
                    "column": 0,
                    "rowSpan": 1,
                    "columnSpan": 1,
                    "alignment": Qt.AlignmentFlag.AlignCenter
                }
            }
        else:
            if self._debug:
                logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {positions}")

            tmp_dict = positions
            
        if widget is None:
            card = Card(debug=True)
        else:
            card = widget

        # Assurez-vous que les clés existent avant d'y accéder
        row_span = tmp_dict["layout"].get("rowSpan", 1)
        col_span = tmp_dict["layout"].get("columnSpan", 1)

        next_free_pos = self.getNextFreePosition(row_span, col_span)

        tmp_dict["layout"]["row"] = next_free_pos["row"]
        tmp_dict["layout"]["column"] = next_free_pos["column"]

        # Ajouter le widget à la liste des objets de la grille
        self._gridObjects.append(card)
        self.scrollLayout.addWidget(
            card,
            tmp_dict["layout"]["row"],
            tmp_dict["layout"]["column"],
            tmp_dict["layout"]["rowSpan"],
            tmp_dict["layout"]["columnSpan"],
            tmp_dict["layout"]["alignment"]
        )
        self.items[card] = (tmp_dict["layout"]["row"], tmp_dict["layout"]["column"])

    def getNextFreePosition(self, rowSpan: int = 1, columnSpan: int = 1) -> Dict[str, int]:
        """
        Détermine la prochaine position libre dans la grille pour une carte de taille spécifiée.
    
        Args:
            rowSpan: Nombre de lignes que la carte occupera
            columnSpan: Nombre de colonnes que la carte occupera
        
        Returns:
            Dict[str, int]: Dictionnaire contenant row, column, rowSpan, columnSpan
        """
        # Initialisation des valeurs par défaut
        max_row, max_col = 0, 0

        resultDict: dict = {
            "row": 0,
            "column": 0,
            "rowSpan": rowSpan,
            "columnSpan": columnSpan
        }

        if not self.items:
            return resultDict
        
        # Parcourir tous les widgets existants pour trouver les positions occupées
        occupied_cells = set()
        for widget, (row, col) in self.items.items():
            item_index = self.scrollLayout.indexOf(widget)
            if item_index != -1:  # Vérifier que le widget est bien dans la grille
                pos = self.scrollLayout.getItemPosition(item_index)
                if pos:
                    r, c, rs, cs = pos
                    # Ajouter toutes les cellules occupées par ce widget
                    for i in range(r, r + rs):
                        for j in range(c, c + cs):
                            occupied_cells.add((i, j))
                    # Mettre à jour les valeurs maximales
                    max_row = max(max_row, r + rs - 1)
                    max_col = max(max_col, c + cs - 1)
        
        # Stratégie de placement basée sur le mode de grille
        if self.isColumnMode():
            # En mode colonne, on remplit d'abord les colonnes
            max_columns = self._grid_number
        
            # Parcourir la grille pour trouver une position libre assez grande
            for row in range(max_row + 2):  # +2 pour vérifier au-delà de la dernière ligne
                for col in range(max_columns):
                    # Vérifier si l'espace est suffisant
                    can_place = True
                    # Vérifier que le placement ne dépasse pas la limite de colonnes
                    if col + columnSpan > max_columns:
                        can_place = False
                        continue
                    
                    for r in range(row, row + rowSpan):
                        for c in range(col, col + columnSpan):
                            if (r, c) in occupied_cells:
                                can_place = False
                                break
                        if not can_place:
                            break
                
                    if can_place:
                        resultDict["row"] = row
                        resultDict["column"] = col
                        return resultDict
            
            # Si pas de place trouvée, ajouter à la ligne suivante
            resultDict["row"] = max_row + 1
            resultDict["column"] = 0
            return resultDict

        elif self.isRowMode():
            # En mode ligne, on remplit d'abord les lignes
            max_rows = self._grid_number

            # Parcourir la grille pour trouver une position libre assez grande
            for col in range(max_col + 2):  # +2 pour vérifier au-delà de la dernière colonne
                for row in range(max_rows):
                    # Vérifier si l'espace est suffisant
                    can_place = True
                    # Vérifier que le placement ne dépasse pas la limite de lignes
                    if row + rowSpan > max_rows:
                        can_place = False
                        continue
                    
                    for r in range(row, row + rowSpan):
                        for c in range(col, col + columnSpan):
                            if (r, c) in occupied_cells:
                                can_place = False
                                break
                        if not can_place:
                            break
                
                    if can_place:
                        resultDict["row"] = row
                        resultDict["column"] = col
                        return resultDict
            
            # Si pas de place trouvée, ajouter à la colonne suivante
            resultDict["row"] = 0
            resultDict["column"] = max_col + 1
            return resultDict

        # Par défaut, simplement ajouter à la fin
        resultDict["row"] = max_row + 1
        resultDict["column"] = 0
        return resultDict


class CardImage(QWidget):
    def __init__(
            self,
            list_image: Optional[Union[List[QImage], QImage]] = None,
            debug: bool = False,
            parent=None):
        super(CardImage, self).__init__(parent)

        self.debug = debug
        self.listPicture: List[QImage] = list_image if list_image is not None else [
        ]

        self.initUI()

    def initUI(self):
        self.mainLayout = QHBoxLayout(self)
        self.setLayout(self.mainLayout)

        if len(self.listPicture) == 1:
            self.setImageUI(self.listPicture[0])
        elif len(self.listPicture) > 1:
            self.setListImageUI(self.listPicture)

    def setImageUI(self, image_card: QImage):
        """Sets the image UI with an image."""
        self.mainLayout.addStretch(1)
        lbl = QLabel()
        lbl.setPixmap(QPixmap.fromImage(image_card))
        self.mainLayout.addWidget(lbl)
        self.mainLayout.addStretch(1)

    def setListImageUI(self, image_card: list[QImage], orientation: Qt.LayoutDirection = Qt.LayoutDirection.LeftToRight):
        """
            Sets the image UI with a list of images.
            Set a carousel of images.
        """
        if self.debug:
            logging.debug(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Setting list of images")
            logging.warning(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Not implemented yet")


class CardFooter(QWidget):
    def __init__(
            self,
            debug: bool = False,
            content: Optional[QWidget] = None,
            parent=None):
        super(CardFooter, self).__init__(parent)

        self.debug = debug
        self.contentWidget = content

        self.initUI()

    def initUI(self):
        self.mainLayout = QHBoxLayout(self)
        self.setLayout(self.mainLayout)

        # set the separator
        sep = QFrame(self)
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFrameShadow(QFrame.Shadow.Sunken)
        self.mainLayout.addWidget(sep)

        # set the content
        if self.contentWidget is not None:
            self.setContent(self.contentWidget)

    def setContent(self, content: QWidget):
        self.mainLayout.addWidget(content)


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


class CardHeader(QWidget):
    def __init__(
            self,
            title: Optional[Union[str, QWidget]] = None,
            icon: Optional[QIcon] = None,
            debug: Optional[bool] = False,
            parent=None):
        super(CardHeader, self).__init__(parent)

        self.debug = debug
        self.title = title
        self.icon = icon

        self.initUI()

    def initUI(self):
        self.mainLayout = QHBoxLayout(self)
        self.setLayout(self.mainLayout)

        # set the title
        if (self.title or self.icon) is not None:
            self.setTitleUI(self.title, self.icon)
        else:
            logging.warning(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: No title or icon specified")

    def setTitleUI(self, title: Optional[Union[str, QWidget]] = None, icon: Optional[QIcon] = None):
        """Sets the title UI with a string or a widget."""
        if icon is not None:
            lbl = QLabel()
            lbl.setPixmap(icon.pixmap(24, 24))
            self.mainLayout.addWidget(lbl)

        if title is not None:
            if isinstance(title, str):
                lbl = QLabel(title)
                lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.mainLayout.addWidget(lbl)
            elif isinstance(title, QWidget):
                self.mainLayout.addWidget(title)

        self.mainLayout.addStretch(1)


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
