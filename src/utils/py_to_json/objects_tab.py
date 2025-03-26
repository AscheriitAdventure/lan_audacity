from typing import Dict, Any


# Object Tab
DEVICE_TAB: Dict[str, Any] = {
    "stacked_title": "Device Tab",
    "separator": True,
    "shortcut": None,
    "enable": True,
    "fields": [
        {
            "title": "Dashboard",
            "form_list": "fmcg",  # Fixed Mosaics Cards Grid
            "separator": True,
            "collapsed": False,
            "tooltip": "Affiche le tableau de bord",
            "actions": [
                {
                    'icon': {
                        "names": ["mdi6.plus-circle"],
                        "options": [
                            {
                                "scale_factor": 1,
                                "color": "Lime",
                                "active": "mdi6.plus-circle-outline"
                            }
                        ]
                    },
                    'callback': None,
                    'tooltip': "More"
                },
                {
                    'icon': {
                        "names": ["mdi6.minus-circle"],
                        "options": [
                            {
                                "scale_factor": 1,
                                "color": "Red",
                                "active": "mdi6.minus-circle-outline"
                            }
                        ]
                    },
                    'callback': None,
                    'tooltip': "Less"
                },
            ],
            "description": "Affiche le tableau de bord et les informations de l'objet",
            "visible": True
        },
        {
            "title": "Interfaces",
            "form_list": "dmcg",  # Dynamic Mosaics Cards Grid
            "separator": True,
            "collapsed": False,
            "tooltip": "Affiche les données de l'objet",
            "actions": [
                {
                    'icon': {
                        "names": ["mdi6.view-split-vertical"]
                    },
                    'callback': None,
                    'tooltip': "grid X colonne"
                },
                {
                    'icon': {
                        "names": ["mdi6.plus-circle"],
                        "options": [
                            {
                                "scale_factor": 1,
                                "color": "Lime",
                                "active": "mdi6.plus-circle-outline"
                            }
                        ]
                    },
                    'callback': None,
                    'tooltip': "More"
                },
                {
                    'icon': {
                        "names": ["mdi6.minus-circle"],
                        "options": [
                            {
                                "scale_factor": 1,
                                "color": "Red",
                                "active": "mdi6.minus-circle-outline"
                            }
                        ]
                    },
                    'callback': None,
                    'tooltip': "Less"
                },
            ],
            "description": "Affiche les interfaces de l'objet",
            "visible": True
        },
    ]
}

NETWORK_TAB: Dict[str, Any] = {
    "stacked_title": "Network Tab",
    "separator": True,
    "shortcut": None,
    "enable": True,
    "fields": [
        {
            "title": "Dashboard",
            "form_list": "fmcg",  # Fixed Mosaics Cards Grid
            "icon": {
                "names": ["mdi6.view-dashboard"],
                "options": [
                    {
                        "color": "PaleTurquoise"
                    }
                ],
            },
            "separator": True,
            "collapsed": False,
            "tooltip": "Affiche le tableau de bord",
            "actions": [
                {
                    'icon': {
                        "names": ["mdi6.plus-circle"],
                        "options": [
                            {
                                "scale_factor": 1,
                                "color": "Lime",
                                "active": "mdi6.plus-circle-outline"
                            }
                        ]
                    },
                    'callback': None,
                    'tooltip': "More"
                },
                {
                    'icon': {
                        "names": ["mdi6.minus-circle"],
                        "options": [
                            {
                                "scale_factor": 1,
                                "color": "Red",
                                "active": "mdi6.minus-circle-outline"
                            }
                        ]
                    },
                    'callback': None,
                    'tooltip': "Less"
                },
            ],
            "description": "Affiche le tableau de bord et les informations de l'objet",
            "visible": True
        },
        {
            "title": "Interfaces",
            "form_list": "dmcg",  # Dynamic Mosaics Cards Grid
            "icon": {
                "names": ["mdi6.cogs"],
                "options": [
                    {
                        "color": "LightSlateGray"
                    }
                ]
            },
            "separator": True,
            "collapsed": False,
            "tooltip": "Affiche les données de l'objet",
            "actions": [
                {
                    'icon': {
                        "names": ["mdi6.view-split-vertical"]
                    },
                    'callback': None,
                    'tooltip': "grid X colonne"
                },
                {
                    'icon': {
                        "names": ["mdi6.plus-circle"],
                        "options": [
                            {
                                "scale_factor": 1,
                                "color": "Lime",
                                "active": "mdi6.plus-circle-outline"
                            }
                        ]
                    },
                    'callback': None,
                    'tooltip': "More"
                },
                {
                    'icon': {
                        "names": ["mdi6.minus-circle"],
                        "options": [
                            {
                                "scale_factor": 1,
                                "color": "Red",
                                "active": "mdi6.minus-circle-outline"
                            }
                        ]
                    },
                    'callback': None,
                    'tooltip': "Less"
                },
            ],
            "description": "Affiche les interfaces de l'objet",
            "visible": True
        },
        {
            "title": "Devices",
            "form_list": "dmcg",  # Dynamic Mosaics Cards Grid
            "icon": {
                "names": ["mdi6.desktop-tower"],
                "options": [
                    {
                        "color": "LightSlateGray"
                    }
                ]
            },
            "separator": True,
            "collapsed": False,
            "tooltip": "Affiche les données de l'objet",
            "actions": [
                {
                    'icon': {
                        "names": ["mdi6.view-split-vertical"]
                    },
                    'callback': None,
                    'tooltip': "grid X colonne"
                },
                {
                    'icon': {
                        "names": ["mdi6.plus-circle"],
                        "options": [
                            {
                                "scale_factor": 1,
                                "color": "Lime",
                                "active": "mdi6.plus-circle-outline"
                            }
                        ]
                    },
                    'callback': None,
                    'tooltip': "More"
                },
                {
                    'icon': {
                        "names": ["mdi6.minus-circle"],
                        "options": [
                            {
                                "scale_factor": 1,
                                "color": "Red",
                                "active": "mdi6.minus-circle-outline"
                            }
                        ]
                    },
                    'callback': None,
                    'tooltip': "Less"
                },
            ],
            "description": "Affiche les interfaces de l'objet",
            "visible": True
        },
        {
            "title": "VLANs",
            "icon": {
                "names": ["mdi6.lan", "mdi6.scan-helper"],
                "options": [
                    {
                        "scale_factor": 0.75
                    },
                    {
                        "color": "Black"
                    }
                ]
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
                "names": ["mdi6.map-legend", "mdi6.routes"],
                "options": [
                    {
                        "scale_factor": 1,
                        "color": "Silver"
                    },
                    {
                        "scale_factor": 0.75,
                        "color": "ForestGreen"
                    }
                ]
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
