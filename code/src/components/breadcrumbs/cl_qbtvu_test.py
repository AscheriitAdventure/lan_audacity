from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *
import os
import random
import logging
import string
from typing import List, Optional

"""
    Commentaires:
        Je me suis planté comme un débutant. Je crash à chaque fois que j'essaie de lancer le programme.
        Je passe sur une Version 2.0 pour corriger les erreurs.
    Outils:
        - nom complet: QWidget Breadcrumbs Template Views Update 1
        - nom de la classe: QBreadcrumbsTVU1
        - QtPy(PyQt6)
        - logging
        - sys, os, etc...
    Etape 1:
        - Mettre tous dans la main puis sortir les éléments dans des fonctions

"""


class QBreadcrumbsTVU1(QWidget):
    def __init__(
        self,
        spacing: Optional[int] = 1,
        separator: Optional[str] = None,
        parent: Optional[QWidget] = None,
    ):
        super(QBreadcrumbsTVU1, self).__init__(parent)

        if separator is None:
            self.separatorCaractere = ">"
        else:
            self.separatorCaractere = separator
        self.layout = QHBoxLayout(self)

        self.layout.addWidget(QLabel("Breadcrumbs: "))
        self.layout.addWidget(QLabel(self.separatorCaractere))
        self.layout.setSpacing(spacing)

        logging.info("Initialisation de la classe QBreadcrumbsTVU1")
        # Possibilité 1: Chemin Absolu
        self.listObj1 = os.getcwd().split(os.sep)
        # Possibilité 2: Liste de Strings
        self.listObj2 = ["Accueil", "Produits", "Frais", "Fruits", "Pomme", "Golden"]

        logging.info(f"Choix 1: {len(self.listObj1)}, Choix 2: {len(self.listObj2)}")

        # Possibilité 3: Liste de QPushButton
        self.listObj3 = []

        for i in range(7):
            btn = QPushButton(f"Button {i}")
            btn.setFlat(True)
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            chaine_aleatoire = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            btn.setToolTip(chaine_aleatoire)
            self.listObj3.append(btn)
        
        logging.info(f"Choix 3: {len(self.listObj3)}")

        self.setLayoutObjects(self.listObj1)
    
    def cleanLayout(self):
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        logging.info("Nettoyage du Layout")
    
    def setLayoutObjects(self, listObj: List[QWidget | str]):
        if self.layout.count() > 0:
            self.cleanLayout()

        for index, obj in enumerate(listObj):
            if isinstance(obj, QWidget):
                self.layout.addWidget(obj)
            elif isinstance(obj, str):
                btn = QPushButton(obj)
                btn.setFlat(True)
                btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                self.layout.addWidget(btn)
            
            if index < len(listObj) - 1:
                self.layout.addWidget(QLabel(self.separatorCaractere))
        logging.info("Ajout des éléments dans le Layout")

        self.update()
