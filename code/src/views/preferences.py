from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *
import logging

from src.views.templates_views import CardStackGeneral
from src.models.language_app import LanguageApp
from src.models.configuration_file import ConfigurationFile


class PreferencesGeneral(CardStackGeneral):
    def __init__(
            self,
            obj_title: str,
            obj_lang: LanguageApp,
            obj_view: ConfigurationFile,
            parent=None
        ):
        super().__init__(
            obj_title=obj_title, 
            obj_lang=obj_lang, 
            obj_view=obj_view,
            parent=parent
        )
        logging.info(self.objManager)

    def setCardList(self):
        self.card_list = [
            {
                "icon_card": None,
                "title_card": QLabel("Name Software"),
                "img_card": None,
                "corps_card": QLineEdit(self.objManager.data['system']['name']),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Description Software"),
                "img_card": None,
                "corps_card": QTextEdit(self.objManager.data['system']['description']),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Version Software"),
                "img_card": None,
                "corps_card": QLineEdit(self.objManager.data['system']['version']),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Authors Software"),
                "img_card": None,
                "corps_card": QLineEdit(self.objManager.data['system']['authors']),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Organisation"),
                "img_card": None,
                "corps_card": QLineEdit(self.objManager.data['system']['organization']),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Type Software"),
                "img_card": None,
                "corps_card": QLineEdit(self.objManager.data['system']['type']),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Version Date"),
                "img_card": None,
                "corps_card": QLineEdit(str(self.objManager.data['system']['version_date'])),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Python Language Version"),
                "img_card": None,
                "corps_card": QLineEdit(str(self.objManager.data['system']['version_python'])),
            },
            {
                "icon_card": None,
                "title_card": QLabel("PyQT Version"),
                "img_card": None,
                "corps_card": QLineEdit(str(self.objManager.data['system']['version_pyqt'])),
            },
            {
                "icon_card": None,
                "title_card": QLabel("NMAP Version"),
                "img_card": None,
                "corps_card": QLineEdit(str(self.objManager.data['system']['version_nmap'])),
            },
        ]