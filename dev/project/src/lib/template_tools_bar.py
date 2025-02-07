from typing import Dict, Callable
import os


DEFAULT_SIDE_PANEL: Dict = {
    "stacked_title": "Démo Default",
    "separator": True,
    "shortcut": "Ctrl+D",
    "enable": True,
    "fields": [
        {
            "title": "Explorateur Fichiers",
            "form_list": "tree-file",
            "separator": True,
            "collapsed": False,
            "tooltip": "Explorateur de fichiers",
            "actions": [],
            "spacer": False,
            "description": "Navigation dans les fichiers",
            "visible": False,
            "slots": []
        },
        {
            "title": "Arbre Objets",
            "form_list": "tree",
            "separator": True,
            "collapsed": True,
            "tooltip": "Vue en arbre",
            "actions": [],
            "spacer": False,
            "description": "Affichage hiérarchique",
            "visible": True,
            "slots": []
        },
        {
            "title": "Liste Simple",
            "form_list": "list-btn",
            "separator": False,
            "collapsed": True,
            "tooltip": "Liste d'éléments",
            "actions": [],
            "spacer": False,
            "description": "Liste d'éléments simples",
            "visible": True,
            "slots": []
        },
        {
            "title": "Explorateur Dossiers",
            "form_list": "tree-file",
            "separator": True,
            "collapsed": False,
            "tooltip": "Explorateur de fichiers",
            "actions": [],
            "spacer": False,
            "description": "Navigation dans les fichiers",
            "visible": True,
            "slots": []
        },
    ]
}

# Templates à implémenter
FILES_EXPLORER: Dict = {
    "title": "Explorateur Fichiers",
    "separator": True,
    "shortcut": "Ctrl+Shift+E",
    "enable": True,
    "fields": [
        {
            "title": "Editeur Ouvert",
            "form_list": "list-btn",
            "separator": True,
            "collapsed": False,
            "tooltip": "Liste des fichiers textes ouverts",
            "actions": [], # Penser à ajouter les actions
            "description": "Liste des onglets de type editeur ouverts",
            "visible": False
        },
        {
            "title": os.path.basename(os.getcwd()), # Nom du dossier implémenter
            "form_list": "tree-file",
            "separator": True,
            "collapsed": False,
            "tooltip": f"Explorateur de fichiers de {os.path.basename(os.getcwd())}",
            "actions": [], # Penser à ajouter les actions
            "description": "Navigation dans les fichiers",
            "visible": True
        }
    ]
}
LAN_EXPLORER: Dict = {}