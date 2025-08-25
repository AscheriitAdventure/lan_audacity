from src.views.templates.MosaicsCards.cl_dmc import DynamicsMosaicsCards as DMC

from qtpy.QtWidgets import *
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
                tmp:dict = dict()
                tmp["top_card"] = QLabel(f"{uc.nameObj}({uc.ipv4})", self)
                tmp["left_card"] = CardImage(img_default.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio), self)
                qw_c = QWidget(self)
                c_card = QFormLayout()
                c_card.setContentsMargins(0, 0, 0, 0)
                c_card.setSpacing(0)
                c_card.addRow(QLabel("Name: "), QLabel(uc.nameObj))
                c_card.addRow(QLabel("IP Address: "), QLabel(uc.ipv4))
                c_card.addRow(QLabel("Mac Address: "), QLabel(uc.macAddress))
                c_card.addRow(QLabel("Vendor: "), QLabel(uc.vendor))
                c_card.addRow(QLabel("Type Name: "), QLabel(uc.type.categoryName))
                
                logging.info(f"{__class__.__name__}::{inspect.currentframe().f_code.co_name}: Os List: {len(uc.nmapInfos.osList)}")
                if len(uc.nmapInfos.osList) > 0:
                    # affiche l'os le plus proche de 100 si disponible
                    os_list = uc.nmapInfos.osList
                    os_list.sort(key=lambda x: x.osAccuracy, reverse=True)
                    os_list = os_list[0]
                    os_list = os_list.osName
                    
                qw_c.setLayout(c_card)
                tmp["center_card"] = qw_c
                self.card_list.append(tmp)
        else:
            self.card_list.append(
                {
                    "center_card": QLabel("No device found")
                }
            )

