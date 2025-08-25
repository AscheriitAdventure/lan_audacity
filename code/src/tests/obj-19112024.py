from qtpy.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
)
from qtpy.QtCore import Qt
import os


class FileHierarchyViewer(QWidget):
    def __init__(self, parent=None):
        super(FileHierarchyViewer, self).__init__(parent)
        self.setWindowTitle("Visualisation Hiérarchique de Fichier")
        self.resize(600, 150)
        
        # Initialiser l'interface
        self.init_ui()

    def init_ui(self):
        """Initialise les widgets et le layout."""
        self.layout = QVBoxLayout(self)
        
        # Label pour afficher la hiérarchie
        self.hierarchy_label = QLabel("Aucun fichier sélectionné.")
        self.hierarchy_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.hierarchy_label)

        # Bouton pour sélectionner un fichier
        self.select_file_button = QPushButton("Sélectionner un fichier")
        self.select_file_button.clicked.connect(self.select_file)
        self.layout.addWidget(self.select_file_button)

    def select_file(self):
        """Ouvre une boîte de dialogue pour sélectionner un fichier et affiche sa hiérarchie."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Sélectionnez un fichier")
        if file_path:
            # Mettre à jour l'étiquette avec la hiérarchie
            hierarchy = self.get_file_hierarchy(file_path)
            self.hierarchy_label.setText(hierarchy)

    def get_file_hierarchy(self, file_path: str) -> str:
        """
        Retourne une chaîne représentant la hiérarchie de fichiers.

        :param file_path: Chemin absolu du fichier sélectionné.
        :return: Hiérarchie formatée (racine > dossier1 > dossier2 > fichier).
        """
        # Normaliser et diviser le chemin en composants
        components = []
        current_path = file_path
        while current_path:
            current_path, tail = os.path.split(current_path)
            if tail:  # Ajouter le composant seulement s'il est non vide
                components.insert(0, tail)

        # Retourner la hiérarchie formatée
        return " > ".join(components)


if __name__ == "__main__":
    app = QApplication([])

    viewer = FileHierarchyViewer()
    viewer.show()

    app.exec()
