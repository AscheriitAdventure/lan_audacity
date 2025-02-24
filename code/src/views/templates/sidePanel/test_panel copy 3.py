import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon
from PySide6.QtCore import *
import qtpy
import qtpy.QtCore


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre principale
        self.setWindowTitle("Jarvis Open")
        self.resize(800, 600)

        # Étape 2 : Ajouter un QLabel au centre
        central_label = QLabel("Jarvis Open", self)
        central_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(central_label)

        # Étape 3 : Ajouter le premier DockWidget (Boite 1)
        self.dock1 = QDockWidget("Boite 1", self)
        self.dock1.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        self.dock1_label = QLabel("Boite 1")
        self.dock1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dock1.setWidget(self.dock1_label)
        self.dock1.setWindowIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxWarning))  # Ajouter une icône au self.dock1
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock1)

        # Étape 4 : Ajouter le deuxième DockWidget (Boite 2)
        dock2 = QDockWidget("Boite 2", self)
        dock2.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        dock2.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        dock2_label = QLabel("Boite 2")
        dock2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dock2.setWidget(dock2_label)
        dock2.setWindowIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxWarning))  # Ajouter une icône au dock2
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock2)

        # Étape 5 : Mettre les docks en onglets
        self.tabifyDockWidget(self.dock1, dock2)

        # Étape 6 : Positionner les onglets à gauche
        self.setTabPosition(Qt.DockWidgetArea.LeftDockWidgetArea, QTabWidget.TabPosition.West)

        # Connecter l'événement qui gère le changement de texte en icône
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        """
        Gère l'événement quand les docks se superposent et remplace le texte par l'icône.
        """
        if isinstance(obj, QTabWidget) and event.type() == QEvent.Type.Paint:
            # Vérifier si les docks sont superposés
            self.dock1 = self.findChild(QDockWidget, "Boite 1")
            dock2 = self.findChild(QDockWidget, "Boite 2")

            if self.dock1 and dock2:
                # Lorsque les docks sont superposés (tabify)
                tab_bar = obj
                if tab_bar.count() > 1:  # Il y a plus d'un onglet
                    # Remplacer le texte par l'icône du windowIcon
                    tab_bar.setTabIcon(0, self.dock1.windowIcon())  # Remplacer par l'icône de Boite 1
                    tab_bar.setTabIcon(1, dock2.windowIcon())  # Remplacer par l'icône de Boite 2
                    tab_bar.setTabToolTip(0, "Boite 1")  # Ajouter une info-bulle
                    tab_bar.setTabToolTip(1, "Boite 2")  # Ajouter une info-bulle
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
