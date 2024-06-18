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
                "title": QLabel("Name Software"),
                "image_path": None,
                "corps_card": QLineEdit(self.objManager.data['system']['name']),
            },
            {
                "icon_card": None,
                "title": QLabel("Description Software"),
                "image_path": None,
                "corps_card": QTextEdit(self.objManager.data['system']['description']),
            },
            {
                "icon_card": None,
                "title": QLabel("Version Software"),
                "image_path": None,
                "corps_card": QLineEdit(self.objManager.data['system']['version']),
            },
            {
                "icon_card": None,
                "title": QLabel("Authors Software"),
                "image_path": None,
                "corps_card": QLineEdit(self.objManager.data['system']['authors']),
            },
            {
                "icon_card": None,
                "title": QLabel("Organisation"),
                "image_path": None,
                "corps_card": QLineEdit(self.objManager.data['system']['organization']),
            },
            {
                "icon_card": None,
                "title": QLabel("Type Software"),
                "image_path": None,
                "corps_card": QLineEdit(self.objManager.data['system']['type']),
            },
            {
                "icon_card": None,
                "title": QLabel("Version Date"),
                "image_path": None,
                "corps_card": QLineEdit(str(self.objManager.data['system']['version_date'])),
            },
            {
                "icon_card": None,
                "title": QLabel("Python Language Version"),
                "image_path": None,
                "corps_card": QLineEdit(str(self.objManager.data['system']['version_python'])),
            },
            {
                "icon_card": None,
                "title": QLabel("PyQT Version"),
                "image_path": None,
                "corps_card": QLineEdit(str(self.objManager.data['system']['version_pyqt'])),
            },
            {
                "icon_card": None,
                "title": QLabel("NMAP Version"),
                "image_path": None,
                "corps_card": QLineEdit(str(self.objManager.data['system']['version_nmap'])),
            },
        ]