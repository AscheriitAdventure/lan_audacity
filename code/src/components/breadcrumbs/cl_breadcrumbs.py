from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *
import os
import sys
import logging
from typing import Any, Dict, List, Tuple, Optional


class QBreadcrumbs(QWidget):
    def __init__(
            self,
            spacing: Optional[int] = 1,
            separator: Optional[QLabel] = QLabel(">"), 
            parent: Optional[QWidget] = None
            ):
        super(QBreadcrumbs, self).__init__(parent)

        self.layout = QHBoxLayout(self)

        self.rootItem = "<root>"
        self.layout.setSpacing(spacing)
        self.separatorLabel = separator
        self.breadcrumbs = []

    def setSeparatorLabel(self, separator: QLabel):
        self.separatorLabel = separator
    
    def setSpacing(self, spacing: int):
        self.layout.setSpacing(spacing)
    
    def clean_layout(self):
        """
        Supprime tous les widgets du layout pour permettre une mise à jour.
        """
        for i in reversed(range(self.layout.count())):
            widget = self.layout.takeAt(i).widget()
            if widget is not None:
                widget.deleteLater()
    
    def generate_breadcrumbs(self, items):
        self.breadcrumbs = items

        for index, item in enumerate(items):
            # Ajouter le bouton ou label pour l'élément
            button = QPushButton(item, self)
            button.setFlat(True)  # Style plat pour ressembler à un lien
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _, idx=index: self.breadcrumb_clicked.emit(idx))
            self.layout.addWidget(button)

            # Ajouter le séparateur sauf pour le dernier élément
            if index < len(items) - 1:
                self.layout.addWidget(self.separatorLabel)
    
    def set_breadcrumbs(self, items):
        self.clean_layout()  # Nettoyer le layout avant d'ajouter de nouveaux items
        self.generate_breadcrumbs(items)  # Générer les nouveaux widgets
        self.update()
