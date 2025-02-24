from qtpy.QtWidgets import QWidget

import os
import logging
from typing import Optional

from src.functionsExt import current_dir
from src.classes.classesExport import ConfigurationFile, LanguageApp, IconsApp
from src.views.templates.WelcomeView.defaultTab import MonitorWD
from src.views.templates.templatesExport import LanAudacityViewGeneral
from src.views.templates.new_export import PDashboardFMC, PaletteIconSettingsDMC, UpdatesNewsDMC

"""
    Informations:
        'PreferencesViewGeneral' est une mise à jour de 'PreferencesTabView'
    Commentaires:
        Suite à la modification de la classe mère 'GeneralTabsView' en 'LanAudacityViewGeneral',
        nous avons modifié certains paramètres pour cela nous avons créé une nouvelle classe.
        Nous avons également modifié la classe pour permettre aux enfants d'avoir les bonnes données.
"""


class PreferencesViewGeneral(LanAudacityViewGeneral):
    def __init__(
            self, 
            title_panel: str,
            external_object: ConfigurationFile,
            language_manager: Optional[LanguageApp] = None,
            icons_manager: Optional[IconsApp] = None,
            parent = None
            ) -> None:
        super(PreferencesViewGeneral, self).__init__(title_panel, external_object, language_manager, icons_manager, parent)

    def setListBtn(self) -> list:
        data = [
            {
                "name": "Dashboard",
                "tooltip": "Dashboard",
                "icon": "dashboardBtn",
                "action": self.general_btn,
            },
            {
                "name": "About System",
                "tooltip": "About System",
                "icon": "lan_audacity",
                "action": self.about_btn,
            },
            {
                "name": "Palette Shortcut",
                "tooltip": "Palette Shortcut",
                "icon": "shortcutKeyAction",
                "action": self.palette_shortcut_btn,
            },
            {
                "name": "Palette Icon",
                "tooltip": "Palette Icon",
                "icon": "paletteSwatch",
                "action": self.palette_icon_btn,
            },
            {
                "name": "License",
                "tooltip": "License",
                "icon": "certificates",
                "action": self.about_btn,
            },
            {
                "name": "Update",
                "tooltip": "Update",
                "icon": "newsUpgrade",
                "action": self.update_btn,
            },
        ]
        return data

    def initDisplay(self):
        self.general_menu = PDashboardFMC(
            obj_title="Dashboard",
            obj_lang=self.languageManager, 
            obj_view=self.externalObject,
            obj_icon=self.iconsManager,
            parent=self,
        )
        self.stackedFields.addWidget(self.general_menu)
        
        data_icons = ConfigurationFile(
            os.path.normpath(os.path.join(current_dir(), self.externalObject.data['software']['conf']['icons_app']['path']))
        )
        self.palette_icon_menu = PaletteIconSettingsDMC(
            obj_title="Palette Icons",
            obj_lang=self.languageManager,
            obj_view=data_icons,
            obj_icon=self.iconsManager,
            parent=self,
        )
        self.stackedFields.addWidget(self.palette_icon_menu)

        data_update = ConfigurationFile(
            os.path.normpath(os.path.join(current_dir(), self.externalObject.data['software']['conf']['newsUpdate_app']['path']))
        )
        self.update_menu = UpdatesNewsDMC(
            obj_title="Update News",
            obj_lang=self.languageManager,
            obj_view=data_update,
            parent=self
        )
        self.stackedFields.addWidget(self.update_menu)

        data_language = ConfigurationFile(
            os.path.normpath(os.path.join(current_dir(), self.externalObject.data['software']['conf']['translate_app']['path']))
        )

        data_shortcut = ConfigurationFile(
            os.path.normpath(os.path.join(current_dir(), self.externalObject.data['software']['conf']['shortcuts_app']['path']))
        )
        self.palette_shortcut_menu = MonitorWD(
            icons_manager=self.iconsManager,
            language_manager=self.languageManager,
            parent=self
        )
        self.stackedFields.addWidget(self.palette_shortcut_menu)

        self.about_menu = MonitorWD(
            icons_manager=self.iconsManager,
            language_manager=self.languageManager,
            parent=self
        )
        self.stackedFields.addWidget(self.about_menu)

    def general_btn(self):
        self.stackedFields.setCurrentWidget(self.general_menu)

    def palette_shortcut_btn(self):
        self.stackedFields.setCurrentWidget(self.palette_shortcut_menu)

    def about_btn(self):
        self.stackedFields.setCurrentWidget(self.about_menu)

    def update_btn(self):
        self.stackedFields.setCurrentWidget(self.update_menu)

    def palette_icon_btn(self):
        self.stackedFields.setCurrentWidget(self.palette_icon_menu)


"""
    Informations:
        Suite à une erreur de conception, nous allons recréer la classe 'PreferencesViewGeneral'.
    Commentaires:
        Je suis presque un élément efficace, je dois continuer à m'améliorer.
    Etape 1:
        - nom complet: Preferences View General Update 1
        - nouveau Nom:  PVGU1
        - Trouver l'erreur de conception.
"""