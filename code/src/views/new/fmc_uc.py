from templates_2 import FixedMosaicsCards as FMC

from qtpy.QtWidgets import QLabel
from typing import Any

from src.classes.languageApp import LanguageApp
from src.classes.iconsApp import IconsApp
from src.components.card.cl_card import CardHeader

"""
    Nom complet: Unit Central Dashboard Fixed Mosaics Cards
    Description: Cette classe est une mise à jour de 'UCDashboard(DashboardCardTemplate)'
    Nouveau nom: UCDashboardFMC
"""

class UCDashboardFMC(FMC):
    def __init__(self, obj_title: str, obj_lang: LanguageApp, obj_view: Any, obj_icon: IconsApp, parent=None):
        super().__init__(obj_title, obj_lang, obj_view, obj_icon, parent)

    def setCardsList(self):
        # Exemple de personnalisation pour UCDashboard
        self.cardList = [
            {
                "layout": {
                    "row": 0,
                    "column": 0,
                    "rowSpan": None,
                    "columnSpan": None,
                    "alignement": None
                },
                "top_card": CardHeader(
                    icon_card=self.iconsManager.get_icon("ucIcon"),
                    title_card=QLabel("User Control")),
                "left_card": None,
                "center_card": QLabel("Manage your users and permissions here."),
                "right_card": None,
                "bottom_card": None
            }
        ]