import logging
import typing
from typing import List, Optional
import inspect
from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *

import qtawesome as qta


"""
    Customs List Widget :
    - Icone et Texte: aura une fonctionnalité qui permettra d'avoir une icone  ou icone et texte
    - Style Accordeon: aura une fonctionnalité qui permettra de déplier ou replier les éléments de la liste
    - Option: Possibilité de Recherche

    Consignes:
        Nom Complet: Custom List Widget Icon & Text Update 1
        Outils de support:
            - QtPy(PyQt6)
            - logging
            - nom de la classe: CLWIconTextU1
        Etape 1:
            - Créer une classe CLWIconTextU1 qui hérite de QWidget [OK]
            - Icone et Texte: aura une fonctionnalité qui permettra d'avoir une icone  ou icone et texte [OK]
            - Style Accordeon: aura une fonctionnalité qui permettra de déplier ou replier les éléments de la liste [OK]
            - Option: Possibilité de Recherche [En cours...]

"""


class CLWIT(QWidget):
    """
        Nom complet: Custom List Widget Icon & Text Update 2
    """
    def __init__(
            self,
            list_objets: Optional[List[QPushButton]] = None,
            toggle: bool = False,
            search: bool = False,
            debug: bool = False,
            parent=None
        ):
        super(CLWIT, self).__init__(parent)
        
        self.listObj: List[QPushButton] = list_objets[:] if list_objets else []
        self.storedText: List[str] = []
        self.debug: bool = debug

        self.search_panel: bool = search
        self.toggle_icon: bool = toggle

        self._loadUI()

    def _loadUI(self):
        self.clwit_layout = QVBoxLayout(self)
        self.setLayout(self.clwit_layout)

        if self.search_panel:
            sp = SearchPanel(self)
            sp.searchBtn.clicked.connect(lambda: self.search(sp.searchInput.text()))
            self.clwit_layout.addWidget(sp)
            
        if self.toggle_icon:
            tb = ToggleBtn(self)
            tb.clicked.connect(self.toggle)
            self.add_btn(tb)
    
    def search(self, text: str):
        for i in range(len(self.listObj)):
            if text.lower() in self.storedText[i].lower():
                self.listObj[i].show()
            else:
                self.listObj[i].hide()
    
    def add_btn(self, btn: QPushButton):
        if btn.text() and len(btn.text()) > 1:
            if btn.icon().isNull():
                logging.info(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Button has no icon")
                w = btn.text().split()

                if len(w) == 1:
                    logging.info(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Button has one caracter")
                    icntxt = w[0][:2].upper()

                else:
                    logging.info(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Button has multiple words")
                    icntxt = ''.join(word[0].upper() for word in w[:4])
                pm = QPixmap(32, 32)
                pm.fill(Qt.GlobalColor.transparent)
                pt = QPainter(pm)
                pt.setPen(Qt.GlobalColor.black)
                pt.setFont(QFont('Arial', 18, QFont.Weight.Bold))
                pt.drawText(pm.rect(), Qt.AlignmentFlag.AlignCenter, icntxt)
                pt.end()

                btn.setIcon(QIcon(pm))

            btn.setIconSize(QSize(32, 32))
            self.clwit_layout.addWidget(btn)
            self.listObj.append(btn)
            self.storedText.append(btn.text())

        elif self.debug:
            logging.error(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Button must have text")
    
    def toggle(self):
        if self.listObj and len(self.listObj) == len(self.storedText):
            if self.listObj[0].text() == "":
                for i in range(len(self.listObj)):
                    self.listObj[i].setText(self.storedText[i])
            else:
                for i in range(len(self.listObj)):
                    self.listObj[i].setText("")
        elif self.debug:
            logging.error(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: ListObj and StoredText are not synchronized!")

    def remove_btn(self, btn: QPushButton):
        if btn in self.listObj:
            index = self.listObj.index(btn)
            self.listObj.remove(btn)
            self.storedText.pop(index)
            self.clwit_layout.removeWidget(btn)
            btn.deleteLater()


class ToggleBtn(QPushButton):
    def __init__(self, parent=None):
        super(ToggleBtn, self).__init__(parent)

        self.setIcon(qta.icon("mdi6.swap-horizontal-bold"))
        self.setText("Extends")
        self.setToolTip("Toggle Icon")
        self.setFlat(True)
        self.setIconSize(QSize(32, 32))


class SearchPanel(QWidget):
    def __init__(self, parent=None):
        super(SearchPanel, self).__init__(parent)

        self.searchPanelLayout = QFormLayout(self)
        self.setLayout(self.searchPanelLayout)

        self.searchInput = QLineEdit()
        self.searchInput.setPlaceholderText("Search")

        self.searchBtn = QPushButton()
        self.searchBtn.setIcon(qta.icon("mdi6.magnify"))
        self.searchBtn.setToolTip("Search")

        self.searchPanelLayout.addRow(self.searchInput, self.searchBtn)

