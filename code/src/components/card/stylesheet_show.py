from stylesheet_test import StyleableCard, CCWStyleable, CCWVU1
from qtpy.QtWidgets import *
from qtpy.QtGui import QColor
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = QWidget()
    layout = QVBoxLayout()
    window.setLayout(layout)
    
    color = QColor(192, 192, 192)
    card = CCWStyleable(border_radius=10)
    card.setBorderStyle(color, 2)
    card.set_background_color(color)
    layout.addWidget(card)

    top_widget = QLabel("Titre de la carte")
    left_widget = QPushButton("Bouton de gauche")
    center_widget = QLabel("Contenu de la carte")
    right_widget = QPushButton("Bouton de droite")
    bottom_widget = QPushButton("Bouton du bas")

    # Création de la carte
    card2 = CCWVU1(
        top_card=top_widget,
        left_card=left_widget,
        center_card=center_widget,
        right_card=right_widget,
        bottom_card=bottom_widget,
    )
    layout.addWidget(card2)

    window.show()
    
    sys.exit(app.exec_())