from qtpy.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from qtpy.QtCore import Qt
from qtpy.QtGui import QCursor
import logging
from typing import List, Optional


class QBreadcrumbs(QWidget):
    def __init__(
        self,
        list_objects: Optional[List[QWidget | str]] = None,
        spacing: Optional[int] = 1,
        separator: Optional[str] = None,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)

        if separator is None:
            self.separatorCaractere = ">"
        else:
            self.separatorCaractere = separator
        
        if list_objects is None:
            self.breadcrumbs = ["Terre", "Europe", "France", "Paris", "Eiffel Tower"]
        else:
            self.breadcrumbs = list_objects[:]
        
        self.layout = QHBoxLayout(self)
        self.setAutoFillBackground(True)
        self.layout.setSpacing(spacing)

        self.setLayoutObjects(self.breadcrumbs)
    
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

"""
    Commentaire:
        Dans une optique d'évolution de la classe il serait intéressant de pouvoir orienter
        les éléments de la liste dans un sens ou dans l'autre (droite - gauche, haut - bas).
"""