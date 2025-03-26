from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *
from typing import *
import logging
import inspect


class TitleWithAction(QWidget):
    def __init__(
        self,
        title: str,
        stretch_ttl: int = 1,
        action: Optional[list[QPushButton]] = None,
        parent=None,
    ):
        super().__init__(parent=parent)

        # Initialisation des composants de l'interface
        self.title_label = QLabel(title)  # Le titre est un QLabel
        self.action_buttons = (
            action if action else []
        )  # Liste des actions sous forme de QPushButton

        # Layout principal
        self.main_layout = QHBoxLayout(self)  # Utilise un layout horizontal

        # Ajoute le titre
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addStretch(stretch_ttl)

        # Ajoute les boutons d'action (s'il y en a)
        if self.action_buttons:
            for button in self.action_buttons:
                self.main_layout.addWidget(button)

        # Aligne le layout à gauche
        self.setLayout(self.main_layout)
 