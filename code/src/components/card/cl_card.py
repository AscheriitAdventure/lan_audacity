"""
    Card component:
    - "Card" est un composant qui permet d'afficher des informations sous forme de carte.
    - "Card" est composé de 3 parties:
        - "CardHeader": La partie supérieure de la carte qui contient le titre de la carte et un icone.
        - "CardBody": La partie centrale de la carte qui contient les informations à afficher.
        - "CardFooter": La partie inférieure de la carte qui contient les actions à effectuer sur la carte.
        - "CardActions": La partie droite ou gauche de la carte qui contient les actions à effectuer sur la carte.
    - "Card" est un composant générique qui peut être utilisé dans plusieurs contextes.
"""

import logging
from typing import Optional, Any
from qtpy.QtWidgets import QWidget, QGridLayout


class Card(QWidget):
    def __init__(
        self,
        top_card: Optional[QWidget] = None,  # Optional[CardHeader],
        left_card: Optional[QWidget] = None,  # Optional[CardActions],
        center_card: Optional[QWidget] = None,  # Optional[CardBody],
        right_card: Optional[QWidget] = None,  # Optional[CardActions],
        bottom_card: Optional[QWidget] = None,  # Optional[CardFooter],
        css_params: Optional[list[str]] = None,
        logger: Optional[bool] = False,
        parent=None,
    ):
        super(Card, self).__init__(parent)
        if logger:
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.DEBUG)

        # Une carte utilise un layout de type Grid
        # Une carte est composée de 3 lignes et 3 colonnes
        self.card_layout = QGridLayout()
        self.setLayout(self.card_layout)

        self.cssParameters(css_params)

        self.topCard: Optional[QWidget] = None
        self.leftCard: Optional[QWidget] = None
        self.centerCard: Optional[QWidget] = None
        self.rightCard: Optional[QWidget] = None
        self.bottomCard: Optional[QWidget] = None

        self.set_ui(top_card, left_card, center_card, right_card, bottom_card)

    def set_ui(
        self,
        top_card: Optional[QWidget],
        left_card: Optional[QWidget],
        center_card: Optional[QWidget],
        right_card: Optional[QWidget],
        bottom_card: Optional[QWidget],
    ):
        if top_card is not None:
            # Il occupera la première ligne de la grille
            self.topCard = top_card
            self.card_layout.addWidget(self.topCard, 0, 0, 1, 3)

        if bottom_card is not None:
            # Il occupera la dernière ligne de la grille
            self.bottomCard = bottom_card
            self.card_layout.addWidget(self.bottomCard, 2, 0, 1, 3)

        if left_card is not None:
            # Il occupera la première colonne de la grille
            self.leftCard = left_card
            self.card_layout.addWidget(self.leftCard, 1, 0, 1, 1)

        if right_card is not None:
            # Il occupera la dernière colonne de la grille
            self.rightCard = right_card
            self.card_layout.addWidget(self.rightCard, 1, 2, 1, 1)

        if center_card is not None:
            # center_card occupera tout l'espace restant
            self.centerCard = center_card
            self.card_layout.addWidget(self.centerCard, 1, 1, 1, 1)

    def cssParameters(self, css_params: Optional[list[str]] = None):
        """Sets the CSS parameters for the CardUI widget."""
        if css_params is None:
            css_params = [
                "background-color: #e7ebed;",
                # "border: 1px solid Black;",
                "border-radius: 4px;",
            ]
        self.setStyleSheet(" ".join(css_params))
