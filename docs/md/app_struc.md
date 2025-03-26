```terminal
mon_application/
│
├── main.py                      # Point d'entrée de l'application
├── requirements.txt             # Dépendances du projet
├── setup.py                     # Script d'installation
├── README.md                    # Documentation principale
├── LICENSE                      # Licence du projet
│
├── assets/                      # Ressources statiques
│   ├── icons/                   # Icônes de l'application
│   ├── images/                  # Images utilisées dans l'application
│   ├── styles/                  # Feuilles de style QSS (CSS pour Qt)
│   └── fonts/                   # Polices personnalisées
│
├── src/                         # Code source principal
│   ├── __init__.py
│   │
│   ├── models/                  # Modèles de données
│   │   ├── __init__.py
│   │   └── data_models.py       # Classes pour les données
│   │
│   ├── views/                   # Composants d'interface utilisateur
│   │   ├── __init__.py
│   │   ├── main_window.py       # Fenêtre principale
│   │   ├── dialogs/             # Boîtes de dialogue
│   │   │   ├── __init__.py
│   │   │   ├── preferences.py
│   │   │   └── about.py
│   │   │
│   │   └── widgets/            # Widgets personnalisés
│   │       ├── __init__.py
│   │       └── custom_widgets.py
│   │
│   ├── controllers/            # Logique de contrôle
│   │   ├── __init__.py
│   │   └── app_controller.py   # Contrôleur principal
│   │
│   └── utils/                  # Utilitaires et fonctions helpers
│       ├── __init__.py
│       ├── config.py           # Gestion de la configuration
│       ├── logger.py           # Système de logging
│       └── helpers.py          # Fonctions utilitaires diverses
│
├── resources/                  # Ressources Qt compilées
│   └── resources.qrc           # Fichier de ressources Qt
│
├── data/                       # Données de l'application
│   ├── config.ini              # Fichier de configuration
│   └── database/               # Base de données locale si nécessaire
│
└── tests/                      # Tests unitaires et d'intégration
    ├── __init__.py
    ├── test_models.py
    ├── test_views.py
    └── test_controllers.py
```
