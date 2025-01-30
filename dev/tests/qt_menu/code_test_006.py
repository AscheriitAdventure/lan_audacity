import sys
import json
from qtpy.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QAction,
    QFileDialog,
    QMessageBox,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Projets récents - PyQt6")
        self.resize(800, 600)

        # Attribut pour stocker les projets récents
        self.recent_projects = []
        self.max_recent_projects = 5  # Nombre maximum de projets récents à stocker
        self.recent_file_path = (
            "recent_projects.json"  # Chemin pour stocker les récents
        )

        # Barre de menus
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&Fichier")

        # Action pour ouvrir un projet
        open_action = QAction("&Ouvrir un projet", self)
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)

        # Menu pour les projets récents
        self.recent_menu = QMenu("Projets &Récents", self)
        file_menu.addMenu(self.recent_menu)

        # Charger les récents depuis le fichier
        # self.load_recent_projects()
        # self.update_recent_menu()

    def open_project(self):
        """Ouvre un projet à partir d'un fichier choisi par l'utilisateur."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Ouvrir un projet", "", "Projets (*.json *.txt)"
        )
        if file_path:
            self.add_to_recent_projects(file_path)
            self.update_recent_menu()
            QMessageBox.information(
                self, "Projet chargé", f"Projet chargé : {file_path}"
            )

    def add_to_recent_projects(self, file_path):
        """Ajoute un chemin à la liste des récents."""
        if file_path in self.recent_projects:
            self.recent_projects.remove(file_path)
        self.recent_projects.insert(0, file_path)
        self.recent_projects = self.recent_projects[
            : self.max_recent_projects
        ]  # Limiter le nombre d'éléments
        self.save_recent_projects()

    def update_recent_menu(self):
        """Met à jour le menu des récents avec les projets actuels."""
        self.recent_menu.clear()
        for project in self.recent_projects:
            action = QAction(project, self)
            action.triggered.connect(
                lambda checked, p=project: self.open_recent_project(p)
            )
            self.recent_menu.addAction(action)

    def open_recent_project(self, project_path):
        """Ouvre un projet à partir de la liste des récents."""
        QMessageBox.information(
            self, "Ouvrir projet récent", f"Projet chargé : {project_path}"
        )
        # Vous pouvez ajouter ici la logique pour charger les données du projet

    def load_recent_projects(self):
        """Charge les projets récents depuis un fichier JSON."""
        try:
            with open(self.recent_file_path, "r") as f:
                self.recent_projects = json.load(f)
        except FileNotFoundError:
            self.recent_projects = []

    def save_recent_projects(self):
        """Sauvegarde les projets récents dans un fichier JSON."""
        with open(self.recent_file_path, "w") as f:
            json.dump(self.recent_projects, f)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
