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


"""
    Commentaires:
        Je suis bon pour recommencer à zéro.
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

class CLIconTextU1(QWidget):
    def __init__(
            self, 
            list_objets: Optional[List[QPushButton]] = [], 
            toggle_icon: Optional[bool] = False, 
            search_panel: Optional[bool] = False, 
            logger: Optional[bool] = False, 
            parent=None
            ):
        super(CLIconTextU1, self).__init__(parent)
        if logger:
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.DEBUG)

        self.listObj = list_objets
        self.storedText = []
        self.layout = QVBoxLayout(self)

        self.searchPanel: Optional[QWidget] = None

        if search_panel:
            self.set_searchPanel()

        if toggle_icon:
            self.set_toggleIcon()
    
    def add_btn(self, btn: QPushButton):
        if btn.text() and len(btn.text()) > 1:
            # Si btn ne possède pas d'icone alors générer une icone avec:
            if btn.icon().isNull():
                logging.info("Button has no icon")
                words = btn.text().split()
                # -si un seul mot : générer une icone avec les 2 premières lettres du mot
                if len(words) == 1:
                    logging.info("Button has one word")
                    icon_text = words[0][:2].upper()
                else:
                    # -si plusieurs mots : générer une icone avec les premières lettres de chaque mot avec une limite de 4 lettres
                    logging.info("Button has multiple words")
                    icon_text = ''.join(word[0].upper() for word in words[:4])
                
                # Create a QPixmap for the text icon
                pixmap = QPixmap(32, 32)
                pixmap.fill(Qt.transparent)
                
                # Paint text onto the pixmap
                painter = QPainter(pixmap)
                painter.setPen(Qt.black)
                painter.setFont(QFont('Arial', 18, QFont.Bold))
                painter.drawText(pixmap.rect(), Qt.AlignCenter, icon_text)
                painter.end()
                
                btn.setIcon(QIcon(pixmap))

            btn.setIconSize(QSize(32, 32))
            self.layout.addWidget(btn)
            self.listObj.append(btn)
            self.storedText.append(btn.text())
        else:
            logging.error("Button must have text")

    def set_toggleIcon(self):
        btn = QPushButton()
        btn.setIcon(qta.icon("mdi6.swap-horizontal-bold"))
        btn.setText("Extends")
        btn.setToolTip("Toggle Icon")
        btn.clicked.connect(self.toggleIcon)
        self.add_btn(btn)

    def set_searchPanel(self):
        self.searchPanel = QWidget()
        searchPanelLayout = QFormLayout(self.searchPanel)

        searchInput = QLineEdit()
        searchInput.setPlaceholderText("Search")

        searchBtn = QPushButton()
        searchBtn.setIcon(qta.icon("mdi6.magnify"))
        searchBtn.setToolTip("Search")
        searchBtn.clicked.connect(lambda: self.search(searchInput.text()))

        searchPanelLayout.addRow(searchInput, searchBtn)
        self.layout.addWidget(self.searchPanel)

    def toggleIcon(self):
        if self.listObj[0].text() == "":
            if self.searchPanel is not None:
                self.searchPanel.show()
            for i in range(len(self.listObj)):
                self.listObj[i].setText(self.storedText[i])
        else:
            if self.searchPanel is not None:
                self.searchPanel.hide()
            for i in range(len(self.listObj)):
                self.listObj[i].setText("")

    def search(self, text: str):
        for i in range(len(self.listObj)):
            if text.lower() in self.storedText[i].lower():
                self.listObj[i].show()
            else:
                self.listObj[i].hide()
                