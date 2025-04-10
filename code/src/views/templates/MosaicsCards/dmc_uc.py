from src.views.templates.MosaicsCards.cl_dmc import DynamicsMosaicsCards as DMC

from qtpy.QtWidgets import QLabel
from qtpy.QtGui import QImage
from qtpy.QtCore import Qt
import logging, inspect

from src.classes.languageApp import LanguageApp
from src.classes.cl_network import Network
from src.classes.iconsApp import IconsApp

from src.components.card.cl_card import CardImage

"""
    Nom complet: Devices Dynamics Mosaics Cards
    Description: Cette classe est une mise à jour de 'DevicesCards(CardStackGeneral)'
    Nouveau nom: DevicesDMC
"""


class DevicesDMC(DMC):
    def __init__(
        self,
        obj_title: str,
        obj_lang: LanguageApp,
        obj_view: Network,
        obj_icon: IconsApp,
        parent=None,
    ):
        super().__init__(obj_title, obj_lang, obj_view, parent)
        self.objManager: Network

    def setCardList(self):
        self.card_list = []
        img_default = QImage(
            "C:\\Users\\g.tronche\\Documents\\GitHub\\affinity\\svg\\circle\\gray\\c_client.svg"
        )
        devices = self.objManager.get_devices()
        logging.debug(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: {len(devices)}, {len(self.objManager.devicesList)}")
        if len(self.objManager.devicesList) > 0:
            for uc in devices:
                tmp:dict = {}
                tmp["top_card"] = QLabel(f"{uc.nameObj}({uc.ipv4})", self)
                tmp["left_card"] = CardImage(img_default.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio), self)
                tmp["center_card"] = QLabel(f"Mac Address: {uc.macAddress}", self)
                self.card_list.append(tmp)
        else:
            self.card_list.append(
                {
                    "center_card": QLabel("No device found")
                }
            )

