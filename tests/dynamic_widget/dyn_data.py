# Variable Template Default
VAR_TMP_DFT = {
    'type': 'container',
    'id': 'mainWindow',
    'layout': {
            'type': 'vertical',
            'margins': 10,
            'spacing': 5,
            'children': [
                {
                    'type': 'label',
                    'text': 'Formulaire dynamique',
                    'style': {
                        'font': {
                            'size': 16,
                            'bold': True
                        }
                    }
                },
                {
                    'type': 'frame',
                    'frameShape': 'stylePanel',
                    'frameShadow': 'raised',
                    'layout': {
                        'type': 'form',
                        'margins': 10,
                        'children': [
                            {
                                'type': 'lineEdit',
                                'id': 'nameField',
                                'placeholder': 'Entrez votre nom',
                                'label': 'Nom :'
                            },
                            {
                                'type': 'comboBox',
                                'id': 'countryCombo',
                                'items': ['France', 'Canada', 'Belgique', 'Suisse'],
                                'label': 'Pays :'
                            },
                            {
                                'type': 'spinBox',
                                'id': 'ageSpinBox',
                                'minimum': 18,
                                'maximum': 120,
                                'value': 30,
                                'label': 'Âge :'
                            }
                        ]
                    }
                },
                {
                    'type': 'groupBox',
                    'title': 'Options',
                    'layout': {
                        'type': 'vertical',
                        'children': [
                            {
                                'type': 'checkBox',
                                'id': 'newsletterCheck',
                                'text': 'Inscription à la newsletter'
                            },
                            {
                                'type': 'checkBox',
                                'id': 'termsCheck',
                                'text': "J'accepte les conditions d'utilisation"
                            }
                        ]
                    }
                },
                {
                    'type': 'container',
                    'layout': {
                        'type': 'horizontal',
                        'children': [
                            {
                                'type': 'button',
                                'id': 'cancelButton',
                                'text': 'Annuler',
                                'style': {
                                    'fixedWidth': 100
                                }
                            },
                            {
                                'type': 'button',
                                'id': 'submitButton',
                                'text': 'Valider',
                                'style': {
                                    'fixedWidth': 100,
                                    'styleSheet': 'background-color: #4CAF50; color: white;'
                                }
                            }
                        ]
                    }
                }
            ]
    }
}

# Variable Template List Card
# Network - Dashboard
VAR_N_DB = {
    "type": "container",
    "id": "networkDashboard",
    "layout": {
        "type": "vertical",
        "margin": 0,
        "spacing": 1,
        "children": [
            {
                "type": "frame",
                "frameShape": "stylePanel",
                "frameShadow": "raised",
                "layout": {
                    "type": "horizontal",
                    "margins": {
                        "left": 1
                    },
                    "children": [
                        {
                            "type": "label",
                            "text": "Dashboard",
                            "style": {
                                "font": {
                                    "size": 16,
                                    "bold": True
                                }
                            }
                        },
                        {
                            "type": "spacer",
                            "stretch": 1
                        },
                        {
                            "type": "button",
                            "id": "moreButton",
                            "text": "addCard",
                            "style": {
                                "styleSheet": "background-color: green; color: white;"
                            }
                        },
                        {
                            "type": "button",
                            "id": "lessButton",
                            "text": "removeCard",
                            "style": {
                                "styleSheet": "background-color: red; color: white;"
                            }
                        }
                    ]
                }
            },
            {
                "type": "frame",
                "frameShape": "hLine",
                "frameShadow": "raised",
            },
            {
                "type": "container",
                "id": "scrollContainer",
                "layout": {
                    "type": "grid",
                    "margin": 0,
                    "spacing": 1,
                    "children": [
                        {
                            "type": "frame",
                            "frameShape": "stylePanel",
                            "frameShadow": "raised",
                            "layout": {
                                "type": "form",
                                "margin": 5,
                                "children": [
                                    {
                                        "type": "label",
                                        "text": "Lan Audacity",
                                        "style": {
                                            "font": {
                                                "size": 16,
                                                "bold": True
                                            }
                                        }
                                    },
                                    {
                                        "type": "frame",
                                        "frameShape": "hLine",
                                        "frameShadow": "raised"
                                    },
                                    {
                                        "type": "lineEdit",
                                        "id": "appVersion",
                                        "placeholder": "Version de l'application",
                                        "label": "Version :"
                                    },
                                    {
                                        "type": "lineEdit",
                                        "id": "appUpdateDate",
                                        "placeholder": "Date de la Dernière Mise à jour",
                                        "label": "Date :"
                                    },
                                    {
                                        "type": "lineEdit",
                                        "id": "programLanguage",
                                        "placeholder": "Compilateur",
                                        "label": "Language :"
                                    },
                                    {
                                        "type": "lineEdit",
                                        "id": "qtType",
                                        "placeholder": "Qt Type",
                                        "label": "Qt :"
                                    },
                                    {
                                        "type": "lineEdit",
                                        "id": "nmapVersion",
                                        "placeholder": "NMAP Version",
                                        "label": "NMAP :"
                                    },
                                    {
                                        "type": "lineEdit",
                                        "id": "osInfo",
                                        "placeholder": "Système d'Exploitation",
                                        "label": "OS :"
                                    },
                                    {
                                        "type": "lineEdit",
                                        "id": "appOrganization",
                                        "placeholder": "Entreprise garante de la publication de l'application",
                                        "label": "Oganization :"
                                    },
                                ],
                            },
                            "position": {
                                "row": 0,
                                "column": 0,
                                "columnSpan": 1,
                                "rowSpan": 1
                            }
                        }
                    ]
                }
            }
        ]
    }
}
# Network - Interfaces
VAR_N_ITF = {
    "type": "container",
    "id": "networkInterfaces",
    "layout": {}
}
# Network - Devices

VAR_N_DVS = {
    "type": "container",
    "id": "networkDevices",
    "layout": {}
}
# Network - VLANs
VAR_N_VLAN = {
    "type": "container",
    "id": "networkVLANs",
    "layout": {}
}
# Network - Network Map
VAR_N_NWM = {
    "type": "container",
    "id": "networkNetworkMap",
    "layout": {}
}
