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

        # Créer des QDockWidget avec une icône et un titre personnalisé
        dock1 = self.create_dock("Dock 1", "fa5s.home", "Contenu Dock 1")
        dock2 = self.create_dock("Dock 2", "fa5s.cog", "Contenu Dock 2")
        dock3 = self.create_dock("Dock 3", "fa5s.info", "Contenu Dock 3")

        # Ajouter les docks dans la même zone
        self.addDockWidget(Qt.LeftDockWidgetArea, dock1)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock2)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock3)

        # Configurer la position des onglets pour la zone gauche
        self.setTabPosition(Qt.LeftDockWidgetArea, QTabWidget.West)

        # Activer le mode de tabulation pour regrouper les docks
        self.tabifyDockWidget(dock1, dock2)
        self.tabifyDockWidget(dock2, dock3)

    def create_dock(self, title, icon_name, content_text):
        """
        Crée un QDockWidget avec une icône et un titre personnalisé.
        :param title: Le titre du dock (affiché uniquement dans la barre de titre).
        :param icon_name: Le nom de l'icône QtAwesome.
        :param content_text: Le texte affiché dans le contenu du dock.
        """
        dock = QDockWidget(title, self)

        # Définir une icône pour le dock
        icon = qta.icon(icon_name)
        dock.setWindowIcon(icon)

        # Définir un contenu pour le dock
        dock_content = QLabel(content_text)
        dock.setWidget(dock_content)

        # Masquer l'icône dans la barre de titre et afficher uniquement le titre
        dock.setTitleBarWidget(QLabel(title))

        return dock


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
