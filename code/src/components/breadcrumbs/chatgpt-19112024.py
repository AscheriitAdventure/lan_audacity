from qtpy.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QPushButton, QLabel, QVBoxLayout
)
from qtpy.QtCore import Signal as pyqtSignal, Qt


class Breadcrumbs(QWidget):
    # Signal déclenché lorsqu'un élément est cliqué
    breadcrumb_clicked = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(1)  # Espace entre les éléments
        self.breadcrumbs = []

    def set_breadcrumbs(self, items):
        """
        Définit les items des breadcrumbs.
        :param items: Liste des noms des breadcrumbs (ex: ["Accueil", "Produits", "Détails"])
        """
        # Nettoyer le layout
        for i in reversed(range(self.layout.count())):
            widget = self.layout.takeAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        self.breadcrumbs = items

        for index, item in enumerate(items):
            # Ajouter le bouton ou label pour l'élément
            button = QPushButton(item, self)
            button.setFlat(True)  # Style plat pour ressembler à un lien
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _, idx=index: self.breadcrumb_clicked.emit(idx))
            self.layout.addWidget(button)

            # Ajouter le séparateur sauf pour le dernier élément
            if index < len(items) - 1:
                separator = QLabel(">")
                self.layout.addWidget(separator)

        self.update()


# Exemple d'utilisation
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exemple de Breadcrumbs")
        self.resize(400, 100)

        # Layout principal
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # Ajout de la classe Breadcrumbs
        self.breadcrumbs = Breadcrumbs(self)
        self.breadcrumbs.set_breadcrumbs(["Accueil", "Produits", "Détails"])
        self.breadcrumbs.breadcrumb_clicked.connect(self.on_breadcrumb_clicked)
        layout.addWidget(self.breadcrumbs)

    def on_breadcrumb_clicked(self, index):
        print(f"Breadcrumb cliqué : {index} ({self.breadcrumbs.breadcrumbs[index]})")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
