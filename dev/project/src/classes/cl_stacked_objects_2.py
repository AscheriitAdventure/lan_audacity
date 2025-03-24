"""
    Remarques:
        A la suite de la création SDFOT(Stacked Dynamic Factory Object Tab), j'ai remarque qu'il fallait que je divise le code 
        de SDFSP(Stacked Dynamic Factory Side Panel), pour que je puisse réutiliser une grande partie du code de SDFSP dans SDFOT.
        Je vais donc créer SDFD(Stacked Dynamic Factory Data) qui va devenir la classe mère de SDFSP et SDFOT.
    Outils:
       - nom complet: Stacked Dynamic Factory Data
       - nom court: SDFD
       - Qtpy(Pyqt6)
       - logging
       - Python 3.12.1

    Réflexion pour load_stacked_widget:
        dict => {
            stacked_title: str,
            fields: List[Dict[str, Any]],
            separator: bool = False, 
            enable: bool = True, # enable = True => le stacked_widget est activé
            slot: Optional[str] = None, # slot = None => pas de slot
            shortcut: Optional[str] = None, # shortcut = None => pas de shortcut
        }
        field => {
            title: str,
            form_list: str,
            widget_data: Any, # <= l'ensemble des données de l'objet en alliance avec le form_list
            separator: bool = False, 
            collapsed: bool = False, # collapsed = True => le stacked_widget est caché
            tooltip: Optional[str] = None,
            actions: List[Union[QPushButton, Dict]],
            spacer: Optional[QWidget], # spacer = None => pas de spacer
            description: Optional[str] = None,
            visible: bool = True, # visible = True => le widget est visible
            slots: List[Callable] = [],
        }
"""

from dev.project.src.classes.cl_extented import IconApp
from dev.project.src.view.mvc_obj import TitleBlock
from typing import List, Dict, Any, Optional, ClassVar, Union
from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *
from enum import Enum
import logging
import inspect
import os


class SDFD(QWidget):
    """
        Stacked Dynamic Factory Data
    """
    class StackLayout(Enum):
        VERTICAL = 1
        HORIZONTAL = 2
        GRID = 3

    exchangeContext: ClassVar[Signal] = Signal(dict)
    itemDoubleClicked: ClassVar[Signal] = Signal(dict)
    itemSimpleClicked: ClassVar[Signal] = Signal(dict)

    def __init__(self, layout_field: 'SDFD.StackLayout' = StackLayout.VERTICAL, debug: bool = False, parent: Optional[QWidget] = None):
        super(SDFD, self).__init__(parent)

        self.debug = debug
        self.activeFields: List[Dict[str, Any]] = []

        self.stackLayout: SDFD.StackLayout = layout_field
        self.stackContextMenu: Optional[QWidget] = None
        self.stackFields: QStackedLayout = QStackedLayout()

        self.visibilityBtnEnabled: bool = False

    def initUI(self):
        # Main layout
        self.mainLayout = QVBoxLayout(self)
        self.setLayout(self.mainLayout)

        # Add Scroll Area
        self._updateFieldArea()

        # Add Custom Context Menu
        if self.stackContextMenu is not None:
            if self.debug:
                logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Adding custom context menu")
            self.setGlobalFieldLayout(self.StackLayout.GRID)
            self._loaddBtnContainer()
            self.scrollLayout.addLayout(self.stackFields, 0, 1, Qt.AlignmentFlag.AlignTop)

    def _updateFieldArea(self):
        """
        Détruit et Initialise la zone de défilement avec le layout approprié
        """
        # Destroy the current scroll area if it exists
        if hasattr(self, 'scrollArea'):
            if self.debug:
                logging.debug(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Destroying scroll area")
            self.scrollArea.setParent(None)
            self.scrollArea.deleteLater()

        # Build the scroll area
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.mainLayout.addWidget(self.scrollArea)

        # Créer le conteneur widget pour la zone de défilement
        self.scrollContainer = QWidget()
        self.scrollArea.setWidget(self.scrollContainer)

        # Initialiser le layout selon le type choisi
        if self.stackLayout == SDFD.StackLayout.VERTICAL:
            self.scrollLayout = QVBoxLayout(self.scrollContainer)
        elif self.stackLayout == SDFD.StackLayout.HORIZONTAL:
            self.scrollLayout = QHBoxLayout(self.scrollContainer)
        elif self.stackLayout == SDFD.StackLayout.GRID:
            self.scrollLayout = QGridLayout(self.scrollContainer)
        else:
            logging.warning(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: StackLayout {self.stackLayout} not found")
            self.scrollLayout = QVBoxLayout(self.scrollContainer)

        # Définir les marges du layout
        self.scrollLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollContainer.setLayout(self.scrollLayout)

    def setGlobalFieldLayout(self, field_layout: 'SDFD.StackLayout'):
        self.stackLayout = field_layout

        self._updateFieldArea()

    def _loaddBtnContainer(self):
        btnContainer = QWidget()
        self.scrollLayout.addWidget(
            btnContainer, 0, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        for field in self.activeFields:
            if field['enable']:
                btn = QPushButton("lol")
                btnContainer.addWidget(btn)

    def setStackContextMenu(self, context_menu: Any):
        self.stackContextMenu = context_menu

    def initDisplay(self, data: Dict[str, Any]):  # or loadStackData
        """Charge les données de stack spécifiées"""
        # Configuration du bouton de visibilité
        visbBtn = None
        if self.visibilityBtnEnabled and len(data.get('fields', [])) > 1:
            visbBtn = QPushButton(IconApp(names="fa5s.eye").get_qIcon(), "")
            visbBtn.setFixedSize(16, 16)
            visbBtn.setStyleSheet("QPushButton { border: none; }")
            visbBtn.clicked.connect(lambda: self._createVisibilityMenu()._exec(
                visbBtn.mapToGlobal(visbBtn.rect().bottomLeft())))

        # Création du bloc de titre
        ttlBlk = TitleBlock(text=data.get('stacked_title', 'Untitled'), actions=[
                            visbBtn] if visbBtn else None)

        if data.get('shortcut'):
            ttlBlk.title_label.setToolTip(
                f"{data.get('stacked_title', 'Untitled')} ({data['shortcut']})")

        self.scrollLayout.addWidget(ttlBlk)

        if data.get("separator", False):
            sep = QFrame()
            sep.setFrameShape(QFrame.Shape.HLine)
            sep.setFrameShadow(QFrame.Shadow.Sunken)
            self.scrollLayout.addWidget(sep)

        # Création du conteneur de fields
        fieldsContainer = QWidget()
        fieldsLayout = QVBoxLayout(fieldsContainer)
        fieldsLayout.setContentsMargins(0, 0, 0, 0)
        fieldsLayout.setSpacing(2)
        fieldsContainer.setLayout(fieldsLayout)

        for fd in data.get('fields', []):
            # Création du field
            fieldWidget = self._createFieldWidget(fd)
            fieldsLayout.addWidget(fieldWidget)

            # Ajout du field à la liste des fields actifs
            fds = {
                "title": fd["title"],
                "form_list": fd.get("form_list"),
                "visible": fd.get("visible", True),
                "collapsed": fd.get("collapsed", False),
                "stack_title": data.get("stacked_title"),
                "enabled": data.get("enable", True),
                "widget": fieldWidget,
                "actions": fd.get("actions", []),
                "tooltip": fd.get("tooltip"),
                "spacer": fd.get("spacer"),
                "description": fd.get("description"),
                "slots": fd.get("slots", []),
            }
            self.activeFields.append(fds)

        fieldsContainer.setVisible(data.get('enable', True))
        self.scrollLayout.addWidget(fieldsContainer)

        if data.get('shortcut'):
            shct = QShortcut(QKeySequence(data['shortcut']), self)
            shct.activated.connect(
                lambda: self._toggleStackVisibility(data['stacked_title']))

        self.exchangeContext.emit({
            "action": "stack_loaded",
            "title": data.get("stacked_title", "Untitled"),
            "enabled": data.get("enable", True),
        })

    def _createVisibilityMenu(self, fields: Dict[str, Any]) -> QMenu:
        visibilityMenu = QMenu(self)

        for field in fields:
            a = QAction(field.get('title'), visibilityMenu)
            a.setCheckable(True)
            fs = self.getActiveFields(field['title'])
            if fs:
                a.setChecked(fs.get('visible', True))

            def makeToggleFunc(ftitle: str):
                def toggleVisibility(checked: bool):
                    vf = sum(1 for f in self.activeFields if f.get(
                        "visible", True))
                    if not checked and vf <= 1:
                        a.setChecked(True)
                        return
                    self.updateFieldState(ftitle, visible=checked)
                return toggleVisibility
            a.triggered.connect(makeToggleFunc(field['title']))
            visibilityMenu.addAction(a)
        return visibilityMenu

    def getActiveFields(self, title: str) -> Optional[Dict[str, Any]]:
        """Récupère toutes les informations d'un field par son titre"""
        return next(
            (field for field in self.activeFields if field["title"] == title),
            None,
        )

    def updateFieldState(self, title: str, **kwargs):
        """Met à jour l'état d'un field"""
        f = self.getActiveFields(title)
        if f:
            f.update(kwargs)
            if "visible" in kwargs:
                f["widget"].setVisible(kwargs["visible"])
                if isinstance(f["widget"].layout().itemAt(1).widget(), QTreeWidget):
                    f["widget"].layout().itemAt(
                        1).widget().setVisible(kwargs["visible"])
            if "tooltip" in kwargs:
                f["widget"].setToolTip(kwargs["tooltip"])

            self.exchangeContext.emit({
                "action": "Field State Updated",
                "title": title,
                "update": kwargs,
            })

    def _createFieldWidget(self, field: Dict[str, Any]) -> QWidget:
        """Crée un widget basé sur le type de champ spécifié"""
        qtc = QWidget()
        qtl = QVBoxLayout(qtc)
        qtl.setContentsMargins(4, 0, 4, 0)
        qtl.setSpacing(1)
        qtc.setLayout(qtl)

        # Création du bouton collapse
        clpsBtn = QPushButton(
            IconApp("mdi6.chevron-double-right").get_qIcon(), "")
        clpsBtn.setFixedSize(20, 20)
        clpsBtn.setStyleSheet("QPushButton { border: none; }")

        # Récupération des actions pour le titre
        actions = []
        if field.get("actions"):
            for action in field.get("actions", []):
                if isinstance(action, dict) and action.get('type') != 'callback':
                    actions.append(action)

        # Création du header
        header = TitleBlock(text=field.get("title", "").upper(),
                            collapse_btn=clpsBtn, actions=actions)

        # Widget principal du field
        fieldWidget = self._createSpecificFieldWidget(field)
        fieldLayout = QVBoxLayout()
        fieldLayout.setContentsMargins(4, 4, 4, 4)
        fieldWidget.setLayout(fieldLayout)

        # Gestion de la visibilité
        isCollapsed = field.get("collapsed", False)
        isVisible = field.get("visible", True)

        # Ajout des widgets au container
        qtl.addWidget(header)

        if field.get("separator", False):
            sep = QFrame()
            sep.setFrameShape(QFrame.Shape.HLine)
            sep.setFrameShadow(QFrame.Shadow.Sunken)
            qtl.addWidget(sep)

        qtl.addWidget(fieldWidget)

        # Application des états de visibilité
        fieldWidget.setVisible(not isCollapsed and isVisible)
        qtc.setVisible(isVisible)

        if field.get("tooltip"):
            qtc.setToolTip(field["tooltip"])

        # Connexion des callbacks
        if field.get("actions"):
            for a in field.get("actions", []):
                if isinstance(a, dict) and a.get('type') == 'callback':
                    if isinstance(fieldWidget, QTreeWidget):
                        fieldWidget.itemClicked.connect(action['callback'])
                    elif isinstance(fieldWidget, QListWidget):
                        fieldWidget.itemClicked.connect(action['callback'])
                    elif isinstance(fieldWidget, QTreeView):
                        fieldWidget.clicked.connect(action['callback'])

        # Gestion du collapse
        def toggle_collapse():
            current_visible = fieldWidget.isVisible()
            fieldWidget.setVisible(not current_visible)
            clpsBtn.setIcon(
                IconApp("mdi6.chevron-double-right").get_qIcon()
                if current_visible
                else IconApp("mdi6.chevron-double-down").get_qIcon()
            )
            field["collapsed"] = current_visible
            self.exchangeContext.emit({
                "action": "field_collapsed",
                "title": field["title"],
                "collapsed": current_visible,
            })

        clpsBtn.clicked.connect(toggle_collapse)

        if field.get("spacer"):
            qtl.addSpacerItem(
                QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
                            QSizePolicy.Policy.Expanding)
            )

        return qtc

    def _toggleStackVisibility(self, title: str):
        """Bascule la visibilité d'un stack"""
        stf = [f for f in self.activeFields if f["stack_title"] == title]
        if stf:
            newVisible = not stf[0]['visible']
            for f in stf:
                f['visible'] = newVisible
                f['widget'].setVisible(newVisible and not f['collapsed'])

            self.exchangeContext.emit({
                "action": "stack_visibility_toggled",
                "title": title,
                "visible": newVisible,
            })

    def _createSpecificFieldWidget(self, field: Dict[str, Any]) -> QWidget:
        """Crée le widget spécifique selon le form_list"""
        return QWidget()


class SDFSP(SDFD):
    """
        Stacked Dynamic Factory Side Panel
    """
    fileDropped: ClassVar[Signal] = Signal(
        str, str)  # source_path, destination_path
    fileClicked: ClassVar[Signal] = Signal(str)  # path_clicked

    def __init__(self, debug: bool = False, parent: Optional[QWidget] = None):
        super(SDFSP, self).__init__(
            layout_field=SDFD.StackLayout.VERTICAL, debug=debug, parent=parent)

        self.initUI()

    def _createSpecificFieldWidget(self, field: Dict[str, Any]) -> QWidget:
        """Crée le widget spécifique selon le form_list"""
        form_type = field.get('form_list')
        widget_data = field.get('widget_data', os.getcwd())

        if form_type == 'tree-file':
            widget = QTreeView()
            if widget_data and os.path.exists(widget_data):
                model = QFileSystemModel()
                model.setRootPath(widget_data)
                model.setFilter(QDir.Filter.NoDotAndDotDot |
                                QDir.Filter.AllDirs | QDir.Filter.Files)
                widget.setModel(model)
                widget.setRootIndex(model.index(widget_data))

                # Configuration de base
                widget.setColumnHidden(1, True)  # Size
                widget.setColumnHidden(2, True)  # Type
                widget.setColumnHidden(3, True)  # Date Modified
                widget.setSortingEnabled(True)
                widget.sortByColumn(0, Qt.SortOrder.AscendingOrder)
                widget.setAnimated(True)
                widget.setIndentation(20)
                widget.setHeaderHidden(True)

                # Configuration drag & drop
                widget.setDragEnabled(True)
                widget.setAcceptDrops(True)
                widget.setDropIndicatorShown(True)
                widget.setDragDropMode(
                    QAbstractItemView.DragDropMode.InternalMove)
                widget.setSelectionMode(
                    QTreeView.SelectionMode.ExtendedSelection)

                # Connecter les signaux pour double-clic
                widget.doubleClicked.connect(lambda index: self.itemDoubleClicked.emit({
                    'type': 'file',
                    'path': model.filePath(index),
                    'is_dir': model.isDir(index)
                }))

                # Connecter les signaux pour drag & drop
                widget.model().rowsInserted.connect(
                    lambda parent, first, last: self.fileDropped.emit(
                        model.filePath(model.index(first, 0, parent)),
                        model.filePath(parent)
                    )
                )

            return widget

        elif form_type == 'list-btn':
            container = QWidget()
            layout = QVBoxLayout(container)
            list_widget = QListWidget()
            if isinstance(widget_data, list):
                list_widget.addItems(widget_data)
            layout.addWidget(list_widget)
            return container

        elif form_type == 'tree':
            widget = QTreeView()
            model = QStandardItemModel()
            widget.setModel(model)
            widget.setRootIsDecorated(True)
            widget.setHeaderHidden(True)
            model.setColumnCount(2)
            widget.setColumnHidden(1, True)
            widget.setEditTriggers(
                QAbstractItemView.EditTrigger.NoEditTriggers)
            if isinstance(widget_data, list):
                for item_data in widget_data:
                    self.add_tree_items(model.invisibleRootItem(), item_data)

            # Connecter le signal pour double-clic
            widget.doubleClicked.connect(lambda index: self.itemDoubleClicked.emit({
                'type': 'network',
                # filter on 'path'
                'path': index.sibling(index.row(), 1).data(),
                # filter on 'alias'
                'name': index.sibling(index.row(), 0).data(),
                'id': index.row()
            }))

            return widget
        return QWidget()

    def addTreeItems(self, parentItem, data: Dict[str, Any]) -> None:
        """Ajoute récursivement les items à l'arbre"""
        if isinstance(data, dict):
            item = QStandardItem(data.get('name', ''))
            if isinstance(parentItem, QStandardItem):
                parentItem.appendRow(item)
            else:
                parentItem.model().appendRow(item)
            if 'childs' in data and isinstance(data['childs'], list):
                for child in data['childs']:
                    self.addTreeItems(item, child)


class SDFOT(SDFD):
    """Stacked Dynamic Factory Object Tab"""

    def __init__(self, debug=False, parent=None):
        super(SDFOT, self).__init__(
            layout_field=SDFD.StackLayout.GRID, debug=debug, parent=parent)

        self.initUI()

    def _createSpecificFieldWidget(self, field: Dict[str, Any]) -> QWidget:
        """Crée le widget spécifique selon le form_list"""
        form_type = field.get('form_list', "")
        widget_data = field.get('widget_data', {})

        if form_type == "fmcg":  # Fixed Mosaics Cards Grid
            pass
        elif form_type == "dmcg":  # Dynamic Mosaics Cards Grid
            pass
        else:  # Default Ressource Form
            pass

        return QWidget()


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


# Extensions
class TitleWithActions(QWidget):
    def __init__(
            self, 
            title: Union[str, QLabel] = "No Title", 
            btn_actions: Optional[List[QPushButton]] = None, 
            debug: bool = False, 
            parent=None):
        """
        Widget avec titre et boutons d'action alignés horizontalement.
        
        Args:
            title: Texte du titre ou widget QLabel
            btn_actions: Liste des boutons d'action
            debug: Active le mode débogage
            parent: Widget parent
        """
        super(TitleWithActions, self).__init__(parent)

        self.debug = debug
        self._title = QLabel(self) if isinstance(title, str) else title
        self._list_btn_action = btn_actions if btn_actions is not None else []
                
        self.initUI()
        
        # Définir le titre si un string est passé
        if isinstance(title, str) and title:
            self.setTitle(title)
    
    def initUI(self):
        """Initialise l'interface utilisateur."""
        self.mainLayout = QHBoxLayout(self)
        self.setLayout(self.mainLayout)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        # Ajouter le titre
        self.mainLayout.addWidget(self._title)
        self._title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.mainLayout.addStretch(1)
        
        # Ajouter les boutons d'action
        if self._list_btn_action:
            self.addListBtnAction(self._list_btn_action)
    
    @property
    def btnActions(self) -> List[QPushButton]:
        """Retourne la liste des boutons d'action."""
        return self._list_btn_action
    
    def setTitle(self, title: Union[QLabel, str]) -> None:
        """
        Définit le titre du widget.
        
        Args:
            title: Texte du titre ou widget QLabel
        """
        try:
            if isinstance(title, QLabel):
                # Remplacer notre QLabel par celui fourni
                self.mainLayout.removeWidget(self._title)
                self._title = title
                self.mainLayout.insertWidget(0, self._title)
            elif isinstance(title, str):
                self._title.setText(title)
            else:
                if self.debug:
                    logging.warning(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: "
                                  f"Type non supporté: {type(title)}")
                return
                
            self._title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        except Exception as e:
            if self.debug:
                logging.error(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {str(e)}")
    
    def addBtnAction(self, btn: QPushButton) -> None:
        """
        Ajoute un bouton d'action.
        
        Args:
            btn: Bouton à ajouter
        """
        if not isinstance(btn, QPushButton):
            if self.debug:
                logging.warning(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: "
                              f"Type non supporté: {type(btn)}")
            return
            
        self._list_btn_action.append(btn)
        self.mainLayout.addWidget(btn)

    def addListBtnAction(self, list_btn: List[QPushButton]) -> None:
        """
        Ajoute une liste de boutons d'action.
        
        Args:
            list_btn: Liste des boutons à ajouter
        """
        if not list_btn:
            return
            
        for btn in list_btn:
            self.addBtnAction(btn)
            
    def clearActions(self) -> None:
        """Supprime tous les boutons d'action."""
        for btn in self._list_btn_action:
            self.mainLayout.removeWidget(btn)
            btn.setParent(None)
        
        self._list_btn_action.clear()

# Mosaïcs Cards
class FixedMosaicsCards(QWidget):
    cardsLoaded = Signal()  # Signal émis quand les cartes sont chargées
    progressChanged = Signal(int)  # Signal pour mettre à jour la progression
    workerFinished = Signal(object)  # Signal émis quand le worker a terminé, avec le résultat
    workerError = Signal(str)  # Signal émis en cas d'erreur

    def __init__(self, debug: bool = False, parent=None):
        super(FixedMosaicsCards, self).__init__(parent)
        
        self.debug = debug
        self._cards: List[Dict] = []  # Liste des cartes avec leur configuration
        self._title: Optional[Union[QLabel, str]] = None
        self.object_view: Optional[Any] = None
        
        self.worker: Optional[Any] = None
        self.progress_dialog: Optional[QDialog] = None
        self.thread_pool = QThreadPool()
        
        self.initUI()
        self._clearCardsLayout()
        
        self.cardsLoaded.connect(self.setCardsView)
        self.progressChanged.connect(self._updateProgressDialog)
        self.workerFinished.connect(self._handleWorkerFinished)
        self.workerError.connect(self._handleWorkerError)
        
        if len(self.cards) > 0:
            self.setCardsView()
    
    def initUI(self):
        self.mainLayout = QVBoxLayout(self)
        self.setLayout(self.mainLayout)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        
        ttlw = QWidget(self)        # Title Widget
        ttlwcnt = QVBoxLayout(ttlw) # Title Widget Container
        ttlwcnt.setContentsMargins(5, 5, 5, 0)  # Marge pour le titre
        self.mainLayout.addWidget(ttlw, alignment=Qt.AlignmentFlag.AlignTop)
        
        self.title_label = QLabel("Title", self) # Title Label
        self.title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        ttlwcnt.addWidget(self.title_label)
        ttlwcnt.addStretch(1)
        
        sep = QFrame(self)          # Separator
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFrameShadow(QFrame.Shadow.Sunken)
        self.mainLayout.addWidget(sep)
        
        self._loadScrollArea()
    
    def _loadScrollArea(self):
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.mainLayout.addWidget(self.scrollArea)
        
        self.scrollContainer = QWidget(self)
        self.scrollArea.setWidget(self.scrollContainer)
        self.scrollLayout = QGridLayout(self.scrollContainer)
        self.scrollLayout.setContentsMargins(0, 0, 0, 0)
    
    def setTitle(self, title_var:Union[QLabel, str]):
        self._title = title_var
        if isinstance(title_var, str):
            self.title_label.setText(title_var)
        elif isinstance(title_var, QLabel):
            index = self.mainLayout.indexOf(self.scrollArea) - 1
            if index >= 0:
                widget = self.mainLayout.itemAt(index).widget()
                if widget:
                    layout = widget.layout()
                    if layout and layout.count() > 0:
                        old_title = layout.itemAt(0).widget()
                        if old_title:
                            layout.replaceWidget(old_title, title_var)

    def _updateProgressDialog(self, value: int):
        """Met à jour la barre de progression si elle existe"""
        if self.progress_dialog and hasattr(self.progress_dialog, 'setValue'):
            self.progress_dialog.setValue(value)

    def _handleWorkerFinished(self, result: object):
        """Gère le résultat du worker une fois terminé"""
        if self.progress_dialog:
            self.progress_dialog.accept()
            self.progress_dialog = None
            
        if self.debug:
            logging.debug(f"Worker finished with result: {result}")

    def _handleWorkerError(self, error_msg: str):
        """Gère les erreurs du worker"""
        if self.progress_dialog:
            self.progress_dialog.reject()
            self.progress_dialog = None
            
        QMessageBox.critical(self, "Error", f"An error occurred: {error_msg}")
        if self.debug:
            logging.error(f"Worker error: {error_msg}")

    @property
    def progressDialog(self):
        return self.progress_dialog
    
    @progressDialog.setter
    def progressDialog(self, dialog: QDialog):
        self.progress_dialog = dialog
    
    @property
    def cards(self) -> List[Dict]:
        return self._cards
    
    @cards.setter
    def cards(self, cards_list: List[Dict]):
        """
            Les cards doivent avoir ce format:
            {
                "layout": {
                    "row": 0,   <-- int
                    "column": 0,<--- int
                    "rowSpan": None,<--- Optional[int]
                    "columnSpan": None, <--- Optional[int]
                    "alignment": None  <--- Optional[Qt.AlignmentFlag]
                },
                "top_card": QLabel("Hello World!"), <--- Optional[QWidget]
                "left_card": None,  <--- Optional[QWidget]
                "center_card": QLabel("Welcome!"),  <--- Optional[QWidget]
                "right_card": None, <--- Optional[QWidget]
                "bottom_card": QLabel("Bye!")   <--- Optional[QWidget]
            }
        """
        self._cards = cards_list
        
        if len(cards_list) > 0:
            self.cardsLoaded.emit()
        
    @property
    def objectView(self) -> Optional[Any]:
        return self.object_view
    
    @objectView.setter
    def objectView(self, view: Any):
        self.object_view = view
    
    @property
    def workerThread(self) -> Optional[Any]:
        return self.worker
    
    @workerThread.setter
    def workerThread(self, worker_thread: Any):
        self.worker = worker_thread
        if worker_thread:
            if hasattr(worker_thread, 'finished'):
                worker_thread.finished.connect(self._onWorkerFinished)
            if hasattr(worker_thread, 'error'):
                worker_thread.error.connect(self.workerError.emit)
            if hasattr(worker_thread, 'progress'):
                worker_thread.progress.connect(self.progressChanged.emit)
    
    def _onWorkerFinished(self):
        """Callback quand le worker a terminé"""
        if self.worker and hasattr(self.worker, 'result'):
            self.workerFinished.emit(self.worker.result)
        else:
            self.workerFinished.emit(None)
    
    def runWorker(self):
        """Lance le worker dans un thread séparé"""
        if not self.worker:
            return
        
        if hasattr(self.worker, 'setAutoDelete'):
            self.worker.setAutoDelete(True)
            
        self.thread_pool.start(self.worker)
    
    def _clearCardsLayout(self):
        """Clear all cards from the layout"""
        while self.scrollLayout.count():
            item = self.scrollLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                layout = item.layout()
                while layout.count():
                    sub_item = layout.takeAt(0)
                    if sub_item.widget():
                        sub_item.widget().deleteLater()
    
    def setCardsView(self):
        """Configure la vue des cartes basée sur les données de self.cards"""
        self._clearCardsLayout()
        
        for ecd in self.cards:  # Edit Card Data
            ls = ecd["layout"]  # Layout Settings
            kwargs = {
                "top": ecd.get("top_card"), 
                "left": ecd.get("left_card"), 
                "center": ecd.get("center_card"), 
                "right": ecd.get("right_card"), 
                "bottom": ecd.get("bottom_card")
            }

            c = Card(debug=self.debug, parent=self)
            c.setAllCards(**kwargs)
            
            if ls.get("rowSpan") is None or ls.get("columnSpan") is None:
                self.scrollLayout.addWidget(c, ls["row"], ls["column"])
            else:
                layout_params = {k: v for k, v in ls.items() if v is not None}
                self.scrollLayout.addWidget(c, **layout_params)
                
        self.scrollLayout.setRowStretch(self.scrollLayout.rowCount(), 1)
        self.scrollLayout.setColumnStretch(self.scrollLayout.columnCount(), 1)
