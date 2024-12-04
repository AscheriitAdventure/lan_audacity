import logging
from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *
from typing import Optional

from src.classes.classesExport import *
from src.views.templates.templatesExport import *

"""
    Ancien Nom: GeneralSidePanel
    Nom Complet: Side Panel Widget
    Commentaire:
        "Side Panel Widget" est une évolution de "GeneralSidePanel".
        A la suite de fuites de données dans cette classe mère (GeneralSidePanel), il a été décidé de réalisé un "Contrôle Qualité de Code" sur tout le projet.
    Description:
        "Side Panel Widget" anciennement "GeneralSidePanel" est un widget mère qui permet d'afficher un panneau latéral gauche(GeneralSidePanel), 
        et qui a pour objectif de servir de support à d'autres widgets filles.
        Il propose comme fonctionnalités:
        - une gestion des widgets enfants
        - une gestion des événements (avec Signal/Slot)
        - une fonction pour gérer l'ouverture d'onglets
        - une fonction pour gérer le model de QTreeView
    Mise à jour:
        - [_] passage de QWidget à QDockWidget
    
"""

class SidePanel(QWidget):
    extObjChanged = Signal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setObjectName("sidePanel")


class FileExplorerPanel(QDockWidget):
    def __init__(
            self,
            path: str, 
            parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Explorer".upper())
        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetFeatureMask)

        self.treeView = QTreeView()
        self.model = QFileSystemModel()
        self.model.setRootPath(path)
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(path))
        self.setWidget(self.treeView)

        