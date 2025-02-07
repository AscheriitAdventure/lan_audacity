from typing import Dict, Callable
import os
from dev.project.src.classes.cl_extented import IconApp


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
            "actions": [],  # Penser à ajouter les actions
            "description": "Liste des onglets de type editeur ouverts",
            "visible": False
        },
        {
            # Nom du dossier implémenter
            "title": os.path.basename(os.getcwd()),
            "form_list": "tree-file",
            "separator": True,
            "collapsed": False,
            "tooltip": f"Explorateur de fichiers de {os.path.basename(os.getcwd())}",
            "actions": [
                {
                    'icon': IconApp(names=[
                        "mdi6.file-outline",
                        "mdi6.circle",
                        "fa5s.plus-circle"
                    ], options=[
                        {
                            "scale_factor": 1
                        },
                        {
                            "scale_factor": 0.5,
                            "color": "AliceBlue",
                            "offset": [0.3, 0.2]
                        },
                        {
                            "scale_factor": 0.5,
                            "color": "Lime",
                            "offset": [0.3, 0.2]
                        }
                    ]).get_qIcon(),
                    'callback': None,
                    'tooltip': 'Nouveau fichier'
                },
                {
                    'icon': IconApp(names=["mdi6.folder", "mdi6.circle", "fa5s.plus-circle"], options=[
                        {
                            "scale_factor": 1,
                            "color": "Orange",
                            "active": "mdi6.folder-open"
                        },
                        {
                            "scale_factor": 0.5,
                            "color": "AliceBlue",
                            "offset": [0.3, 0.2]
                        },
                        {
                            "scale_factor": 0.5,
                            "color": "Lime",
                            "offset": [0.3, 0.2]
                        }
                    ]).get_qIcon(),
                    'callback': None,
                    'tooltip': 'Nouveau dossier'
                },
                {
                    'icon': IconApp(names=["mdi6.refresh"]).get_qIcon(),
                    'callback': None,
                    'tooltip': 'Rafrachir'
                },
                {
                    'icon': IconApp(names=["mdi6.minus-box-multiple-outline"]).get_qIcon(),
                    'callback': None,
                    'tooltip': 'Tout réduire'
                },
            ],  # Penser à ajouter les actions
            "description": "Navigation dans les fichiers",
            "visible": True
        }
    ]
}
LAN_EXPLORER: Dict = {}
