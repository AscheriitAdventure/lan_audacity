from src.views.templates.MosaicsCards.cl_dmc import DynamicsMosaicsCards as DMC

from qtpy.QtWidgets import QLabel, QLineEdit, QPushButton
import qtawesome as qta

from src.classes.languageApp import LanguageApp
from src.classes.cl_network import Network

from src.views.templatesViews import LineUpdate

"""
    Nom complet: Nertwork General Dynamics Mosaics Cards
    Description: Cette classe est une mise à jour de 'NetworkGeneral(CardStackGeneral)'
    Nouveau nom: NetworkGeneralDMC
"""


class NetworkGeneralDMC(DMC):
    def __init__(
        self, obj_title: str, obj_lang: LanguageApp, obj_view: Network, parent=None
    ):
        super().__init__(obj_title, obj_lang, obj_view, parent)

    def setCardList(self):
        btn_edit = QPushButton(self)
        btn_edit.setIcon(qta.icon("mdi6.pencil"))
        self.card_list = [
            {
                "top_card": QLabel("IPv4 Address"),
                "center_card": LineUpdate(
                    input_obj=QLineEdit(self.objManager.ipv4),
                    action_obj=btn_edit
                )
            },
            {
                "top_card": QLabel("IPv4 Mask"),
                "center_card": LineUpdate(
                    input_obj=QLineEdit(self.objManager.maskIpv4),
                    action_obj=btn_edit
                )
            },
            {
                "top_card": QLabel("IPv6 Address"),
                "center_card": LineUpdate(
                    input_obj=QLineEdit(self.objManager.ipv6),
                    action_obj=btn_edit
                )
            },
            {
                "top_card": QLabel("Gateway"),
                "center_card": LineUpdate(
                    input_obj=QLineEdit(self.objManager.gateway),
                    action_obj=btn_edit
                )
            },
            {
                "top_card": QLabel("Domain Name"),
                "center_card": LineUpdate(
                    input_obj=QLineEdit(self.objManager.dns),
                    action_obj=btn_edit
                )
            },
            {
                "top_card": QLabel("Creation Date"),
                "center_card": QLineEdit(
                    self.objManager.clockManager.conv_unix_to_datetime(
                        self.objManager.clockManager.clockCreated
                    )
                )
            },
            {
                "top_card": QLabel("Update Date"),
                "center_card": QLineEdit(
                    self.objManager.clockManager.conv_unix_to_datetime(
                        self.objManager.clockManager.get_clock_last()
                    )
                )
            },
        ]
