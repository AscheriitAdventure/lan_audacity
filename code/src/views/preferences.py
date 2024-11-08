import qtawesome
from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *
import logging
import os
import json

from typing import Optional
from src.classes.languageApp import LanguageApp
from src.classes.cl_network import Network
from src.views.templatesViews import (
    LineUpdate,
    RoundedBtn,
    CardStackGeneral,
    TitleWithAction,
)
from src.classes.configurationFile import ConfigurationFile
from src.classes.iconsApp import IconsApp
from src.views.formsApp2 import AccordionWidget


class PreferencesGeneral(CardStackGeneral):
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
                "icon_card": None,
                "title_card": QLabel("Name Software"),
                "img_card": None,
                "corps_card": QLineEdit(self.objManager.data["system"]["name"]),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Description Software"),
                "img_card": None,
                "corps_card": QTextEdit(self.objManager.data["system"]["description"]),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Version Software"),
                "img_card": None,
                "corps_card": QLineEdit(self.objManager.data["system"]["version"]),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Authors Software"),
                "img_card": None,
                "corps_card": QLineEdit(self.objManager.data["system"]["authors"]),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Organisation"),
                "img_card": None,
                "corps_card": QLineEdit(self.objManager.data["system"]["organization"]),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Type Software"),
                "img_card": None,
                "corps_card": QLineEdit(self.objManager.data["system"]["type"]),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Version Date"),
                "img_card": None,
                "corps_card": QLineEdit(
                    str(self.objManager.data["system"]["version_date"])
                ),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Python Language Version"),
                "img_card": None,
                "corps_card": QLineEdit(
                    str(self.objManager.data["system"]["version_python"])
                ),
            },
            {
                "icon_card": None,
                "title_card": QLabel("PyQT Version"),
                "img_card": None,
                "corps_card": QLineEdit(
                    str(self.objManager.data["system"]["version_pyqt"])
                ),
            },
            {
                "icon_card": None,
                "title_card": QLabel("NMAP Version"),
                "img_card": None,
                "corps_card": QLineEdit(
                    str(self.objManager.data["system"]["version_nmap"])
                ),
            },
        ]


class NetworkGeneral(CardStackGeneral):
    def __init__(
        self, obj_title: str, obj_lang: LanguageApp, obj_view: Network, parent=None
    ):
        super().__init__(obj_title, obj_lang, obj_view, parent)

    def setCardList(self):
        self.card_list = [
            {
                "icon_card": None,
                "title_card": QLabel("IPv4 Address"),
                "img_card": None,
                "corps_card": LineUpdate(
                    input_obj=QLineEdit(self.objManager.ipv4),
                    action_obj=RoundedBtn(
                        icon=qtawesome.icon("mdi6.pencil"), text=None, parent=self
                    ),
                ),
            },
            {
                "icon_card": None,
                "title_card": QLabel("IPv4 Mask"),
                "img_card": None,
                "corps_card": LineUpdate(
                    input_obj=QLineEdit(self.objManager.maskIpv4),
                    action_obj=RoundedBtn(
                        icon=qtawesome.icon("mdi6.pencil"), text=None, parent=self
                    ),
                ),
            },
            {
                "icon_card": None,
                "title_card": QLabel("IPv6 Address"),
                "img_card": None,
                "corps_card": LineUpdate(
                    input_obj=QLineEdit(self.objManager.ipv6),
                    action_obj=RoundedBtn(
                        icon=qtawesome.icon("mdi6.pencil"), text=None, parent=self
                    ),
                ),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Gateway"),
                "img_card": None,
                "corps_card": LineUpdate(
                    input_obj=QLineEdit(self.objManager.gateway),
                    action_obj=RoundedBtn(
                        icon=qtawesome.icon("mdi6.pencil"), text=None, parent=self
                    ),
                ),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Nom de Domaine"),
                "img_card": None,
                "corps_card": LineUpdate(
                    input_obj=QLineEdit(self.objManager.dns),
                    action_obj=RoundedBtn(
                        icon=qtawesome.icon("mdi6.pencil"), text=None, parent=self
                    ),
                ),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Creation Date"),
                "img_card": None,
                "corps_card": QLineEdit(
                    self.objManager.clockManager.conv_unix_to_datetime(
                        self.objManager.clockManager.clockCreated
                    )
                ),
            },
            {
                "icon_card": None,
                "title_card": QLabel("Update Date"),
                "img_card": None,
                "corps_card": QLineEdit(
                    self.objManager.clockManager.conv_unix_to_datetime(
                        self.objManager.clockManager.get_clock_last()
                    )
                ),
            },
        ]


class DevicesCards(CardStackGeneral):
    def __init__(
        self,
        obj_title: str,
        obj_lang: LanguageApp,
        obj_view: Network,
        obj_icon: IconsApp,
        parent=None,
    ):
        super().__init__(obj_title, obj_lang, obj_view, parent)

    def setCardList(self):
        self.card_list = []
        img_default = QImage(
            "C:\\Users\\g.tronche\\Documents\\GitHub\\affinity\\svg\\circle\\gray\\c_client.svg"
        )

        if self.objManager.devicesList is not []:
            for device in self.objManager.devicesList:
                var_path = os.path.join(
                    os.path.dirname(os.path.dirname(self.objManager.absPath)),
                    "desktop",
                    f"{device}.json",
                )
                if os.path.exists(var_path):
                    with open(var_path, "r") as f:
                        device_data = json.load(f)
                        ipv4 = (
                            device_data.get("ipv4", "value unknown") or "value unknown"
                        )
                        name = (
                            device_data.get("name", "value unknown") or "value unknown"
                        )
                        self.card_list.append(
                            {
                                "icon_card": None,
                                "title_card": QLabel(f"{name}({ipv4})"),
                                "img_card": img_default.scaled(
                                    50, 50, Qt.KeepAspectRatio
                                ),
                                "corps_card": QLabel(
                                    f"Mac Address: {device_data.get('mac', 'value unknown') or 'value unknown'}"
                                ),
                            }
                        )
        else:
            self.card_list.append(
                {
                    "icon_card": None,
                    "title_card": QLabel("No device found"),
                    "img_card": None,
                    "corps_card": QLabel("No device found"),
                }
            )


class PaletteIconSettings(CardStackGeneral):
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
                            icon=qtawesome.icon("mdi6.pencil"), text=None, parent=self
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
                "icon_card": qtawesome.icon("mdi6.palette-advanced"),  # QIcon
                "title_card": cardTtl,  # QLabel
                "img_card": cardImg,  # QImage
                "corps_card": cardOpt,  # QLabel ou QWidgets
            }

            self.card_list.append(icon_dict)
        logging.info(f"Card list: {len(self.card_list)} item(s)")

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
