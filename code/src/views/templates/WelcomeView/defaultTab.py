"""
    Informations:
        Dans le fichier 'defaultTab.py', nous allons définir une page d'affichage par défaut si une erreur survient.
    Commentaires:
        Si une erreur survient, nous affichons une page d'erreur avec un message d'erreur et un code d'erreur.
        Si c'est une page en construction, nous affichons un message de construction aléatoire.
    Outils:
        - des variables globalisées pour les titres et les logs
        - QtPy(PyQt6)
        - logging
        - nom complet: Widget Default and Monitor Widget Default
        - nom de la classe: MonitorWD
    Etape 1:
        - Créer une classe 'MonitorWD' qui hérite de 'QWidget'
        - Créer une méthode '__init__' qui initialise la classe
        - Créer une méthode 'initUI' qui initialise l'interface utilisateur
        - Créer une méthode 'initDisplay' qui initialise l'affichage
    Etape 2:
        - ajouter un layout principal 'main_layout' de type 'QVBoxLayout'
        - ajouter un 'QScrollArea' pour le défilement
        - ajouter un conteneur interne 'scroll_content' de type 'QWidget'
        - ajouter un layout 'layout' de type '?'
"""

from typing import List, Optional
from qtpy.QtWidgets import *
from qtpy.QtCore import Qt
from qtpy.QtGui import QFont
import random

from src.components.componentsExport import Card, CardImage
from src.classes.classesExport import IconsApp, LanguageApp


VAR_LIST_TITLE: List[str] = [
    "Winter is coming",
    "Coming soon",
    "The workforce work on it",
    "A storm is brewing",
    "Just around the corner",
    "Prepare for the unexpected",
    "The wheels are in motion",
    "On the horizon",
    "Change is coming",
    "The calm before the storm",
    "In the pipeline",
    "Stay tuned",
    "Work in progress",
    "Something big is on its way",
    "Under construction",
    "Coming your way",
    "The best is yet to come",
    "Hold your breath",
    "I'll be back",
]

VAR_LIST_LOGS: List[dict] = [
    {
        "log_flag": "Error",
        "log_number": 400,
        "log_description": "Bad Request",
    },
    {
        "log_flag": "Error",
        "log_number": 401,
        "log_description": "Unauthorized",
    },
    {
        "log_flag": "Error",
        "log_number": 403,
        "log_description": "Forbidden",
    },
    {
        "log_flag": "Error",
        "log_number": 404,
        "log_description": "Not Found",
    },
    {
        "log_flag": "Error",
        "log_number": 405,
        "log_description": "Method Not Allowed",
    },
    {
        "log_flag": "Error",
        "log_number": 407,
        "log_description": "Proxy Authentication Required",
    },
    {
        "log_flag": "Error",
        "log_number": 408,
        "log_description": "Request Timeout",
    },
    {
        "log_flag": "Error",
        "log_number": 429,
        "log_description": "Too Many Requests",
    },
    {
        "log_flag": "Error",
        "log_number": 500,
        "log_description": "Internal Server Error",
    },
    {
        "log_flag": "Error",
        "log_number": 502,
        "log_description": "Bad Gateway",
    },
    {
        "log_flag": "Error",
        "log_number": 503,
        "log_description": "Service Unavailable",
    },
    {
        "log_flag": "Error",
        "log_number": 504,
        "log_description": "Gateway Timeout",
    }
]


class MonitorWD(QWidget):
    def __init__(
            self, 
            icons_manager: IconsApp,
            language_manager: Optional[LanguageApp] = None,
            log_flag: Optional[bool] = False,
            parent: Optional[QWidget] = None):
        super(MonitorWD, self).__init__(parent)

        self.iconsManager = icons_manager
        self.languageManager = language_manager

        # Layout principal (avec scroll)
        self.main_layout = QVBoxLayout(self)
        self.initScrollArea()

        # Ajout des autres composants
        if log_flag:
            self.intitFlagDisplay()
        else:
            self.initDisplay()

    def initScrollArea(self):
        """
        Encapsule le layout principal dans un QScrollArea
        """
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)

        # Conteneur interne pour le contenu défilable
        self.scroll_content = QWidget()
        self.scroll_area.setWidget(self.scroll_content)

        # Utilisation de QGridLayout existant
        self.layout = QGridLayout(self.scroll_content)

    def initDisplay(self):
        imgWork = self.iconsManager.get_icon("workInProgress").pixmap(128, ).toImage()
        leftCard = CardImage(image_card=imgWork)
        centerCard = QLabel(random.choice(VAR_LIST_TITLE))
        centerCard.setFont(QFont("Arial", 12, QFont.Bold))
        rightCard = CardImage(image_card=imgWork)
        cardTemplate = Card(
            left_card=leftCard,
            center_card=centerCard,
            right_card=rightCard
        )
        self.layout.addWidget(cardTemplate, 0, 0)

    def intitFlagDisplay(self):
        pass
