from src.views.new.templates_2 import DynamicsMosaicsCards as DMC

from qtpy.QtWidgets import QLabel, QLineEdit, QWidget, QVBoxLayout, QPushButton
from qtpy.QtGui import QImage
from typing import Optional
import logging
import qtawesome as qta

from src.classes.classesExport import ConfigurationFile, LanguageApp, IconsApp
from src.components.componentsExport import CardHeader, CardImage, AccordionWidget

from src.views.templatesViews import LineUpdate

"""
    Nom complet: Palette Icon Settings Dynamics Mosaics Cards
    Description: Cette classe est une mise à jour de 'PaletteIconSettings(CardStackGeneral)'
    Nouveau nom: PaletteIconSettingsDMC
"""


class PaletteIconSettingsDMC(DMC):
    def __init__(
        self,
        obj_title: str,
        obj_lang: LanguageApp,
        obj_view: IconsApp,
        obj_icon: Optional[IconsApp] = None,
        obj_img: Optional[QImage] = None,
        parent=None,
    ):
        super().__init__(obj_title, obj_lang, obj_view, obj_icon, obj_img, parent)

    def setCardList(self):
        self.card_list = []
        for icon in self.objManager.data_manager:
            # Titre de la carte
            cardTtl = QLabel(icon["name"])
            # Image de la carte
            cardImg = self.objManager.get_icon(icon["name"]).pixmap(64, 64).toImage()
            # Corps de la carte
            if icon.get("options") is not None:
                cardOpt = QWidget()
                cardOptLayout = QVBoxLayout()
                cardOpt.setLayout(cardOptLayout)

                len_options = len(icon["options"])
                data_options = icon["options"]

                for i, option in enumerate(data_options):
                    keys = option.keys()
                    if len_options > 1:
                        cardOptLayout.addWidget(
                            QLabel(f"{icon["platform_and_name"][i]} :")
                        )
                    for key in keys:
                        btn_options = QPushButton(self)
                        btn_options.setIcon(qta.icon("mdi6.pencil"))
                        if len_options > 1:
                            ttl_label = QLabel(f"    {key} :")
                        else:
                            ttl_label = QLabel(f"{key} :")

                        options_lineUpdate = LineUpdate(
                            label_obj=ttl_label,
                            input_obj=QLineEdit(str(option[key])),
                            action_obj=btn_options,
                        )
                        cardOptLayout.addWidget(options_lineUpdate)

            else:
                cardOpt = QLabel("No options")

            icon_dict: dict = {
                "top_card": CardHeader(
                    icon_card=qta.icon("mdi6.palette-advanced"),
                    title_card=cardTtl),
                "center_card": CardImage(image_card=cardImg),
                "right_card": cardOpt
            }

            self.card_list.append(icon_dict)
        logging.info(f"Card list: {len(self.card_list)} item(s)")

"""
    Commentaires:
        Bon travail, la classe est bien structurée et les noms des méthodes et des variables sont explicites.
        Toutefois la liste qui montre les paramètres des icônes est moche.
        Je vous propose de la rendre plus agréable en utilisant le principe d'accordéon du web.
    Consignes:
        - Nom complet: Palette Icon Settings Dynamics Mosaics Cards Accordion
        - Description: Cette classe est une mise à jour de 'PaletteIconSettingsDMC'
        - Nouveau nom: PISDMCAccordion
    Etape 1:
        - Implémentez la méthode 'setCardListAccordion' qui affiche les paramètres des icônes dans un accordéon.
    Aide:
    Une première recherche est à disposition en commentaire.
"""

class PISDMCAccordion(DMC):
    def __init__(
        self,
        obj_title: str,
        obj_lang: LanguageApp,
        obj_view: ConfigurationFile,
        obj_icon: Optional[IconsApp] = None,
        obj_img: Optional[QImage] = None,
        parent=None,
    ):
        super().__init__(obj_title, obj_lang, obj_view, obj_icon, obj_img, parent)

    def setCardList(self):
        self.card_list = []
        for icon in self.objManager.data:
            # Titre de la carte
            cardHeader = CardHeader(
                icon_card=qta.icon("mdi6.palette-advanced"),
                title_card=QLabel(icon["name"])
            )
            # Image de la carte
            cardImage = CardImage(
                image_card=self.iconsManager.get_icon(icon["name"]).pixmap(64, 64).toImage()
            )
            # Commentaires de la carte
            if icon.get("options") is not None:
                rightCard = QWidget()
                cardOptLayout = QVBoxLayout(rightCard)
                
                accordion = AccordionWidget()
                cardOptLayout.addWidget(accordion)

                len_options = len(icon["options"])
                data_options = icon["options"]

                for i, option in enumerate(data_options):
                    keys = option.keys()
                    content_obj = QWidget()
                    content_layout = QVBoxLayout(content_obj)

                    for key in keys:
                        btn_options = QPushButton(self)
                        btn_options.setIcon(qta.icon("mdi6.pencil"))
                        ttl_label = QLabel(f"{key} :")
                        options_lineUpdate = LineUpdate(
                            label_obj=ttl_label,
                            input_obj=QLineEdit(str(option[key])),
                            action_obj=btn_options,
                        )
                        content_layout.addWidget(options_lineUpdate)

                    accordion.add_section(f"{icon['platform_and_name'][i]}", content_obj)

            else:
                rightCard = QLabel("No options")

            # Dictionnaire
            icon_dict: dict = {
                "top_card": cardHeader,
                "center_card": cardImage,
                "right_card": rightCard
            }
            self.card_list.append(icon_dict)
        logging.info(f"Card list: {len(self.card_list)} item(s)")

