"""
    Remarques:
        Suite à la création de la classe GeneralSidePanel, nous avons pu créer différentes classes filles.
        Mais avec une vision d'évolution, cette classe est devenue embêtante à maintenir.
        Donc nous allons améliorer cette classe pour permettre une meilleure possibilité d'évolution.
        Pour cela nous allons créer une classe dynamique ou de type "Factory" qui va s'occuper de toute la partie GUI.
    Outils:
       - nom complet: Stacked Dynamic Factory Side Panel
       - nom court: SDFSP
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
            field_name: str,
            field_type: str, # "tree", "list-btn", "list", "tree-file"
            widget: QWidget,
            widget_layout: QVBoxLayout,
            visible: bool = True, # visible = True => le widget est visible
            slot: List[Callable] = [],
            tooltip: Optional[str] = None,
            actions: List[Callable],
            spacer: Optional[QWidget], # spacer = None => pas de spacer
            collapsed: bool = False, # collapsed = True => le stacked_widget est caché
            field_description: Optional[str] = None,
        }
"""

from typing import List, Dict, Any, Optional, Union, ClassVar
import logging
import inspect

from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *


class SDFSP(QWidget):

    exchangeContext: ClassVar[Signal] = Signal(
        dict
    )  # Signal pour échanger des informations
    
    def __init__(self, debug: bool = False, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.debug: bool = debug
        self.active_fields: List[Dict[str, Any]] = (
            []
        )  # Structure unique pour stocker l'état des fields
        self.link_tab: Optional[QTabWidget] = None

        self.loadUI()

    def loadUI(self):
        """Initialise l'interface utilisateur principale"""
        # Layout principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(2)

        # Scroll Area pour gérer le défilement si nécessaire
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Widget conteneur pour les fields
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(2, 2, 2, 2)
        self.content_layout.setSpacing(2)

        self.scroll_area.setWidget(self.content_widget)
        self.main_layout.addWidget(self.scroll_area)

        if self.debug:
            logging.debug("UI initialized")

    def create_field_widget(self, field: Dict[str, Any]) -> QWidget:
        """Crée un widget basé sur le type de champ spécifié"""
        if self.debug:
            logging.debug(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Creating field widget for {field.get('field_name')}"
            )

        # Création du conteneur principal pour le field
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(4, 0, 4, 0)
        container_layout.setSpacing(1)

        # Création du header avec titre et bouton collapse
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 2, 0, 2)

        # Bouton collapse
        collapse_btn = QPushButton("↓")
        collapse_btn.setFixedSize(20, 20)
        collapse_btn.setStyleSheet("QPushButton { border: none; }")

        # Label du field
        title = QLabel(field.get("field_name", "").upper())

        header_layout.addWidget(collapse_btn)
        header_layout.addWidget(title)
        header_layout.addStretch()

        # Widget principal du field
        field_widget = field.get("widget", QWidget())
        field_layout = field.get("widget_layout", QVBoxLayout())
        field_layout.setContentsMargins(4, 4, 4, 4)
        field_widget.setLayout(field_layout)

        # Ajout des widgets au conteneur
        container_layout.addWidget(header)

        # Ajout d'un séparateur si demandé
        if field.get("separator", False):
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Sunken)
            container_layout.addWidget(separator)

        container_layout.addWidget(field_widget)

        # Configuration de la visibilité et du tooltip
        field_widget.setVisible(not field.get("collapsed", False))
        if field.get("tooltip"):
            container.setToolTip(field["tooltip"])

        # Connexion des actions
        if field.get("actions"):
            for action in field["actions"]:
                if callable(action):
                    if isinstance(field_widget, QTreeWidget):
                        field_widget.itemClicked.connect(action)
                    elif isinstance(field_widget, QListWidget):
                        field_widget.itemClicked.connect(action)

        # Gestion du collapse
        def toggle_collapse():
            is_visible = field_widget.isVisible()
            field_widget.setVisible(not is_visible)
            collapse_btn.setText("→" if is_visible else "↓")
            self.exchangeContext.emit(
                {
                    "action": "field_collapsed",
                    "field_name": field["field_name"],
                    "collapsed": is_visible,
                }
            )

        collapse_btn.clicked.connect(toggle_collapse)

        # Ajout du spacer si spécifié
        if field.get("spacer"):
            container_layout.addSpacerItem(
                QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            )

        return container

    def load_stack_data(self, data: Dict[str, Any]):
        """Charge les données de stack spécifiées"""
        if self.debug:
            logging.info(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Loading stack data")

        title_block = QWidget(self)
        title_block.setFixedHeight(25)
        title_layout = QHBoxLayout(title_block)
        title_layout.setContentsMargins(2, 2, 2, 2)

        title_label = QLabel(data.get("stacked_title", "Untitled").upper())
        shortcut_text = f" ({data['shortcut']})" if data.get("shortcut") else ""
        title_label.setToolTip(f"{data.get('stacked_title', 'Untitled')}{shortcut_text}")
        title_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        title_layout.addWidget(title_label)
        title_layout.addStretch()

        # Ajout du bouton de visibilité si plus d'un field
        fields = data.get("fields", [])
        if len(fields) > 1:
            visibility_btn = QPushButton("👁")
            visibility_btn.setFixedSize(16, 16)
            visibility_btn.setStyleSheet("QPushButton { border: none; }")
        
            def show_visibility_menu():
                menu = QMenu(self)
                visible_count = sum(1 for f in self.active_fields if f.get("visible", True))
                for field in fields:
                    field_name = field.get("field_name")
                    action = QAction(field_name, menu)
                    action.setCheckable(True)
                    field_state = self.get_field(field_name)
                    if field_state:
                        action.setChecked(field_state.get("visible", True))

                    def make_toggle_func(fname):
                        def toggle_visibility(checked):
                            visible_fields = sum(1 for f in self.active_fields if f.get("visible", True))
                            if not checked and visible_fields <= 1:
                                action.setChecked(True)
                                return
                            self.update_field_state(fname, visible=checked)
                        return toggle_visibility
                    
                    action.triggered.connect(make_toggle_func(field_name))
                    menu.addAction(action)
            
                menu.exec_(visibility_btn.mapToGlobal(visibility_btn.rect().bottomLeft()))
            
            visibility_btn.clicked.connect(show_visibility_menu)
            title_layout.addWidget(visibility_btn)

        self.content_layout.addWidget(title_block)

        if data.get("separator", False):
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Sunken)
            self.content_layout.addWidget(separator)

        fields_container = QWidget()
        fields_layout = QVBoxLayout(fields_container)
        fields_layout.setContentsMargins(0, 0, 0, 0)
        fields_layout.setSpacing(2)

        for field in fields:
            field_widget = self.create_field_widget(field)
            fields_layout.addWidget(field_widget)

            field_state = {
                "field_name": field["field_name"],
                "field_type": field.get("field_type"),
                "visible": field.get("visible", True),
                "collapsed": field.get("collapsed", False),
                "stack_title": data.get("stacked_title"),
                "enabled": data.get("enable", True),
                "widget": field_widget,
                "actions": field.get("actions", []),
                "tooltip": field.get("tooltip"),
                "spacer": field.get("spacer"),
                "field_description": field.get("field_description"),
                "slots": field.get("slots", []),
            }
            self.active_fields.append(field_state)

        fields_container.setVisible(data.get("enable", True))
        self.content_layout.addWidget(fields_container)

        if data.get("shortcut"):
            shortcut = QShortcut(QKeySequence(data["shortcut"]), self)
            shortcut.activated.connect(lambda: self.toggle_stack_visibility(data["stacked_title"]))

        self.exchangeContext.emit({
            "action": "stack_loaded",
            "title": data["stacked_title"],
            "enabled": data.get("enable", True),
        })

    def get_field(self, field_name: str) -> Optional[Dict[str, Any]]:
        """Récupère toutes les informations d'un field par son nom"""
        return next(
            (
                field
                for field in self.active_fields
                if field["field_name"] == field_name
            ),
            None,
        )

    def update_field_state(self, field_name: str, **kwargs):
        """Met à jour l'état d'un field"""
        field = self.get_field(field_name)
        if field:
            field.update(kwargs)
            # Mise à jour du widget si nécessaire
            if "visible" in kwargs:
                field["widget"].setVisible(kwargs["visible"])
            if "tooltip" in kwargs:
                field["widget"].setToolTip(kwargs["tooltip"])

            self.exchangeContext.emit(
                {
                    "action": "field_state_updated",
                    "field_name": field_name,
                    "updates": kwargs,
                }
            )

    def toggle_stack_visibility(self, stack_title: str):
        """Bascule la visibilité d'un stack"""
        stack_fields = [
            field for field in self.active_fields if field["stack_title"] == stack_title
        ]
        if stack_fields:
            new_visible = not stack_fields[0]["visible"]
            for field in stack_fields:
                field["visible"] = new_visible
                field["widget"].setVisible(new_visible)

            self.exchangeContext.emit(
                {
                    "action": "stack_visibility_changed",
                    "title": stack_title,
                    "visible": new_visible,
                }
            )
