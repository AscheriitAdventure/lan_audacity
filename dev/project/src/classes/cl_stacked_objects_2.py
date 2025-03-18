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
from typing import List, Dict, Any, Optional, ClassVar
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

    def __init__(self, layout_field: 'SDFD.StackLayout' = StackLayout.VERTICAL, debug: bool = False, parent: Optional[QWidget] = None):
        super(SDFD, self).__init__(parent)

        self.debug = debug
        self.activeFields: List[Dict[str, Any]] = []

        self.stackLayout: SDFD.StackLayout = layout_field
        self.stackContextMenu: Optional[QWidget] = None
        self.stackFields: QStackedLayout = QStackedLayout()

        self.visibilityBtnEnabled: bool = False

    def setupClass(self):
        pass

    def initUI(self):
        # Main layout
        self.mainLayout = QVBoxLayout(self)
        self.setLayout(self.mainLayout)

        # Add Scroll Area
        self._updateFieldArea()

        # Add Custom Context Menu
        if self.stackContextMenu is not None:
            if self.debug:
                logging.debug(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Adding custom context menu")
            self.setGlobalFieldLayout(self.StackLayout.GRID)
            self._loaddBtnContainer()
            self.scrollLayout.addLayout(
                self.stackFields, 0, 1, Qt.AlignmentFlag.AlignTop)

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
            visbBtn.clicked.connect(lambda: self._createVisibilityMenu()._exec(visbBtn.mapToGlobal(visbBtn.rect().bottomLeft())))

        # Création du bloc de titre
        ttlBlk = TitleBlock(text=data.get('stacked_title', 'Untitled'), actions=[visbBtn] if visbBtn else None)

        if data.get('shortcut'):
            ttlBlk.title_label.setToolTip(f"{data.get('stacked_title', 'Untitled')} ({data['shortcut']})")
        
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
            shct.activated.connect(lambda: self._toggleStackVisibility(data['stacked_title']))
        
        self.exchangeContext.emit({
            "action": "stack_loaded",
            "title": data["stacked_title"],
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
        clpsBtn = QPushButton(IconApp("mdi6.chevron-double-right").get_qIcon(), "")
        clpsBtn.setFixedSize(20, 20)
        clpsBtn.setStyleSheet("QPushButton { border: none; }")

        # Récupération des actions pour le titre
        actions = []
        if field.get("actions"):
            for action in field.get("actions", []):
                if isinstance(action, dict) and action.get('type') != 'callback':
                    actions.append(action)
        
        # Création du header
        header = TitleBlock(text=field.get("title", "").upper(), collapse_btn=clpsBtn, actions=actions)

        # Widget principal du field
        fieldWidget = self._createSpecificFieldWidget(field)
        fieldLayout = QVBoxLayout()
        fieldLayout.setContentsMargins(4,4,4,4)
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
                QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
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
    fileDropped: ClassVar[Signal] = Signal(str, str)  # source_path, destination_path
    fileClicked: ClassVar[Signal] = Signal(str)  # path_clicked

    def __init__(self, debug: bool = False, parent: Optional[QWidget] = None):
        super(SDFSP, self).__init__(layout_field=SDFD.StackLayout.VERTICAL, debug=debug, parent=parent)

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
                model.setFilter(QDir.Filter.NoDotAndDotDot | QDir.Filter.AllDirs | QDir.Filter.Files)
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
                widget.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
                widget.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)
                
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
            widget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            if isinstance(widget_data, list):
                for item_data in widget_data:
                    self.add_tree_items(model.invisibleRootItem(), item_data)
            
            # Connecter le signal pour double-clic
            widget.doubleClicked.connect(lambda index: self.itemDoubleClicked.emit({
                'type': 'network',
                'path': index.sibling(index.row(), 1).data(), # filter on 'path'
                'name': index.sibling(index.row(), 0).data(), # filter on 'alias'
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

    def __init__(self, debug = False, parent = None):
        super(SDFOT, self).__init__(layout_field=SDFD.StackLayout.GRID, debug=debug, parent=parent)

        self.initUI()
        
    def _createSpecificFieldWidget(self, field: Dict[str, Any]) -> QWidget:
        """Crée le widget spécifique selon le form_list"""
        form_type = field.get('form_list', "")
        widget_data = field.get('widget_data', {})

        if form_type == "fmcg": # Fixed Mosaics Cards Grid
            pass
        elif form_type == "dmcg": # Dynamic Mosaics Cards Grid
            pass
        else: # Default Ressource Form
            pass

        return QWidget()