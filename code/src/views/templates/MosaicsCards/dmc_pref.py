from src.views.templates.MosaicsCards.cl_dmc import DynamicsMosaicsCards as DMC

from qtpy.QtWidgets import QLabel, QLineEdit, QTextEdit
from typing import Any

from src.classes.languageApp import LanguageApp
from src.classes.configurationFile import ConfigurationFile

"""
    Nom complet: Preferences General Dynamics Mosaics Cards
    Description: Cette classe est une mise à jour de 'PreferencesGeneral(CardStackGeneral)'
    Nouveau nom: PreferencesGeneralDMC
"""


class PreferencesGeneralDMC(DMC):
    def __init__(
        self,
        obj_title: str,
        obj_lang: LanguageApp,
        obj_view: ConfigurationFile,
        parent=None,
    ):
        super().__init__(
            obj_title=obj_title, obj_lang=obj_lang, obj_view=obj_view, parent=parent
        )

    def setCardList(self):
        self.card_list = [
            {
                "top_card": QLabel("Name Software"),
                "center_card": QLineEdit(self.objManager.data["system"]["name"])
            },
            {
                "top_card": QLabel("Description Software"),
                "center_card": QTextEdit(self.objManager.data["system"]["description"])
            },
            {
                "top_card": QLabel("Version Software"),
                "center_card": QLineEdit(self.objManager.data["system"]["version"])
            },
            {
                "top_card": QLabel("Authors Software"),
                "center_card": QLineEdit(self.objManager.data["system"]["authors"])
            },
            {
                "top_card": QLabel("Organization"),
                "center_card": QLineEdit(self.objManager.data["system"]["organization"])
            },
            {
                "top_card": QLabel("Type Software"),
                "center_card": QLineEdit(self.objManager.data["system"]["type"])
            },
            {
                "top_card": QLabel("Version Date"),
                "center_card": QLineEdit(str(self.objManager.data["system"]["version_date"]))
            },
            {
                "top_card": QLabel("Python Language Version"),
                "center_card": QLineEdit(str(self.objManager.data["system"]["version_python"]))
            },
            {
                "top_card": QLabel("PyQT Version"),
                "center_card": QLineEdit(str(self.objManager.data["system"]["version_pyqt"]))
            },
            {
                "top_card": QLabel("NMAP Version"),
                "center_card": QLineEdit(str(self.objManager.data["system"]["version_nmap"]))
            },
        ]
