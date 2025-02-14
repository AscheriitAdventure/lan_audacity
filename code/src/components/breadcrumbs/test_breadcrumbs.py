from src.components.breadcrumbs.cl_breadcrumbs_2 import QBreadcrumbs
from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *
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
        breadcrumbs = QBreadcrumbs(["Terre", "Europe", "France", "Paris", "Eiffel Tower"],True, self)
        breadcrumbs.setBtnStyle(QBreadcrumbs.BtnStyle.NoStyle)
        breadcrumbs.setSeparator(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowRight))
        layout.addWidget(breadcrumbs)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
