from enum import Enum, auto
from typing import *
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *
import logging
import os
import inspect
from dataclasses import asdict

from src.views.widgets.custom import *
from .tab import Tab
from src.utils.py_to_json import *
from src.models import IconApp, Network, Device, FactoryConfFile
from src.views.widgets import WidgetField, TitleWithActions, Card, CLWIT
from src.utils import prettyKeysList, prettyKeys
from src.views.dialogs import NWD



class NetworkObjectTab(Tab):
    class DomainType(Enum):
        DEVICE = auto()     # Objet créer à partir d'un device brut
        INTERFACE = auto()  # Objet créer à partir d'une box FAI
        VLAN = auto()       # Objet créer à partir d'un device
        OTHER = auto()      # Objet créer à partir de qqch

    """Tab for network objects like devices, interfaces etc."""

    def __init__(self, object_data: Optional[Dict] = None, parent=None):
        super().__init__(parent, Tab.TabType.NETWORK,object_data.get('name', 'Network Object'))
        self.rootData = object_data
        self.stackedWidgetList: List[QWidget] = list()
        self.domainType: NetworkObjectTab.DomainType = self.DomainType.OTHER

        self.initUI()
        self._loadData()

    def initUI(self):
        # Main layout
        self.mainLayout = QGridLayout(self)
        self.setLayout(self.mainLayout)
        self.mainLayout.setContentsMargins(0, 5, 0, 0)

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
        self._zone2.setContentsMargins(0, 5, 0, 0)
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
        
        tmp_object = FactoryConfFile(os.getenv("TEMPLATES_TAB"), FactoryConfFile.RWX.READ)
        tmp_object.read_file()

        if domain_type == 'interfaces':
            self.domainType = self.DomainType.INTERFACE
            self.templateTabManager = tmp_object.getOneDict("stacked_title", "Network Tab")
            
        elif domain_type == 'desktop':
            self.domainType = self.DomainType.DEVICE
            self.templateTabManager = tmp_object.getOneDict("stacked_title", "Device Tab")
        else:
            self.domainType = self.DomainType.OTHER
            self.templateTabManager = tmp_object.getOneDict("stacked_title", "Default Tab")

        self._loadStackData(self.templateTabManager)

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
            btn.clicked.connect(lambda checked=False, index=i: self.showField(index)())
            btn_list.append(btn)

            sdfot = WidgetField(self.debug)
            sdfot.setGridForm(WidgetField.GridForm.CMosaics, 5)
            ttl_d = TitleWithActions(title=f.get("title", ""), parent=sdfot)

            sdfot.setHeaderArea(ttl_d)
            # Ajout des cartes
            logging.debug(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}::{inspect.currentframe().f_lineno}: {f}")
            m = self.__loadCardObject(f)

            for i in m:
                tmp: dict = {
                    "layout": {
                        "columnSpan": 1,
                        "rowSpan": 1,
                        "row": 1,
                        "column": 1,
                        "alignment": Qt.AlignmentFlag.AlignLeft
                    }
                }
                if isinstance(i, CCT):
                    tmp["layout"]["rowSpan"] = 2
                    tmp["layout"]["columnSpan"] = 2
                # elif isinstance(i, CCF):
                #     tmp["layout"]["rowSpan"] = 2

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
        tmp_d2 = dict()
        tmp_d2["stack_name"] = stack_name
        tmp_d2["title"] = self.rootData.get("name")
        tmp_d2["debug"] = self.debug
        tmp_d2["parent"] = self

        tmp_d = dict()
        tmp_d["alias"] = self.rootData.get("name")
        tmp_d["path"] = self.rootData.get("path")
        tmp_d["name_file"] = self.rootData.get("uuid")
        obj_class: Any = None

        if self.domainType == self.DomainType.INTERFACE:
            obj_class: Network = Network.from_dict(tmp_d)
            tmp_d2["data_form"] = obj_class
            logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}::{inspect.currentframe().f_lineno}: {self.DomainType.INTERFACE},{stack_name.lower()}")

            if isinstance(obj["fields"], list):
                if stack_name.lower() == "dashboard":
                    obj["fields"].append(tmp_d2)
                    ls_c.extend(self._generateCardFromObject(obj_class))
                for i, c in enumerate(obj["fields"]):
                    if (c.get("format") == "cct" and c.get("title") == "Local Area Network"):
                        obj["fields"][i]["key_table"] = prettyKeysList(Device())
                        obj["fields"][i]["data_table"] = [data.get_dict() for data in obj_class.get_devices()]

                    if (c.get("format") == "ccfb" and c.get("title") == "Operating System Action List"):
                        btn_runnable_all = QPushButton("All")
                        btn_runnable_all.clicked.connect(self.run_all)

                        btn_runnable_nmap = QPushButton("Runnable Nmap")
                        btn_runnable_nmap.clicked.connect(self.run_nmap)

                        btn_runnable_icmp = QPushButton("ICMP")
                        btn_runnable_icmp.clicked.connect(self.run_icmp)

                        btn_runnable_snmp = QPushButton("SNMP")
                        btn_runnable_snmp.clicked.connect(self.run_snmp)

                        btn_runnable_wireshark = QPushButton("Wireshark")
                        btn_runnable_wireshark.clicked.connect(self.run_wireshark)

                        btn_runnable_generate_map = QPushButton("Generate Map")
                        btn_runnable_generate_map.clicked.connect(self.run_generate_map)

                        obj["fields"][i]["data_form"]["runnable_all"] = btn_runnable_all
                        obj["fields"][i]["data_form"]["runnable_nmap"] = btn_runnable_nmap
                        obj["fields"][i]["data_form"]["runnable_icmp"] = btn_runnable_icmp
                        obj["fields"][i]["data_form"]["runnable_snmp"] = btn_runnable_snmp
                        obj["fields"][i]["data_form"]["runnable_wireshark"] = btn_runnable_wireshark
                        obj["fields"][i]["data_form"]["runnable_generate_map"] = btn_runnable_generate_map
                
                    if (c.get("format") == "ccf" and c.get("title") == "Status of the Runnable Actions"):
                        # Créer des QLineEdit pour chaque statut
                        status_nmap = QLineEdit("Non Renseigné")
                        status_nmap.setReadOnly(True)

                        status_icmp = QLineEdit("Non Renseigné")
                        status_icmp.setReadOnly(True)

                        status_snmp = QLineEdit("Non Renseigné")
                        status_snmp.setReadOnly(True)

                        status_oid = QLineEdit("Non Renseigné")
                        status_oid.setReadOnly(True)

                        status_wireshark = QLineEdit("Non Renseigné")
                        status_wireshark.setReadOnly(True)

                        status_generate_map = QLineEdit("Non Renseigné")
                        status_generate_map.setReadOnly(True)

                        obj["fields"][i]["data_form"]["status_nmap"] = status_nmap
                        obj["fields"][i]["data_form"]["status_icmp"] = status_icmp
                        obj["fields"][i]["data_form"]["status_snmp"] = status_snmp
                        obj["fields"][i]["data_form"]["status_oid"] = status_oid
                        obj["fields"][i]["data_form"]["status_wireshark"] = status_wireshark
                        obj["fields"][i]["data_form"]["status_generate_map"] = status_generate_map
    
            else:
                logging.debug(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}::{inspect.currentframe().f_lineno}: {obj.get('fields')}")

        
        elif self.domainType == self.DomainType.DEVICE:
            obj_class: Device = Device.from_dict(tmp_d)
            tmp_d2["data_form"] = obj_class
            logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {self.DomainType.DEVICE}")
            if isinstance(obj["fields"], list):
                obj['fields'].append(tmp_d)
            else:
                obj["fields"] = [tmp_d]
        
        else:
            obj_class: None = None
            tmp_d2["data_form"] = []
            logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {self.DomainType.OTHER}")

        for f_c in obj["fields"]:
            if f_c.get("format") == "cct":
                c = CCT(
                    title=f_c.get("title"),
                    key_table=f_c.get("key_table"),
                    data_table=f_c.get("data_table", None),
                    debug=self.debug,
                    parent=self)
                c.setFilterPanel(f_c.get("filter_panel", False))
                c.setExportBtn(f_c.get("export_btn", False))
                ls_c.append(c)
                logging.info(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {c}")

            elif f_c.get("format") == "ccf":
                c = CCF(
                    title=f_c.get("title"),
                    data_form=f_c.get("data_form", None),
                    debug=self.debug,
                    parent=self)
                ls_c.append(c)
                logging.info(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {c}")

            elif f_c.get("format") == "ccfb":
                c = CCFB(
                    title=f_c.get("title"),
                    data_form=f_c.get("data_form", None),
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

        origin_d: dict = dict()
        origin_d["title"] = obj.__class__.__name__
        origin_d["debug"] = self.debug
        origin_d["parent"] = self.parent()
        origin_d["data_form"] = asdict(obj) if hasattr(
            obj, '__dataclass_fields__') else obj.__dict__.copy()
        # Parcours des attributs de l'objet
        for attr_name, attr_value in obj.__dict__.items():
            # Construit le titre avec le préfixe si fourni
            tmp_d = dict()
            tmp_d["title"] = f"{title_prefix} {attr_name}" if title_prefix else prettyKeys(
                origin_d["data_form"])[attr_name]
            tmp_d["debug"] = self.debug
            tmp_d["parent"] = parent

            logging.info(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}::{inspect.currentframe().f_lineno}: {attr_name} - {attr_value}")

            # Traitement selon le type d'attribut
            if isinstance(attr_value, dict) or inspect.isclass(attr_value) or hasattr(attr_value, '__dataclass_fields__'):
                origin_d["data_form"].pop(attr_name)
                logging.info(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {attr_name} - {attr_value}")
                # Création d'une carte de type formulaire pour les dictionnaires ou classes
                tmp_d["data_form"] = attr_value
                card = CCF(**tmp_d)
                card.setUpdateBtn(True)
                cards.append(card)

            elif isinstance(attr_value, (list, tuple)):
                origin_d["data_form"].pop(attr_name)
                # Création d'une carte de type tableau pour les listes ou tuples
                tmp_d["key_table"] = prettyKeysList(attr_value[0]) if len(attr_value) > 0 else ['column 0']
                tmp_d["data_table"] = attr_value if len(attr_value) > 0 else None
                card = CCT(**tmp_d)
                card.setFilterPanel(True)
                card.setExportBtn(True)
                logging.info(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}::{inspect.currentframe().f_lineno}: {attr_name} - {attr_value}")
                cards.append(card)

            else:
                # Pour les autres types, vous pouvez choisir de créer une carte ou de l'ignorer
                logging.debug(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Ignoring attribute {attr_name} of type {type(attr_value)}")

        card = CCF(**origin_d)
        cards.append(card)

        return cards

    ####### TESTS #######
    def run_nmap(self):
        """
        Lance un scan Nmap sur le réseau et affiche une boîte de dialogue de progression.
        """
        tmp_d = dict()
        tmp_d["alias"] = self.rootData.get("name")
        tmp_d["path"] = self.rootData.get("path")
        tmp_d["name_file"] = self.rootData.get("uuid")
        obj_class: Network = Network.from_dict(tmp_d)
        # Création et affichage de la boîte de dialogue
        dialog = NWD(obj_class, self, self.debug)

        # Mise à jour du statut avant de lancer le scan
        self._update_action_status("nmap", "In Progress")

        # Lancement du scan
        dialog.start_scan()

        # Affichage modal (bloque jusqu'à ce que le scan soit terminé ou annulé) je souhaite l'inverse
        result = dialog.exec_()

        if result == QDialog.DialogCode.Accepted:
            # Le scan s'est terminé avec succès
             self._loadData()  # Recharger les données
        else:
            # Le scan a été annulé
            self._update_action_status("nmap", "Cancelled")

    def _update_action_status(self, action_name, status):
        """
        Met à jour le statut d'une action dans la carte "Status of the Runnable Actions".

        Args:
            action_name (str): Nom de l'action (nmap, icmp, snmp, etc.)
            status (str): Nouveau statut (In Progress, Completed, Cancelled, etc.)
        """
        status_field_name = f"status_{action_name}"

        # Parcourir les widgets empilés pour trouver la carte de statut
        for i in range(self._zone2.count()):
            widget = self._zone2.widget(i)

            for card in widget.findChildren(CCF):
                if card.headerPanel._title.text == "Status of the Runnable Actions":
                    # Si le widget utilise CustomCardForm, on utilise edit_widgets
                    if hasattr(card, "edit_widgets") and status_field_name in card.edit_widgets:
                        widget = card.edit_widgets[status_field_name]
                        if isinstance(widget, QLineEdit) or isinstance(widget, QLabel):
                            widget.setText(status)
                    # Sinon on vérifie l'ancienne structure data_form
                    elif hasattr(card, "data_form") and status_field_name in card.data_form:
                        widget = card.data_form[status_field_name]
                        if isinstance(widget, QLineEdit) or isinstance(widget, QLabel):
                            widget.setText(status)
                    break

    def run_icmp(self):
        pass

    def run_snmp(self):
        pass

    def run_wireshark(self):
        pass

    def run_generate_map(self):
        # Ici on donne un type de device pour chaque device enregistré
        # 1 - scan de ports, os, hop, etc...
            # nmap -sS -sU -T4 -A -v -PE -PP -PS80,443 -PA3389 -PU40125 -PY -g 53 --script "default or (discovery and safe)" <ip/cidr>
        # 2 - on cherche un ou plusieurs mots clés puis on distribue les devices dans les couches OSI
        # 3 - on supprime nativement tous les devices qui ne sont pas dans les couches OSI 1-3
        # 4 - on alimente un fihier de données qui sera ensuite utilisé pour générer la carte 
        pass

    def run_all(self):
        pass
