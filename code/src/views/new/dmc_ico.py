from src.views.new.templates_2 import DynamicsMosaicsCards as DMC

from qtpy.QtWidgets import QLabel, QLineEdit, QWidget, QVBoxLayout
from qtpy.QtGui import QImage
from typing import Optional
import logging
import qtawesome as qta

from src.classes.languageApp import LanguageApp
from src.classes.iconsApp import IconsApp

from src.components.card.cl_card import CardHeader, CardImage
from src.views.templatesViews import LineUpdate, RoundedBtn

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
                        btn_options = RoundedBtn(
                            icon=qta.icon("mdi6.pencil"), text=None, parent=self
                        )
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

    # def setCardListAccordion(self):
    #     self.card_list = []
    #     accordion = AccordionWidget()
    #     for icon in self.objManager.data_manager:
    #         # Titre de la carte
    #         cardTtl = QLabel(icon["name"])
    #         # Image de la carte
    #         cardImg = self.objManager.get_icon(icon["name"]).pixmap(64, 64).toImage()
    #         # Corps de la carte
    #         if icon.get("options") is not None:
    #             cardOpt = QWidget()
    #             cardOptLayout = QVBoxLayout()
    #             cardOpt.setLayout(cardOptLayout)
    #             data_options = icon["options"]

    #             for i, option in enumerate(data_options):
    #                 keys = option.keys()
    #                 btn_title = QPushButton(f"{icon['platform_and_name'][i]} :")

    #                 for key in keys:
    #                     btn_options = RoundedBtn(
    #                         icon=qtawesome.icon("mdi6.pencil"), text=None, parent=self
    #                     )
    #                     ttl_label = QLabel(f"{key} :")
    #                     options_lineUpdate = LineUpdate(
    #                         label_obj=ttl_label,
    #                         input_obj=QLineEdit(str(option[key])),
    #                         action_obj=btn_options,
    #                     )
    #                     cardOptLayout.addWidget(options_lineUpdate)

    #         else:
    #             cardOpt = QLabel("No options")

    #         icon_dict: dict = {
    #             "icon_card": qtawesome.icon("mdi6.palette-advanced"),  # QIcon
    #             "title_card": cardTtl,  # QLabel
    #             "img_card": cardImg,  # QImage
    #             "corps_card": cardOpt,  # QLabel ou QWidgets
    #         }
    #     logging.info(f"Card list: {len(self.card_list)} item(s)")
