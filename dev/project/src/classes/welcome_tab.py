import enum
from typing import Optional, ClassVar, Any
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *
import logging
import os
import sys
import inspect


"""
    Objectif:
        - Créer une classe qui permet de créer un onglet avec des paramètres par défaut
        - Créer un onglet de bienvenue
    Remarque:
        Je compte bien comprendre comment fonctionne les classes "QTabWidget" et "QTabBar".
"""

class TabFactory(QTabWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.removeTab)
        self.setMovable(True)
        self.setDocumentMode(True)
    

class WelcomeTab(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.initUI()
    
    def initUI(self):
        self.setLayout(QVBoxLayout(self))
        self.layout().addStretch(1)
        # TITRE
        # SOUS-TITRE
        # Qwidget->QHBox: Apps
        # Box 1: Commencer
        # Box 2: Récent
        # Box 3: Custom
        self.layout().addStretch(1)