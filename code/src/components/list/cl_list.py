import logging
from typing import List, Optional

from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *

import qtawesome as qta


"""
    Customs List Widget :
    - Icone et Texte: aura une fonctionnalité qui permettra d'avoir une icone  ou icone et texte
    - Style Accordeon: aura une fonctionnalité qui permettra de déplier ou replier les éléments de la liste
    - Option: Possibilité de Recherche
"""


class CLWIconText(QWidget):
    def __init__(
        self,
        list_objets: List[dict],
        toggle_icon: Optional[bool] = False,
        search_panel: Optional[bool] = False,
        logger: Optional[bool] = False,
        parent=None,
    ):
        super(CLWIconText, self).__init__(parent)
        if logger:
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.DEBUG)

        self.listObj = list_objets
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.searchPanel: Optional[QWidget] = None

        if toggle_icon:
            self.set_toggleIcon()

        if search_panel:
            self.set_searchPanel()

    def set_listUI(self):
        self.logger.debug(f"Setting List UI: {len(self.listObj)}")
        for obj in self.listObj:
            obj_widget = QWidget()
            obj_layout = QHBoxLayout()
            obj_widget.setLayout(obj_layout)

            obj_icon = QLabel()
            if obj["icon"]:
                obj_icon.setPixmap(obj["icon"])
            else:
                obj_icon.setPixmap(qta.icon("mdi6.loading", color="Blue"))
            obj_layout.addWidget(obj_icon)

            obj_text = QLabel(obj["text"])
            obj_layout.addWidget(obj_text)

            self.layout.addWidget(obj_widget)

    def set_toggleIconFunc(self):
        btn = {
            "icon": qta.icon("mdi6.loading", color="Blue"),
            "text": ["Collapse", "Expand"],
            "action": self.toggleIcon,
        }
        # ajouter à la liste d'objet au rang de zéro sans supprimer les informations déjà existante
        self.listObj.insert(0, btn)

    def set_searchPanelFunc(self):
        searchPanel = QLineEdit()
        searchPanel.setWindowIcon(qta.icon("mdi6.magnify"))

        self.searchPanel = searchPanel
