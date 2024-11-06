from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QGroupBox,
    QLabel,
)
from PyQt6.QtCore import Qt


class Accordion(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Accordéon avec PyQt6")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Création des sections de l'accordéon
        self.create_section("Section 1", "Contenu de la section 1")
        self.create_section("Section 2", "Contenu de la section 2")
        self.create_section("Section 3", "Contenu de la section 3")

    def create_section(self, title, content):
        # Création du bouton pour ouvrir/fermer la section
        button = QPushButton(title)
        button.setCheckable(
            True
        )  # Rendre le bouton "checkable" pour le comportement toggle
        button.clicked.connect(lambda: self.toggle_section(groupbox))

        # Création du groupbox pour contenir le contenu de la section
        groupbox = QGroupBox()
        groupbox.setLayout(QVBoxLayout())
        groupbox.layout().addWidget(QLabel(content))
        groupbox.setVisible(False)  # Par défaut, la section est fermée

        # Ajout du bouton et du contenu dans le layout principal
        self.layout.addWidget(button)
        self.layout.addWidget(groupbox)

    def toggle_section(self, groupbox):
        # Affiche ou masque la section en fonction de son état actuel
        groupbox.setVisible(not groupbox.isVisible())


if __name__ == "__main__":
    app = QApplication([])
    accordion = Accordion()
    accordion.show()
    app.exec()
