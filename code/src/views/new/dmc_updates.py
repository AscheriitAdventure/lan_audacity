from src.views.new.templates_2 import DynamicsMosaicsCards as DMC

import logging
from qtpy.QtWidgets import QLabel

from src.classes.languageApp import LanguageApp
from src.classes.configurationFile import ConfigurationFile

"""
    Nom complet: Updates News Dynamics Mosaics Cards
    Description: Cette classe affiche un journal des mises à jour
    Nouveau nom: UpdatesNewsDMC
"""

class UpadtesNewsDMC(DMC):
    def __init__(self, obj_title: str, obj_lang: LanguageApp, obj_view: ConfigurationFile, parent=None):
        super().__init__(obj_title=obj_title, obj_lang=obj_lang, obj_view=obj_view, parent=parent)
    
    def generateCard(self):
        data = self.objManager.data["news_update"]
        logging.debug(f"Lenght of data: {len(data)}")
        leftCard = None
        rightCard = None
        centerCard = None
        bottomCard = None
        for obj in data:
            topCard = QLabel(f"{obj['version']} - {obj['date']}")
            if obj["sources"] is not None:
                logging.debug(f"Sources: {obj['sources']}")
                centerCard = QLabel(f"{obj['sources']}")

            if obj["authors"] is not None:
                logging.debug(f"Authors: {obj['authors']}")
                bottomCard = QLabel(f"{obj['authors']}")
            
            if obj["description"] is not None:
                logging.debug(f"Description: {obj['description']}")
                if centerCard is None:
                    centerCard = QLabel(f"{obj['description']}")
                else:
                    rightCard = QLabel(f"{obj['description']}")

            self.card_list.append(
                {
                    "top_card": topCard,
                    "left_card": leftCard,
                    "center_card": centerCard, # <--- Ajouter le texte de la description
                    "right_card": rightCard,
                    "bottom_card": bottomCard # <--- Ajouter les auteurs
                }
            )
    
    def setCardList(self):
        self.card_list = []
        self.generateCard()
    
        