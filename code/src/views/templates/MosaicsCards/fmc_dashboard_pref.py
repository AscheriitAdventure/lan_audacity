""" 
    Informations:
        Ce fichier a pour but de présenter une nouvelle présentation de "Preferences/Dashboard".
        Il doit afficher ces cartes:
            - Un rapide aperçu des informations du logiciel
            - Choix des langues
            - Opion de mise à jour
            - Un Objet qui affichera (si ce n'est pas un fichier) les dernières fonctionnalités ajoutées sinon un lien.
    Outils:
        - QtPy(PyQt6)
        - logging
        - typing
        - nom complet: Preferences Dashboard Fixed Mosaics Cards
        - nom classe: PDashboardFMC
"""
from src.views.templates.MosaicsCards.cl_fmc import FixedMosaicsCards as FMC
from qtpy.QtWidgets import QLabel

from src.classes.classesExport import LanguageApp, IconsApp, ConfigurationFile
from src.components.componentsExport import CardHeader


class PDashboardFMC(FMC):
    def __init__(
        self, 
        obj_title: str, 
        obj_lang: LanguageApp, 
        obj_view: ConfigurationFile, 
        obj_icon: IconsApp, 
        parent=None):
        super().__init__(obj_title, obj_lang, obj_view, obj_icon, parent)
    
    def setCardsList(self):
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
                    icon_card=self.iconsManager.get_icon("lan_audacity"),
                    title_card=QLabel("Software Information")),
                "left_card": None,
                "right_card": None,
                "bottom_card": None,
                "center_card": QLabel("Manage your software information here.") # <--- A Impléménter
            },
            {
                "layout": {
                    "row": 0,
                    "column": 1,
                    "rowSpan": None,
                    "columnSpan": None,
                    "alignement": None
                },
                "top_card": CardHeader(
                    icon_card=self.iconsManager.get_icon("languageAction"),
                    title_card=QLabel("Language Choice")),
                "left_card": None,
                "right_card": None,
                "bottom_card": None,
                "center_card": QLabel("Manage your Language here.") # <--- A Impléménter
            },
            {
                "layout": {
                    "row": 1,
                    "column": 0,
                    "rowSpan": None,
                    "columnSpan": None,
                    "alignement": None
                },
                "top_card": CardHeader(
                    icon_card=self.iconsManager.get_icon("updateAction"),
                    title_card=QLabel("Update Option")),
                    "left_card": None,
                "right_card": None,
                "bottom_card": None,
                "center_card": QLabel("Manage your update option here.") # <--- A Impléménter
            },
            {
                "layout": {
                    "row": 1,
                    "column": 1,
                    "rowSpan": None,
                    "columnSpan": None,
                    "alignement": None
                },
                "top_card": CardHeader(
                    icon_card=self.iconsManager.get_icon("newsUpgrade"),
                    title_card=QLabel("Feature Information")),
                "left_card": None,
                "right_card": None,
                "bottom_card": None,
                "center_card": QLabel("Manage your feature information here.") # <--- A Impléménter
            }
        ]
