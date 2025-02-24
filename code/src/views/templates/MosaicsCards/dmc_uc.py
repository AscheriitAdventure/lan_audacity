from src.views.templates.MosaicsCards.cl_dmc import DynamicsMosaicsCards as DMC

from qtpy.QtWidgets import QLabel
from qtpy.QtGui import QImage
from qtpy.QtCore import Qt
import json
import os

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
                                "top_card": QLabel(f"{name}({ipv4})"),
                                "left_card": CardImage(img_default.scaled(50, 50, Qt.KeepAspectRatio)),
                                "center_card": QLabel(
                                    f"Mac Address: {device_data.get('mac', 'value unknown') or 'value unknown'}"
                                ),
                            }
                        )
        else:
            self.card_list.append(
                {
                    "center_card": QLabel("No device found")
                }
            )

