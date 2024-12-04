from qtpy.QtWidgets import *
from qtpy.QtCore import Qt
import qtawesome as qta


"""
    IMPORTANT: NE PAS EFFACER OU MODIFIER CE FICHIER
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Icônes dans les onglets des docks")
        self.resize(800, 600)

        icon_cog = qta.icon("mdi6.cog")
        icon_home = qta.icon("fa5s.home")
        icon_info = qta.icon("fa5s.info")

        btn = QPushButton(self)
        btn.setIcon(icon_cog)

        dock_1 = QDockWidget(self)
        dock_1.setWindowIcon(icon_cog)
        dock_1.setWindowTitle(" ")

        dock_1.setWidget(btn)

        dock_2 = QDockWidget(self)
        dock_2.setWindowIcon(icon_home)
        dock_2.setWindowTitle(" ")

        # Ajouter les docks
        self.addDockWidget(Qt.LeftDockWidgetArea, dock_1)
        self.addDockWidget(Qt.RightDockWidgetArea, dock_2)

        # Activer l'option pour afficher les icônes dans les onglets des docks
        self.setTabPosition(Qt.LeftDockWidgetArea, QTabWidget.West)
        self.setDockOptions(QMainWindow.AllowTabbedDocks | QMainWindow.AnimatedDocks)
        self.tabifyDockWidget(dock_1, dock_2)


if __name__ == "__main__":
    app = QApplication([])
    # app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    app.exec_()
