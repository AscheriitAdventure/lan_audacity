from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout

class Card(QWidget):
    def __init__(self, title, description, parent=None):
        super().__init__(parent)
        self.title = title
        self.description = description
        self.init_ui()

    def init_ui(self):
        # Création des éléments de la carte
        title_label = QLabel(self.title)
        description_label = QLabel(self.description)
        button = QPushButton("Cliquez ici")

        # Layout vertical pour organiser les éléments de la carte
        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addWidget(button)

        # Définit le layout de la carte
        self.setLayout(layout)

class CardGrid(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Création d'un layout grid pour organiser les cartes
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        # Création de plusieurs cartes et ajout dans le grid layout
        for i in range(3):
            for j in range(3):
                card = Card(f"Carte {i*3+j+1}", f"Description de la carte {i*3+j+1}")
                self.grid_layout.addWidget(card, i, j)

        # Activation de la possibilité de drag and drop
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("text/plain"):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        mime_data = event.mimeData()
        data = mime_data.text()
        source_widget = event.source()

        # Vérifie si la source est une carte
        if isinstance(source_widget, Card):
            source_layout = source_widget.parent()
            source_layout.removeWidget(source_widget)
            event.accept()

            # Trouve les coordonnées de la case du grid où l'élément a été lâché
            pos = self.grid_layout.getItemPosition(self.grid_layout.indexOf(self.childAt(event.pos())))
            row, column, *_ = pos

            # Ajoute l'élément à la nouvelle position dans le grid layout
            self.grid_layout.addWidget(source_widget, row, column)

            source_widget.show()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication([])

    # Création de l'ensemble de cartes dans un grid layout
    card_grid = CardGrid()
    card_grid.show()

    app.exec_()
