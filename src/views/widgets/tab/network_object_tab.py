from enum import Enum, auto
from typing import *
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *
import logging
import os
import inspect

from src.views.widgets.custom import *
from .tab import Tab
from src.utils.py_to_json import *
from src.models import IconApp, Network, Device
from src.views.widgets import WidgetField, TitleWithActions, Card, CLWIT
from src.utils import prettyKeysList

FIXED_CARDS: List[Dict[str, Any]] = [
    {
        "stack_name": "Dashboard",
        "format": "cct",
        "title": "Local Area Network",
        "icon": {
            "names": [],
            "options": []
        },
        "filter_panel": True,
        "export_btn": True,
        "key_table": prettyKeysList(Device()),
        "data_table": None,
    },
    {
        "stack_name": "Dashboard",
        "format": "cct",
        "title": "List of network equipments",
        "icon": {
            "names": [],
            "options": []
        },
        "filter_panel": True,
        "export_btn": True,
        "key_table": ["column 0"],
        "data_table": None,
    },
    {
        "stack_name": "Dashboard",
        "format": "cct",
        "title": "Current Problems",
        "icon": {
            "names": [],
            "options": []
        },
        "filter_panel": True,
        "export_btn": True,
        "key_table": ["column 0"],
        "data_table": None,
    },
]


class NetworkObjectTab(Tab):
    class DomainType(Enum):
        DEVICE = auto()     # Objet créer à partir d'un device brut
        INTERFACE = auto()  # Objet créer à partir d'une box FAI
        VLAN = auto()       # Objet créer à partir d'un device
        OTHER = auto()      # Objet créer à partir de qqch

    """Tab for network objects like devices, interfaces etc."""

    def __init__(self, object_data: Optional[Dict] = None, parent=None):
        super().__init__(parent, Tab.TabType.NETWORK,
                         object_data.get('name', 'Network Object'))
        self.rootData = object_data
        self.stackedWidgetList: List[QWidget] = list()
        self.domainType: NetworkObjectTab.DomainType = self.DomainType.OTHER

        self.initUI()
        self._loadData()

    def initUI(self):
        # Main layout
        self.mainLayout = QGridLayout(self)
        self.setLayout(self.mainLayout)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        # Add Scroll Area
        self._loadScrollArea()

        # Add Object 1 --> Custom List Widget Icon Text
        self._zone1 = QWidget()
        self._zone1Layout = QVBoxLayout(self._zone1)
        self._zone1Layout.setContentsMargins(0, 0, 0, 0)
        self.scrollLayout.addWidget(self._zone1, 0, 0, 1, 1)

        # Add Object 2 --> Stacked
        self._zone2 = QStackedWidget(self)
        self._zone2.setMinimumWidth(100)
        self.scrollLayout.addWidget(self._zone2, 0, 1, 1, 1)

    def _loadScrollArea(self):
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.mainLayout.addWidget(self.scrollArea)

        # Create container widget for scroll area
        self.scrollContainer = QWidget()
        self.scrollArea.setWidget(self.scrollContainer)
        self.scrollLayout = QGridLayout(self.scrollContainer)
        self.scrollLayout.setContentsMargins(0, 0, 0, 0)

    def _loadData(self):
        # Définir quel stack utilisé pour l'affichage
        domain_type = os.path.basename(os.path.dirname(self.rootData['path']))
        logging.debug(
            f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Domain type: {domain_type}")

        if domain_type == 'interfaces':
            self.domainType = self.DomainType.INTERFACE
            self._loadStackData(NETWORK_TAB)
        elif domain_type == 'desktop':
            self.domainType = self.DomainType.DEVICE
            self._loadStackData(DEVICE_TAB)
        else:
            self.domainType = self.DomainType.OTHER
            self._loadStackData(DEFAULT_SIDE_PANEL)

    def _loadStackData(self, data: dict):
        btn_list: List[QPushButton] = list()
        fields: List[dict] = data.get("fields", [])

        for i, f in enumerate(fields):
            btn = QPushButton()
            btn.setText(f.get("title", ""))
            btn.setToolTip(f.get("tooltip", ""))
            if icon := f.get("icon"):
                ico = IconApp.from_dict(icon)
                btn.setIcon(ico.get_qIcon())
            btn.setFlat(True)
            btn.clicked.connect(lambda checked=False,
                                index=i: self.showField(index)())
            btn_list.append(btn)

            sdfot = WidgetField(self.debug)
            sdfot.setGridForm(WidgetField.GridForm.CMosaics, 5)
            ttl_d = TitleWithActions(title=f.get("title", ""), parent=sdfot)

            sdfot.setHeaderArea(ttl_d)
            # Ajout des cartes
            m = self.__loadCardObject(f)

            for i in m:
                tmp: dict = {
                    "layout": {
                        "columnSpan": 1,
                        "rowSpan": 1,
                        "row": 1,
                        "column": 1,
                        "alignment": Qt.AlignmentFlag.AlignJustify
                    }
                }
                if isinstance(i, CCT):
                    tmp["layout"]["rowSpan"] = 2
                    tmp["layout"]["columnSpan"] = 2
                elif isinstance(i, CCF):
                    tmp["layout"]["rowSpan"] = 2

                sdfot.addCard(i, tmp)

            self._zone2.addWidget(sdfot)
            self.stackedWidgetList.append(sdfot)

        self._zone2.setCurrentIndex(0)

        logging.debug(
            f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Button list: {btn_list}")
        params = {
            "toggle": True,
            "search": False,
            "parent": self
        }

        if len(btn_list) > 0:
            o = CLWIT(**params)
            for b in btn_list:
                o.add_btn(b)
            self._zone1Layout.addWidget(o)
            self._zone1Layout.addStretch()

    def handleItemSimpleClick(self, data: Dict[str, Any]):
        """
        Gère le clic sur un élément du CLWIT.

        Args:
            item_data (dict): Données de l'élément cliqué avec les clés :
                - name: nom de l'objet 
                - id: identifiant de l'objet 
        """
        pass

    def showField(self, index: int):
        """
        Renvoie une fonction de rappel qui affichera le widget empilé à l'index spécifié.
        Cette méthode est utilisée pour connecter aux signaux de clic de bouton.

        Args:
            index (int): Index du widget empilé à afficher

        Returns:
            function: Fonction de rappel qui affiche le widget empilé spécifié
        """
        def callback():
            if 0 <= index < len(self.stackedWidgetList):
                self._zone2.setCurrentIndex(index)
                logging.debug(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Affichage du champ à l'index {index}")

        return callback

    def __loadCardObject(self, obj: dict) -> list[Card]:
        ls_c: list = list()

        stack_name: str = obj.get('title')
        tmp_d = dict()
        tmp_d["alias"] = self.rootData.get("name")
        tmp_d["path"] = self.rootData.get("path")
        tmp_d["name_file"] = self.rootData.get("uuid")
        obj_class: Network = Network.from_dict(tmp_d)
        logging.debug(
            f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {obj}")
        if "dashboard" in stack_name.lower():
            # Création de la carte principale pour l'objet réseau
            tmp_d = dict()
            tmp_d["stack_name"] = stack_name
            tmp_d["title"] = self.rootData.get("name")
            tmp_d["debug"] = self.debug
            tmp_d["parent"] = self
            tmp_d["data_form"] = obj_class

            FIXED_CARDS.append(tmp_d)

            # Rechercher l'index de la carte "Local Area Network" et mettre à jour son data_table
            for i, card in enumerate(FIXED_CARDS):
                if (card.get("stack_name", "").lower() == stack_name.lower() and card.get("format") == "cct" and card.get("title") == "Local Area Network"):
                    FIXED_CARDS[i]["data_table"] = [data.get_dict() for data in obj_class.get_devices()]
                    break

            # Utilisation de la nouvelle fonction pour créer des cartes à partir des attributs
            ls_c.extend(self._generateCardFromObject(obj_class))

        elif "interfaces" in stack_name.lower():
            logging.info(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}:366: {self.rootData}")

        elif "devices" in stack_name.lower():
            logging.info(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}:367: {self.rootData}")

        elif "vlans" in stack_name.lower():
            logging.info(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}:368: {self.rootData}")

        elif "network map" in stack_name.lower():
            logging.info(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}:369: {self.rootData}")

        for f_c in FIXED_CARDS:
            if f_c.get("stack_name").lower() == stack_name.lower() and f_c.get("format") == "cct":
                c = CCT(
                    title=f_c.get("title"),
                    key_table=f_c.get("key_table"),
                    data_table=f_c.get("data_table"),
                    debug=self.debug,
                    parent=self)
                c.setFilterPanel(f_c.get("filter_panel", False))
                c.setExportBtn(f_c.get("export_btn", False))
                ls_c.append(c)
                logging.info(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {c}")

            elif f_c.get("stack_name") == stack_name and f_c.get("format") == "ccf":
                c = CCF(
                    title=f_c.get("title"),
                    data_form=None,
                    debug=self.debug,
                    parent=self)
                ls_c.append(c)
                logging.info(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {c}")

        return ls_c

    def _generateCardFromObject(self, obj: object, title_prefix: Optional[str] = "", parent=None) -> List[Card]:
        """
        Crée des cartes CCF ou CCT à partir des attributs d'un objet.

        Args:
            obj: L'objet à partir duquel créer les cartes
            title_prefix (str): Préfixe à ajouter aux titres des cartes (optionnel)
            parent: Le widget parent des cartes (par défaut self)

        Returns:
            List[Card]: Liste des cartes créées
        """
        cards: List[Card] = list()
        parent = parent or self

        # Parcours des attributs de l'objet
        for attr_name, attr_value in obj.__dict__.items():
            # Construit le titre avec le préfixe si fourni
            tmp_d = dict()
            tmp_d["title"] = f"{title_prefix} {attr_name}" if title_prefix else attr_name
            tmp_d["debug"] = self.debug
            tmp_d["parent"] = parent

            logging.info(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}:{inspect.currentframe().f_code.co_lines()} {attr_name} - {attr_value}")

            # Traitement selon le type d'attribut
            if isinstance(attr_value, dict) or inspect.isclass(attr_value):
                logging.info(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {attr_name} - {attr_value}")
                # Création d'une carte de type formulaire pour les dictionnaires ou classes
                tmp_d["data_form"] = attr_value
                card = CCF(**tmp_d)
                cards.append(card)

            elif isinstance(attr_value, (list, tuple)):
                # Création d'une carte de type tableau pour les listes ou tuples
                tmp_d["key_table"] = ["column 0"]
                tmp_d["data_table"] = attr_value
                card = CCT(**tmp_d)
                card.setFilterPanel(True)
                card.setExportBtn(True)
                logging.info(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {attr_name} - {attr_value}")
                cards.append(card)

            else:
                # Pour les autres types, vous pouvez choisir de créer une carte ou de l'ignorer
                logging.debug(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Ignoring attribute {attr_name} of type {type(attr_value)}")

        return cards
