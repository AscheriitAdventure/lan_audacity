import sys
from typing import List, Dict, Any, Optional, Union, ClassVar
import logging

from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *

from dev.project.src.classes.cl_stacked_objects import SDFSP


class DemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SDFSP Demo")
        self.resize(300, 600)
        
        # Création du widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout horizontal pour avoir le panneau sur le côté
        layout = QHBoxLayout(central_widget)
        
        # Création de notre SDFSP
        self.side_panel = SDFSP(debug=True)
        
        # Configuration des champs de démonstration
        demo_fields = [
            {
                'field_name': "Explorateur de fichiers",
                'field_type': "tree-file",
                'field_description': "Navigation dans les fichiers du projet",
                'tooltip': "Explorez vos fichiers ici",
                'actions': [self.on_file_clicked],
                'collapsed': False
            },
            {
                'field_name': "Liste des tâches",
                'field_type': "list-btn",
                'field_description': "Gestionnaire de tâches",
                'tooltip': "Gérez vos tâches ici",
                'actions': [self.on_task_added],
                'collapsed': True
            },
            {
                'field_name': "Propriétés",
                'field_type': "tree",
                'field_description': "Propriétés de l'élément sélectionné",
                'tooltip': "Voir les propriétés",
                'collapsed': False
            }
        ]
        
        # Chargement des fields
        self.side_panel.load_fields(demo_fields)
        
        # Connexion du signal d'échange de contexte
        self.side_panel.exchangeContext.connect(self.on_context_changed)
        
        # Ajout du panneau au layout
        layout.addWidget(self.side_panel)
        
        # Ajout d'une zone de texte pour les logs
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text, stretch=2)
        
        # Remplissage avec des données de démo
        self.populate_demo_data()

    def populate_demo_data(self):
        """Remplit les widgets avec des données de démonstration"""
        # Remplissage de l'explorateur de fichiers
        file_tree = self.find_widget_by_type(self.side_panel, "tree-file")
        if file_tree:
            project = QTreeWidgetItem(file_tree, ["Mon Projet"])
            src = QTreeWidgetItem(project, ["src"])
            QTreeWidgetItem(src, ["main.py"])
            QTreeWidgetItem(src, ["utils.py"])
            docs = QTreeWidgetItem(project, ["docs"])
            QTreeWidgetItem(docs, ["readme.md"])
            file_tree.expandAll()

        # Remplissage de la liste des tâches
        task_list = self.find_widget_by_type(self.side_panel, "list")
        if task_list:
            task_list.addItems([
                "Implémenter la nouvelle fonctionnalité",
                "Corriger le bug #123",
                "Mettre à jour la documentation"
            ])

        # Remplissage de l'arbre des propriétés
        prop_tree = self.find_widget_by_type(self.side_panel, "tree")
        if prop_tree:
            prop_tree.setHeaderLabels(["Propriété", "Valeur"])
            QTreeWidgetItem(prop_tree, ["Nom", "main.py"])
            QTreeWidgetItem(prop_tree, ["Taille", "1.2 KB"])
            QTreeWidgetItem(prop_tree, ["Date", "2024-02-05"])

    def find_widget_by_type(self, parent: QWidget, widget_type: str) -> Optional[QWidget]:
        """Trouve le premier widget du type spécifié dans les fields"""
        for field_name, widgets in self.side_panel.field_widgets.items():
            content = widgets['content_widget']
            for child in content.findChildren(QWidget):
                if (widget_type == "tree-file" and isinstance(child, QTreeWidget)) or \
                   (widget_type == "list" and isinstance(child, QListWidget)) or \
                   (widget_type == "tree" and isinstance(child, QTreeWidget)):
                    return child
        return None

    def on_file_clicked(self, item: QTreeWidgetItem, column: int):
        """Gestionnaire de clic sur un fichier"""
        self.log_text.append(f"Fichier sélectionné: {item.text(column)}")

    def on_task_added(self):
        """Gestionnaire d'ajout de tâche"""
        self.log_text.append("Nouvelle tâche ajoutée")

    def on_context_changed(self, context: dict):
        """Gestionnaire de changement de contexte"""
        self.log_text.append(f"Contexte changé: {context}")


if __name__ == '__main__':
    # Configuration du logging
    logging.basicConfig(level=logging.DEBUG)
    
    app = QApplication(sys.argv)
    
    # Application d'un style moderne
    # app.setStyle("Fusion")
    
    # Création et affichage de la fenêtre
    window = DemoWindow()
    window.show()
    
    sys.exit(app.exec())