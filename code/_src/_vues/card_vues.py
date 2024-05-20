from PyQt6.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *
from _src._mdl.mdl_itm import IconItem
from _src._mdl.mdl_managers import IconsManager
import qtawesome as qta
import sys

class IconCard(QWidget):
    def __init__(self, icon, dsc_flag='', parent=None):
        super().__init__(parent)
        self.icon = None
        self.dsc_flag = ''

        if isinstance(icon, QIcon):
            self.icon = icon
            self.dsc_flag = dsc_flag
        elif isinstance(icon, IconItem):
            self.icon = icon.objIcon
            self.dsc_flag = icon.label
        elif isinstance(icon, any):
            self.icon = icon
            self.dsc_flag = dsc_flag

        self.init_card()

    def init_card(self):
        # Création des éléments de la carte
        icon_label = QLabel()
        icon_label.setPixmap(self.icon.pixmap(64, 64))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label = QLineEdit(self.dsc_flag)
        edit_icon = qta.icon('fa5s.paint-brush', color='ForestGreen')
        edit_label = QPushButton(edit_icon, 'Edit')

        layout = QVBoxLayout(self)
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(edit_label)

        self.setLayout(layout)

class IconCardGridView(QWidget):
    def __init__(self, ico_manager: IconsManager, parent=None):
        super().__init__(parent)
        self.iconManager = ico_manager

        # Création d'un layout grid pour organiser les cartes
        grid_layout = QGridLayout()
        widget_layout = QWidget()  # Création d'un widget pour encapsuler le grid layout
        widget_layout.setLayout(grid_layout)

        # Création de plusieurs cartes et ajout dans le grid layout
        nb_row = int(self.iconManager.len_ls() / 5)
        for i in range(nb_row):
            for j in range(5):
                nb_itm = i*5+j
                card = IconCard(self.iconManager.listIcons[nb_itm])
                grid_layout.addWidget(card, i, j, 1, 1)

        # Création de la zone de défilement et ajout du widget à l'intérieur
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Permet à la zone de défilement de s'adapter à la taille du contenu
        scroll_area.setWidget(widget_layout)  # Ajout du widget contenant le grid layout

        # Ajout de la zone de défilement à la disposition principale du widget
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        # Activation de la possibilité de drag and drop
        self.setAcceptDrops(True)


class Card(QWidget):
    def __init__(self, icon_card: QIcon = None, title: QLabel = None, image_path: QImage = None,
                 corps_card: any = None, parent=None):
        super().__init__(parent)
        self.layoutCard = QGridLayout(self)
        self.setLayout(self.layoutCard)

        if icon_card or title:
            self.setTitleUI(icon_card, title)

        if image_path:
            self.setImageUI(image_path)

        if corps_card:
            self.setBodyUI(corps_card)

    def setTitleUI(self, icon_card: QIcon = None, title: QLabel = None):
        hbar_title = QHBoxLayout()
        if icon_card:
            icon_label = QLabel()
            icon_label.setPixmap(icon_card.pixmap(24, 24))
            hbar_title.addWidget(icon_label)

        if title:
            hbar_title.addWidget(title)

        hbar_title.addStretch(1)
        hbar_cnt = QWidget()
        hbar_cnt.setLayout(hbar_title)
        self.layoutCard.addWidget(hbar_cnt, 0, 0, 1, 2, Qt.AlignmentFlag.AlignTop)

    def setImageUI(self, image_path: QImage):
        image_label = QLabel()
        image_label.setPixmap(QPixmap.fromImage(image_path))
        image_label.setAlignment(Qt.AlignCenter)
        self.layoutCard.addWidget(image_label, 1, 0, 1, 2, Qt.AlignmentFlag.AlignHCenter)

    def setBodyUI(self, corps_card: QWidget):
        self.layoutCard.addWidget(corps_card, 2, 0, 1, 2)
