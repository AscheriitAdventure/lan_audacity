from typing import *
import logging
import inspect

from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *
import qtawesome as qta

from src.models import Device
from src.views.widgets import Card, TitleWithActions


class CustomCardDevice(Card):
    """Carte personnalisée pour afficher un appareil"""

    def __init__(
        self,
        data_form: Union[Device, Dict[str, Any], None] = None,
        debug: Optional[bool] = False,
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(debug, parent)
        self.device_data: Optional[Device] = None

        # Déterminer les informations de base
        if isinstance(data_form, Device):
            self.device_data = data_form
            self.title = data_form.name_object
            self.icon = QIcon(data_form.type_device.pixmap_path) if data_form.type_device else qta.icon("mdi6.desktop-classic")
            self.tool_tip = data_form.web_address.cidr
        elif isinstance(data_form, dict):
            self.title = data_form.get("name_object", "Unknown Device")
            self.icon = data_form.get("img", qta.icon("mdi6.desktop-classic"))
        else:
            self.title = "Unknown Device"
            self.icon = qta.icon("mdi6.desktop-classic")

        # Bouton principal au centre
        self.btnDevice = QPushButton()
        self.btnDevice.setIcon(self.icon)
        self.btnDevice.setIconSize(QSize(64, 64))
        self.btnDevice.setFlat(True)
        self.btnDevice.setText(self.title)
        if self.tool_tip:
            self.btnDevice.setToolTip(self.tool_tip)
        self.btnDevice.clicked.connect(self.openTab)
        self.setPositionCard("center", self.btnDevice)

        # Initialisation du reste de l'UI
        self.initForm()

        logging.debug(
            f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}::{inspect.currentframe().f_lineno}: {self.title}"
        )

    def initForm(self) -> None:
        """Initialise les éléments d’interface supplémentaires (nom + statut)"""

        # Label de statut (ex: connecté / déconnecté)
        self.statusLabel = QLabel("●")
        self.statusLabel.setStyleSheet("color: green; font-size: 16px;")
        self.statusLabel.setFixedWidth(15)

        # Nom de l'appareil
        self.nameLabel = QLabel(self.title)
        self.nameLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.nameLabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # Layout horizontal pour le bas
        bottomWidget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(10)
        layout.addWidget(self.statusLabel)
        layout.addWidget(self.nameLabel)
        layout.addStretch()
        bottomWidget.setLayout(layout)

        self.setPositionCard("bottom", bottomWidget)

    def openTab(self) -> None:
        """Ouvre un onglet de détail pour l'appareil"""
        logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}::{inspect.currentframe().f_lineno}: Ouverture d'un onglet pour : {self.title}")
        # TODO: Intégrer à un gestionnaire d’onglets réel via signal ou callback

    def setStatusColor(self, status: str) -> None:
        """Définit la couleur du point de statut en fonction de l’état"""
        color = {
            "online": "green",
            "offline": "red",
            "warning": "orange"
        }.get(status.lower(), "gray")

        self.statusLabel.setStyleSheet(f"color: {color}; font-size: 16px;")

