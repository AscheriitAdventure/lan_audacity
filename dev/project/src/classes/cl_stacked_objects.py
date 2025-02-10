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
from typing import List, Dict, Any, Optional, Union, ClassVar
from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *
import logging
import inspect
import os

class TitleBlock(QWidget):
    """Widget pour le bloc de titre avec actions optionnelles"""
    def __init__(self, text: Union[str, QLabel], collapse_btn: Optional[QPushButton] = None, actions: Optional[List[Union[QPushButton, Dict]]] = None):
        super().__init__()
        self.setFixedHeight(25)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(2, 2, 2, 2)
        
        # Ajout du bouton collapse s'il existe
        if collapse_btn:
            self.layout.addWidget(collapse_btn)
        
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
                    btn = QPushButton()
                    if isinstance(action.get('icon'), str):
                        btn.setText(action.get('icon', ''))
                    elif isinstance(action.get('icon'), dict):
                        btn.setIcon(IconApp.from_dict(action.get('icon')).get_qIcon())
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
            btn = QPushButton()
            if isinstance(action.get('icon'), str):
                btn.setText(action.get('icon', ''))
            elif isinstance(action.get('icon'), dict):
                btn.setIcon(IconApp.from_dict(action.get('icon')).get_qIcon())
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

        # Création du bouton collapse        
        collapse_btn = QPushButton(IconApp("mdi6.chevron-double-right").get_qIcon(), "")
        collapse_btn.setFixedSize(20, 20)
        collapse_btn.setStyleSheet("QPushButton { border: none; }")
        
        # Récupération des actions du field pour les mettre dans la barre de titre
        actions = []
        if field.get("actions"):
            for action in field.get("actions", []):
                if isinstance(action, dict) and action.get('type') != 'callback':
                    actions.append(action)
        
        # Création du header avec TitleBlock incluant le collapse_btn et les actions
        header = TitleBlock(
            field.get("title", "").upper(),
            collapse_btn=collapse_btn,
            actions=actions
        )

        # Widget principal du field
        field_widget = self.create_specific_widget(field)
        field_layout = QVBoxLayout()                
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

        # Connexion des callbacks uniquement (pas les boutons)
        if field.get("actions"):
            for action in field["actions"]:
                if isinstance(action, dict) and action.get('type') == 'callback':
                    if isinstance(field_widget, QTreeWidget):
                        field_widget.itemClicked.connect(action['callback'])
                    elif isinstance(field_widget, QListWidget):
                        field_widget.itemClicked.connect(action['callback'])

        # Gestion du collapse
        def toggle_collapse():
            current_visible = field_widget.isVisible()
            field_widget.setVisible(not current_visible)
            collapse_btn.setIcon(IconApp("mdi6.chevron-double-right").get_qIcon() if current_visible else IconApp("mdi6.chevron-double-down").get_qIcon())
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

    def create_specific_widget(self, field: Dict[str, Any]) -> QWidget:
        """Crée le widget spécifique selon le form_list"""
        form_type = field.get('form_list')
        widget_data = field.get('widget_data')

        if form_type == 'tree-file':
            widget = QTreeWidget()
            widget.setHeaderLabels(['Fichiers'])
            widget.setRootIsDecorated(True)
            widget.setHeaderHidden(True)
            if widget_data and os.path.exists(widget_data):
                root_item = QTreeWidgetItem(widget, [os.path.basename(widget_data)])
                self.populate_file_tree(root_item, widget_data)
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
            widget = QTreeWidget()
            widget.setHeaderLabels(['Objets'])
            widget.setRootIsDecorated(True)
            widget.setHeaderHidden(True)
            if isinstance(widget_data, list):
                for item_data in widget_data:
                    self.add_tree_items(widget, item_data)
            return widget

        return QWidget()

    def add_tree_items(self, parent_widget, data: Dict[str, Any]) -> None:
        """Ajoute récursivement les items à l'arbre"""
        if isinstance(data, dict):
            item = QTreeWidgetItem([data.get('name', '')])
            if isinstance(parent_widget, QTreeWidget):
                parent_widget.addTopLevelItem(item)
            else:
                parent_widget.addChild(item)
        
            if 'childs' in data and isinstance(data['childs'], list):
                for child in data['childs']:
                    self.add_tree_items(item, child)
    
    def populate_file_tree(self, parent_item: QTreeWidgetItem, path: str) -> None:
        """Remplit récursivement l'arbre des fichiers"""
        try:
            # Trie les entrées : dossiers d'abord, puis fichiers
            entries = os.listdir(path)
            dirs = []
            files = []
        
            for entry in entries:
                full_path = os.path.join(path, entry)
                if os.path.isdir(full_path):
                    dirs.append(entry)
                else:
                    files.append(entry)
                
            # Ajoute les dossiers d'abord
            for dir_name in sorted(dirs):
                full_path = os.path.join(path, dir_name)
                dir_item = QTreeWidgetItem(parent_item, [dir_name])
                self.populate_file_tree(dir_item, full_path)
            
            # Puis ajoute les fichiers
            for file_name in sorted(files):
                file_item = QTreeWidgetItem(parent_item, [file_name])
            
        except PermissionError:
            error_item = QTreeWidgetItem(parent_item, ["Accès refusé"])
            error_item.setForeground(0, QBrush(Qt.red))
        except Exception as e:
            error_item = QTreeWidgetItem(parent_item, [str(e)])
            error_item.setForeground(0, QBrush(Qt.red))

    def update_field_state(self, title: str, **kwargs):
        """Met à jour l'état d'un field"""
        field = self.get_field(title)
        if field:
            field.update(kwargs)
            if "visible" in kwargs:
                # On doit mettre à jour à la fois le conteneur et le widget interne
                field["widget"].setVisible(kwargs["visible"])
                # Pour un tree widget, on doit s'assurer que son parent est aussi visible
                if isinstance(field["widget"].layout().itemAt(1).widget(), QTreeWidget):
                    field["widget"].layout().itemAt(1).widget().setVisible(kwargs["visible"])
            if "tooltip" in kwargs:
                field["widget"].setToolTip(kwargs["tooltip"])

            self.exchangeContext.emit({
                "action": "field_state_updated",
                "title": title,
                "updates": kwargs,
            })

    def get_field(self, title: str) -> Optional[Dict[str, Any]]:
        """Récupère toutes les informations d'un field par son titre"""
        return next(
            (field for field in self.active_fields if field["title"] == title),
            None,
        )

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
            visibility_btn = QPushButton(IconApp(names="fa5s.eye").get_qIcon(), "")
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

