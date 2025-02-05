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
            stacked_widget: QWidget, 
            widget_layout: QVBoxLayout,
            enable: bool = True, # enable = True => le stacked_widget est activé
            slot: Optional[str] = None, # slot = None => pas de slot
            tooltip: Optional[str] = None, # tooltip = None => pas de tooltip
            shortcut: Optional[str] = None, # shortcut = None => pas de shortcut
        }
        field => {
            field_name: str,
            field_type: str, # "tree", "list-btn", "list", "tree-file"
            widget: QWidget,
            widget_layout: QVBoxLayout,
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

    exchangeContext: ClassVar[Signal] = Signal(dict)  # Signal pour échanger des informations 

    def __init__(self, debug: bool = False, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.debug: bool = debug
        self.active_fields: List = []
        self.link_tab: Optional[QTabWidget] = None
        self.field_widgets: Dict[str, Dict[str, Any]] = {}  # Stocke les widgets par nom de field
        
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

    def create_field_widget(self, field: Dict[str, Any]) -> Dict[str, Any]:
        """Crée un widget basé sur le type de champ spécifié"""
        field_type = field.get('field_type', '')
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(1)
        
        # Création du header avec titre et bouton collapse si description fournie
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(2, 2, 2, 2)
        
        # Titre du field
        title_label = QLabel(field.get('field_name', 'Untitled'))
        header_layout.addWidget(title_label)
        
        # Bouton collapse si une description est fournie
        collapse_btn = None
        if field.get('field_description'):
            collapse_btn = QPushButton('▼' if not field.get('collapsed', False) else '▶')
            collapse_btn.setFixedSize(20, 20)
            collapse_btn.setStyleSheet("QPushButton { border: none; }")
            header_layout.addWidget(collapse_btn)
        
        header_layout.addStretch()
        container_layout.addWidget(header_widget)
        
        # Création du widget principal selon le type
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(4, 0, 4, 0)
        
        if field_type == "tree":
            tree = QTreeWidget()
            content_layout.addWidget(tree)
            if field.get('actions'):
                for action in field['actions']:
                    if callable(action):
                        tree.itemClicked.connect(action)
                        
        elif field_type == "list-btn":
            list_widget = QListWidget()
            button_widget = QPushButton(field.get('field_name', 'Button'))
            content_layout.addWidget(list_widget)
            content_layout.addWidget(button_widget)
            
        elif field_type == "list":
            list_widget = QListWidget()
            content_layout.addWidget(list_widget)
            
        elif field_type == "tree-file":
            file_tree = QTreeWidget()
            file_tree.setHeaderLabels(["Files"])
            content_layout.addWidget(file_tree)
        
        container_layout.addWidget(content_widget)
        
        # Ajout du spacer si spécifié
        if field.get('spacer'):
            container_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
            
        # Configuration de la visibilité initiale
        if field.get('collapsed', False):
            content_widget.hide()
            
        # Ajout du tooltip si spécifié
        if field.get('tooltip'):
            container.setToolTip(field['tooltip'])
            
        # Configuration du collapse button
        if collapse_btn:
            def toggle_collapse():
                is_visible = content_widget.isVisible()
                content_widget.setVisible(not is_visible)
                collapse_btn.setText('▼' if not is_visible else '▶')
                self.exchangeContext.emit({
                    'action': 'field_collapsed',
                    'field_name': field['field_name'],
                    'collapsed': is_visible
                })
            
            collapse_btn.clicked.connect(toggle_collapse)
        
        return {
            'container': container,
            'content_widget': content_widget,
            'collapse_btn': collapse_btn
        }

    def load_fields(self, fields: List[Dict[str, Any]]):
        """Charge tous les champs spécifiés"""
        for field_data in fields:
            if self.debug:
                logging.debug(f"Loading field: {field_data.get('field_name', 'Unknown')}")
            
            # Création des widgets pour ce field
            field_widgets = self.create_field_widget(field_data)
            
            # Stockage des références des widgets
            field_name = field_data['field_name']
            self.field_widgets[field_name] = field_widgets
            
            # Ajout au layout principal
            self.content_layout.addWidget(field_widgets['container'])
            
            if field_data.get('enable', True):
                self.active_fields.append(field_name)
        
        # Ajout d'un spacer à la fin pour pousser tous les widgets vers le haut
        self.content_layout.addStretch()

    def set_field_collapsed(self, field_name: str, collapsed: bool):
        """Change l'état de collapse d'un field spécifique"""
        if field_name in self.field_widgets:
            widgets = self.field_widgets[field_name]
            widgets['content_widget'].setVisible(not collapsed)
            if widgets['collapse_btn']:
                widgets['collapse_btn'].setText('▶' if collapsed else '▼')
            
            if self.debug:
                logging.debug(f"Set field {field_name} collapsed: {collapsed}")

    def set_link_tab(self, tab_widget: QTabWidget):
        """Définit un onglet de lien pour les actions"""
        self.link_tab = tab_widget
