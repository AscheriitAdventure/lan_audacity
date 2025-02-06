from typing import Dict, Callable
from qtpy.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QListWidget
from qtpy.QtCore import Qt

def create_demo_widget(widget_type: str) -> QWidget:
    """Fonction utilitaire pour créer des widgets de démonstration"""
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    
    if widget_type == "tree":
        tree = QTreeWidget()
        layout.addWidget(tree)
    elif widget_type == "list":
        list_widget = QListWidget()
        layout.addWidget(list_widget)
    
    return widget

def demo_action(item) -> None:
    """Action de démonstration pour les événements"""
    print(f"Action triggered for: {item.text()}")

def demo_slot() -> None:
    """Slot de démonstration"""
    print("Slot triggered")

DEFAULT_SIDE_PANEL: Dict = {
    "stacked_title": "Démo Default",
    "separator": True,
    "shortcut": "Ctrl+D",
    "enable": True,
    "slot": demo_slot,
    "description": "Panneau de démonstration des fonctionnalités",
    "style": {
        "background": "#f5f5f5",
        "border": "1px solid #ddd",
        "padding": "5px"
    },
    "fields": [
        {
            "title": "Explorateur Simple",
            "form_list": "tree-file",
            "separator": True,
            "collapsed": False,
            "tooltip": "Explorateur de fichiers basique",
            "actions": [demo_action],
            "spacer": True,
            "description": "Permet de naviguer dans les fichiers",
            "visible": True,
            "slots": [demo_slot],
            "context_menu": True,
            "drag_drop": True,
            "selection_mode": "multi",
            "filters": ["*.txt", "*.py"],
            "sort_enabled": True,
            "custom_icons": {
                "folder": ":/icons/folder.png",
                "file": ":/icons/file.png"
            }
        },
        {
            "title": "Liste Interactive",
            "form_list": "list-btn",
            "separator": False,
            "collapsed": False,
            "tooltip": "Liste avec boutons d'action",
            "actions": [
                {"name": "add", "icon": "➕", "callback": demo_slot},
                {"name": "remove", "icon": "➖", "callback": demo_slot},
                {"name": "edit", "icon": "✏️", "callback": demo_slot}
            ],
            "buttons": [
                {
                    "text": "Rafraîchir",
                    "icon": "🔄",
                    "tooltip": "Actualiser la liste",
                    "shortcut": "F5",
                    "callback": demo_slot
                }
            ],
            "spacer": False,
            "description": "Liste avec boutons de contrôle",
            "visible": True,
            "slots": [demo_slot],
            "header_visible": True,
            "columns": ["Nom", "Type", "Taille"],
            "column_widths": [200, 100, 80],
            "context_menu_items": [
                {"text": "Copier", "shortcut": "Ctrl+C", "callback": demo_slot},
                {"text": "Coller", "shortcut": "Ctrl+V", "callback": demo_slot},
                "-",  # Séparateur
                {"text": "Supprimer", "shortcut": "Delete", "callback": demo_slot}
            ]
        },
        {
            "title": "Arbre Objets",
            "form_list": "tree-object",
            "separator": True,
            "collapsed": True,
            "tooltip": "Vue hiérarchique d'objets",
            "actions": [],
            "spacer": False,
            "description": "Affichage hiérarchique personnalisé",
            "visible": True,
            "slots": [],
            "custom_delegate": None,  # Pour personnaliser l'affichage
            "search_enabled": True,
            "search_placeholder": "Rechercher...",
            "auto_expand": False,
            "max_depth": 3,
            "style": {
                "alternate_background": "#f9f9f9",
                "selected_background": "#e3f2fd",
                "hover_background": "#f5f5f5"
            }
        },
        {
            "title": "Liste Avancée",
            "form_list": "list-object",
            "separator": False,
            "collapsed": False,
            "tooltip": "Liste d'objets avancée",
            "actions": [],
            "spacer": True,
            "description": "Liste avec fonctionnalités avancées",
            "visible": True,
            "slots": [],
            "features": {
                "filtering": True,
                "sorting": True,
                "grouping": True,
                "pagination": True,
                "items_per_page": 50
            },
            "toolbar": {
                "visible": True,
                "position": "top",
                "items": [
                    {"type": "search", "placeholder": "Rechercher..."},
                    {"type": "separator"},
                    {"type": "button", "text": "Exporter", "callback": demo_slot},
                    {"type": "combobox", "items": ["Vue 1", "Vue 2", "Vue 3"]}
                ]
            },
            "status_bar": {
                "visible": True,
                "elements": [
                    {"type": "count", "format": "{} éléments"},
                    {"type": "selection", "format": "{} sélectionné(s)"},
                    {"type": "custom", "widget": None}
                ]
            }
        }
    ]
}

FILES_EXPLORER: Dict = {}
LAN_EXPLORER: Dict = {}