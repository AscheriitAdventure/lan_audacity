from enum import Enum, auto
from typing import List, Dict, Optional, Any
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *
import logging
import os
import inspect

from .tab import Tab
from src.utils.py_to_json import *
from src.models import IconApp
from src.views.widgets import *


class NetworkObjectTab(Tab):
    class DomainType(Enum):
        DEVICE = auto() # Objet créer à partir d'un device brut
        INTERFACE = auto() # Objet créer à partir d'une box FAI
        VLAN = auto() # Objet créer à partir d'un device
        OTHER = auto() # Objet créer à partir de qqch

    """Tab for network objects like devices, interfaces etc."""

    def __init__(self, object_data: Optional[Dict] = None, parent=None):
        super().__init__(parent, Tab.TabType.NETWORK, object_data.get('name', 'Network Object'))
        self.rootData = object_data
        self.stackedWidgetList: List[QWidget] = []
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
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.mainLayout.addWidget(self.scrollArea)

        # Create container widget for scroll area
        self.scrollContainer = QWidget()
        self.scrollArea.setWidget(self.scrollContainer)
        self.scrollLayout = QGridLayout(self.scrollContainer)
        self.scrollLayout.setContentsMargins(0, 0, 0, 0)

    def _loadData(self):
        # Définir quel stack utilisé pour l'affichage
        domain_type = os.path.basename(os.path.dirname(self.rootData['path']))
        logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Domain type: {domain_type}")

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
        btn_list: List[QPushButton] = []
        fields: List[dict] = data.get("fields", [])

        for i, f in enumerate(fields):
            btn = QPushButton()
            btn.setText(f.get("title", ""))
            btn.setToolTip(f.get("tooltip", ""))
            if icon := f.get("icon"):
                ico = IconApp.from_dict(icon)
                btn.setIcon(ico.get_qIcon())
            btn.setFlat(True)
            btn.clicked.connect(self.showField(i))
            btn_list.append(btn)
            
            sdfot = WidgetField(self.debug)
            sdfot.setGridForm(WidgetField.GridForm.CMosaics, 5)
        
            sdfot.setHeaderArea(TitleWithActions(title=f.get("title", ""), parent=sdfot))
            for i in range(1,26):
                tmp: dict = {
                    "layout":{
                        "columnSpan": 2,
                        "rowSpan": 1,
                        "row": 1,
                        "column": 1,
                        "alignment": Qt.AlignmentFlag.AlignJustify
                    }
                }
                carte = Card(debug=self.debug)
                carte.setCenterCard(QLabel(str(i)))
                sdfot.addCard(carte,tmp)

            self._zone2.addWidget(sdfot)
            self.stackedWidgetList.append(sdfot)

        self._zone2.setCurrentIndex(0)
        
        logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Button list: {btn_list}")
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
                logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Affichage du champ à l'index {index}")
    
        return callback
    