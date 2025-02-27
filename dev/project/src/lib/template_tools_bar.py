from typing import Dict
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
# Side Panel
FILES_EXPLORER: Dict = {
    "stacked_title": "Explorateur Fichiers",
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
                    'icon': {
                        "names": ["mdi6.file-outline", "mdi6.circle", "fa5s.plus-circle"],
                        "options": [
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
                        ]
                    },
                    'callback': "create_new_file",
                    'tooltip': 'Nouveau fichier'
                },
                {
                    'icon': {
                        "names": ["mdi6.folder", "mdi6.circle", "fa5s.plus-circle"],
                        "options": [
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
                        ]
                    },
                    'callback': "create_new_folder",
                    'tooltip': 'Nouveau dossier'
                },
                {
                    'icon': {"names": ["mdi6.refresh"]},
                    'callback': "refresh_tree_view",
                    'tooltip': 'Rafrachir'
                },
                {
                    'icon': {"names": ["mdi6.minus-box-multiple-outline"]},
                    'callback': "collapse_all_tree_items",
                    'tooltip': 'Tout réduire'
                },
            ],  # Penser à ajouter les actions
            "description": "Navigation dans les fichiers",
            "visible": True
        }
    ]
}

LAN_EXPLORER: Dict = {
    "stacked_title": "Networks",
    "separator": True,
    "shortcut": "Ctrl+Shift+E",
    "enable": True,
    "fields": [
        {
            "title": "Network Object Ouvert",
            "form_list": "list-btn",
            "separator": True,
            "collapsed": False,
            "tooltip": "Liste des interfaces ouverts",
            "actions": [],  # Penser à ajouter les actions
            "description": "Liste des onglets  de type objet ouverts",
            "visible": False
        },
        {
            # Nom du dossier implémenter
            "title": "Project Name",
            "form_list": "tree",
            "separator": True,
            "collapsed": False,
            "tooltip": f"Explorateur de Réseaux de Project Name",
            "actions": [
                {
                    'icon': {
                        "names": ["mdi6.desktop-tower", "mdi6.circle", "fa5s.plus-circle"],
                        "options": [
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
                        ]
                    },
                    'callback': "create_new_machine",
                    'tooltip': 'Nouvelle Machine'
                },
                {
                    'icon': {
                        "names": ["mdi6.lan", "mdi6.circle", "fa5s.plus-circle"],
                        "options": [
                            {
                                "scale_factor": 1,
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
                        ]
                    },
                    'callback': "create_new_network",
                    'tooltip': 'Nouveau Réseau'
                },
                {
                    'icon': {"names": ["mdi6.refresh"]},
                    'callback': "refresh_tree_view",
                    'tooltip': 'Rafrachir'
                },
                {
                    'icon': {"names": ["mdi6.minus-box-multiple-outline"]},
                    'callback': "collapse_all_tree_items",
                    'tooltip': 'Tout réduire'
                },
            ],  # Penser à ajouter les actions
            "description": "Navigation dans les réseaux",
            "visible": True
        }
    ]
}

DLC_EXPLORER: Dict = {
    "stacked_title": "Extensions",
    "separator": True,
    "shortcut": "Ctrl+Shift+E",
    "enable": True,
    "fields": [
        {
            "title": "Extensions Ouvert",
            "form_list": "list-btn",
            "separator": True,
            "collapsed": False,
            "tooltip": "Liste des extensions ouverts",
            "actions": [],  # Penser à ajouter les actions
            "description": "Liste des onglets de type extension ouverts",
            "visible": False
        },
        {
            "title": "Liste Simple",
            "form_list": "list-btn",
            "separator": True,
            "collapsed": False,
            "tooltip": "Liste d'éléments",
            "actions": [],
            "spacer": False,
            "description": "Liste d'éléments simples",
            "visible": True,
            "slots": []
        },
    ]
}

# Object Tab
DEVICE_TAB: Dict = {
    "stacked_title": "Device Tab",
    "separator": True,
    "shortcut": None,
    "enable": True,
    "fields": [
        {
            "title": "Dashboard",
            "form_list": "fmcg", # Fixed Mosaics Cards Grid
            "separator": True,
            "collapsed": False,
            "tooltip": "Affiche le tableau de bord",
            "actions": [
                {
                    'icon': {
                        "names:": ["mdi6.plus-circle"],
                        "options": [
                            {
                                "scale_factor": 1,
                                "color": "Lime",
                                "active": "mdi6.plus-circle-outline"
                            }
                        ]
                    },
                    'callback': "",
                    'tooltip': "More"
                },
                {
                    'icon': {
                        "names:": ["mdi6.minus-circle"],
                        "options": [
                            {
                                "scale_factor": 1,
                                "color": "Red",
                                "active": "mdi6.minus-circle-outline"
                            }
                        ]
                    },
                    'callback': "",
                    'tooltip': "Less"
                },
            ],  
            "description": "Affiche le tableau de bord et les informations de l'objet",
            "visible": True
        },
        {
            "title": "Interfaces",
            "form_list": "dmcg", # Dynamic Mosaics Cards Grid
            "separator": True,
            "collapsed": False,
            "tooltip": "Affiche les données de l'objet",
            "actions": [
                {
                    'icon': {},
                    'callback': "",
                    'tooltip': "grid X colonne"
                },
                {
                    'icon': {
                        "names:": ["mdi6.plus-circle"],
                        "options": [
                            {
                                "scale_factor": 1,
                                "color": "Lime",
                                "active": "mdi6.plus-circle-outline"
                            }
                        ]
                    },
                    'callback': "",
                    'tooltip': "More"
                },
                {
                    'icon': {
                        "names:": ["mdi6.minus-circle"],
                        "options": [
                            {
                                "scale_factor": 1,
                                "color": "Red",
                                "active": "mdi6.minus-circle-outline"
                            }
                        ]
                    },
                    'callback': "",
                    'tooltip': "Less"
                },
            ],  
            "description": "Affiche les interfaces de l'objet",
            "visible": True
        },
    ]
}

NETWORK_TAB: Dict = {
    "stacked_title": "Network Tab",
    "separator": True,
    "shortcut": None,
    "enable": True,
    "fields": [
        {
            "title": "Dashboard",
            "form_list": "fmcg", # Fixed Mosaics Cards Grid
            "separator": True,
            "collapsed": False,
            "tooltip": "Affiche le tableau de bord",
            "actions": [
                {
                    'icon': {
                        "names:": ["mdi6.plus-circle"],
                        "options": [
                            {
                                "scale_factor": 1,
                                "color": "Lime",
                                "active": "mdi6.plus-circle-outline"
                            }
                        ]
                    },
                    'callback': "",
                    'tooltip': "More"
                },
                {
                    'icon': {
                        "names:": ["mdi6.minus-circle"],
                        "options": [
                            {
                                "scale_factor": 1,
                                "color": "Red",
                                "active": "mdi6.minus-circle-outline"
                            }
                        ]
                    },
                    'callback': "",
                    'tooltip': "Less"
                },
            ],  
            "description": "Affiche le tableau de bord et les informations de l'objet",
            "visible": True
        },
        {
            "title": "Interfaces",
            "form_list": "dmcg", # Dynamic Mosaics Cards Grid
            "separator": True,
            "collapsed": False,
            "tooltip": "Affiche les données de l'objet",
            "actions": [
                {
                    'icon': {},
                    'callback': "",
                    'tooltip': "grid X colonne"
                },
                {
                    'icon': {
                        "names:": ["mdi6.plus-circle"],
                        "options": [
                            {
                                "scale_factor": 1,
                                "color": "Lime",
                                "active": "mdi6.plus-circle-outline"
                            }
                        ]
                    },
                    'callback': "",
                    'tooltip': "More"
                },
                {
                    'icon': {
                        "names:": ["mdi6.minus-circle"],
                        "options": [
                            {
                                "scale_factor": 1,
                                "color": "Red",
                                "active": "mdi6.minus-circle-outline"
                            }
                        ]
                    },
                    'callback': "",
                    'tooltip': "Less"
                },
            ],  
            "description": "Affiche les interfaces de l'objet",
            "visible": True
        },
        {
            "title": "Devices",
            "form_list": "dmcg", # Dynamic Mosaics Cards Grid
            "separator": True,
            "collapsed": False,
            "tooltip": "Affiche les données de l'objet",
            "actions": [
                {
                    'icon': {},
                    'callback': "",
                    'tooltip': "grid X colonne"
                },
                {
                    'icon': {},
                    'callback': "",
                    'tooltip': "More"
                },
                {
                    'icon': {},
                    'callback': "",
                    'tooltip': "Less"
                },
            ],  
            "description": "Affiche les interfaces de l'objet",
            "visible": True
        },
        {
            "title": "VLANs",
            "icon": {
                "names": ["mdi6.lan"],
                "options": None
            },
            "form_list": "map",
            "separator": True,
            "collapsed": False,
            "tooltip": "Affiche les VLAN sur réseau",
            "actions": [],
            "description": "Affiche les VLAN du réseau",
            "visible": True                
        },
        {
            "title": "Network Map",
            "icon": {
                "names": ["mdi6.map"],
                "options": None
            },
            "form_list": "map",
            "separator": True,
            "collapsed": False,
            "tooltip": "Affiche la carte du réseau",
            "actions": [],
            "description": "Affiche la carte du réseau",
            "visible": True                
        },
    ]
}

