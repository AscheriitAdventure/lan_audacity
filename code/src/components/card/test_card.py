from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from cl_card import Card, CardHeader
import qtawesome as qta

# from src.components.card.cl_card import Card

if __name__ == "__main__":
    app = QApplication([])

    # Création des widgets pour les différentes parties de la carte
    ico_topWidget = qta.icon('fa5s.flag')
    top_widget = CardHeader(title_card=QLabel("Titre de la carte"), icon_card=ico_topWidget)
    left_widget = QPushButton("Bouton de gauche")
    center_widget = QLabel("Contenu de la carte")
    right_widget = QPushButton("Bouton de droite")
    bottom_widget = QPushButton("Bouton du bas")

    # Création de la carte
    card = Card(
        top_card=top_widget,
        left_card=left_widget,
        center_card=center_widget,
        right_card=right_widget,
        bottom_card=bottom_widget,
    )

    # Mise en place du layout principal
    layout = QVBoxLayout()
    layout.addWidget(card)

    window = QWidget()
    window.setLayout(layout)
    window.show()
    app.exec_()
