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
            title: str,
            form_list: str, # "tree", "list-btn", "list", "tree-file"
            widget: QWidget,
            widget_layout: QVBoxLayout,
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

from typing import List, Dict, Any, Optional, Union, ClassVar
from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *
import logging
import inspect

class TitleBlock(QWidget):
    """Widget pour le bloc de titre avec actions optionnelles"""
    def __init__(self, text: Union[str, QLabel], actions: Optional[List[Union[QPushButton, Dict]]] = None):
        super().__init__()
        self.setFixedHeight(25)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(2, 2, 2, 2)
        
        # Gestion du titre
        if isinstance(text, str):
            self.title_label = QLabel(text.upper())
        else:
            self.title_label = text
        self.title_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.layout.addWidget(self.title_label)
        self.layout.addStretch()
        
        # Ajout des actions
        if actions:
            for action in actions:
                if isinstance(action, QPushButton):
                    self.layout.addWidget(action)
                elif isinstance(action, dict):
                    btn = QPushButton(action.get('icon', ''))
                    btn.setFixedSize(16, 16)
                    btn.setStyleSheet("QPushButton { border: none; }")
                    if 'callback' in action:
                        btn.clicked.connect(action['callback'])
                    if 'tooltip' in action:
                        btn.setToolTip(action['tooltip'])
                    self.layout.addWidget(btn)

    def set_title(self, text: str):
        """Met à jour le texte du titre"""
        self.title_label.setText(text.upper())

    def add_action(self, action: Union[QPushButton, Dict]):
        """Ajoute une action au bloc de titre"""
        if isinstance(action, QPushButton):
            self.layout.addWidget(action)
        elif isinstance(action, dict):
            btn = QPushButton(action.get('icon', ''))
            btn.setFixedSize(16, 16)
            btn.setStyleSheet("QPushButton { border: none; }")
            if 'callback' in action:
                btn.clicked.connect(action['callback'])
            if 'tooltip' in action:
                btn.setToolTip(action['tooltip'])
            self.layout.addWidget(btn)

class SDFSP(QWidget):
    exchangeContext: ClassVar[Signal] = Signal(dict)
    
    def __init__(self, debug: bool = False, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.debug: bool = debug
        self.active_fields: List[Dict[str, Any]] = []
        self.link_tab: Optional[QTabWidget] = None
        self.loadUI()

    def loadUI(self):
        """Initialise l'interface utilisateur principale"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(2)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

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
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Creating field widget for {field.get('title')}"
            )

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(4, 0, 4, 0)
        container_layout.setSpacing(1)

        # Création du header avec TitleBlock
        collapse_btn = QPushButton("↓")
        collapse_btn.setFixedSize(20, 20)
        collapse_btn.setStyleSheet("QPushButton { border: none; }")
        
        header = TitleBlock(
            field.get("title", "").upper(),
            actions=[collapse_btn]
        )

        # Widget principal du field
        field_widget = field.get("widget", QWidget())
        field_layout = field.get("widget_layout", QVBoxLayout())
        field_layout.setContentsMargins(4, 4, 4, 4)
        field_widget.setLayout(field_layout)

        # Gestion de la visibilité initiale
        is_collapsed = field.get("collapsed", False)
        is_visible = field.get("visible", True)
        
        container_layout.addWidget(header)

        if field.get("separator", False):
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Sunken)
            container_layout.addWidget(separator)

        container_layout.addWidget(field_widget)
        
        # Application des états de visibilité
        field_widget.setVisible(not is_collapsed and is_visible)
        container.setVisible(is_visible)

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
            current_visible = field_widget.isVisible()
            field_widget.setVisible(not current_visible)
            collapse_btn.setText("→" if current_visible else "↓")
            field["collapsed"] = current_visible
            self.exchangeContext.emit({
                "action": "field_collapsed",
                "title": field["title"],
                "collapsed": current_visible,
            })

        collapse_btn.clicked.connect(toggle_collapse)

        if field.get("spacer"):
            container_layout.addSpacerItem(
                QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            )

        return container

    def load_stack_data(self, data: Dict[str, Any]):
        """Charge les données de stack spécifiées"""
        if self.debug:
            logging.info(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Loading stack data")

        # Création du menu de visibilité
        def create_visibility_menu():
            menu = QMenu(self)
            for field in data.get("fields", []):
                action = QAction(field.get("title"), menu)
                action.setCheckable(True)
                field_state = self.get_field(field["title"])
                if field_state:
                    action.setChecked(field_state.get("visible", True))
                
                def make_toggle_func(ftitle):
                    def toggle_visibility(checked):
                        visible_fields = sum(1 for f in self.active_fields if f.get("visible", True))
                        if not checked and visible_fields <= 1:
                            action.setChecked(True)
                            return
                        self.update_field_state(ftitle, visible=checked)
                    return toggle_visibility
                
                action.triggered.connect(make_toggle_func(field["title"]))
                menu.addAction(action)
            return menu

        # Configuration du bouton de visibilité
        visibility_btn = None
        if len(data.get("fields", [])) > 1:
            visibility_btn = QPushButton("👁")
            visibility_btn.setFixedSize(16, 16)
            visibility_btn.setStyleSheet("QPushButton { border: none; }")
            visibility_btn.clicked.connect(
                lambda: create_visibility_menu().exec_(
                    visibility_btn.mapToGlobal(visibility_btn.rect().bottomLeft())
                )
            )

        # Création du bloc de titre
        title_actions = [visibility_btn] if visibility_btn else None
        title_block = TitleBlock(
            text=data.get("stacked_title", "Untitled"),
            actions=title_actions
        )
        
        if data.get("shortcut"):
            title_block.title_label.setToolTip(
                f"{data.get('stacked_title', 'Untitled')} ({data['shortcut']})"
            )

        self.content_layout.addWidget(title_block)

        # Ajout du séparateur si nécessaire
        if data.get("separator", False):
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Sunken)
            self.content_layout.addWidget(separator)

        # Création du conteneur de fields
        fields_container = QWidget()
        fields_layout = QVBoxLayout(fields_container)
        fields_layout.setContentsMargins(0, 0, 0, 0)
        fields_layout.setSpacing(2)

        for field in data.get("fields", []):
            field_widget = self.create_field_widget(field)
            fields_layout.addWidget(field_widget)

            field_state = {
                "title": field["title"],
                "form_list": field.get("form_list"),
                "visible": field.get("visible", True),
                "collapsed": field.get("collapsed", False),
                "stack_title": data.get("stacked_title"),
                "enabled": data.get("enable", True),
                "widget": field_widget,
                "actions": field.get("actions", []),
                "tooltip": field.get("tooltip"),
                "spacer": field.get("spacer"),
                "description": field.get("description"),
                "slots": field.get("slots", []),
            }
            self.active_fields.append(field_state)

        fields_container.setVisible(data.get("enable", True))
        self.content_layout.addWidget(fields_container)

        if data.get("shortcut"):
            shortcut = QShortcut(QKeySequence(data["shortcut"]), self)
            shortcut.activated.connect(
                lambda: self.toggle_stack_visibility(data["stacked_title"])
            )

        self.exchangeContext.emit({
            "action": "stack_loaded",
            "title": data["stacked_title"],
            "enabled": data.get("enable", True),
        })

    def get_field(self, title: str) -> Optional[Dict[str, Any]]:
        """Récupère toutes les informations d'un field par son titre"""
        return next(
            (field for field in self.active_fields if field["title"] == title),
            None,
        )

    def update_field_state(self, title: str, **kwargs):
        """Met à jour l'état d'un field"""
        field = self.get_field(title)
        if field:
            field.update(kwargs)
            if "visible" in kwargs:
                field["widget"].setVisible(kwargs["visible"] and not field["collapsed"])
            if "tooltip" in kwargs:
                field["widget"].setToolTip(kwargs["tooltip"])

            self.exchangeContext.emit({
                "action": "field_state_updated",
                "title": title,
                "updates": kwargs,
            })

    def toggle_stack_visibility(self, stack_title: str):
        """Bascule la visibilité d'un stack"""
        stack_fields = [
            field for field in self.active_fields 
            if field["stack_title"] == stack_title
        ]
        if stack_fields:
            new_visible = not stack_fields[0]["visible"]
            for field in stack_fields:
                field["visible"] = new_visible
                field["widget"].setVisible(new_visible and not field["collapsed"])

            self.exchangeContext.emit({
                "action": "stack_visibility_changed",
                "title": stack_title,
                "visible": new_visible,
            })

