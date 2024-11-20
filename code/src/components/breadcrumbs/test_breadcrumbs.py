from src.components.breadcrumbs.cl_breadcrumbs import QBreadcrumbs as QBreadcrumbsTVU1  # Importation de la classe QBreadcrumbs
from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
import sys
import logging


# Configuration de logging
logging.basicConfig(level=logging.INFO)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exemple de Breadcrumbs")
        self.resize(400, 100)

        # Layout principal
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # Ajout de la classe Breadcrumbs
        breadcrumbs = QBreadcrumbsTVU1(parent=self)
        layout.addWidget(breadcrumbs)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
