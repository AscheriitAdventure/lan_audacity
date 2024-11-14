from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *

import qtawesome as qta
from typing import Optional

from src.components.card.cl_card import Card, CardHeader


# Version 12/11/2024
class CardTemplateView(QWidget):
    def __init__(
            self,
            title: Optional[str | QWidget] = None,
            list_card: Optional[list[Card]] = None,
            parent=None
            ):
        super(CardTemplateView, self).__init__(parent)
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        if title:
            if isinstance(title, str):
                self.title = QLabel(title)
            else:
                self.title = title
            self.layout.addWidget(self.title)

            self.frame = QFrame()
            self.frame.setFrameShape(QFrame.StyledPanel)
            self.layout.addWidget(self.frame)
        
        self.slide_zone = QFrame()
        self.slide_zone_layout = QVBoxLayout()
        self.slide_zone.setLayout(self.slide_zone_layout)

        if list_card:
            for card in list_card:
                self.slide_zone_layout.addWidget(card)

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.slide_zone)
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.layout.addWidget(self.scroll)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    
    ico_topWidget = qta.icon('fa5s.flag')
    list_card = []

    for i in range(10):
        center_widget = QLabel("Contenu de la carte")
        top_widget = CardHeader(title_card=QLabel(f"Titre de la carte {i}"), icon_card=ico_topWidget)
        list_card.append(Card(top_card=top_widget, center_card=center_widget))

    window = CardTemplateView("Title", list_card)
    window.show()

    sys.exit(app.exec_())
