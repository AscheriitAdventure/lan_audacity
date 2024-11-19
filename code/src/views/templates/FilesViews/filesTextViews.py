"""
    Informations:
        Objectif de cette classe est de permettre de visualiser le contenu d'un fichier texte.
        Avec comme possibilités:
            - Lire le contenu du fichier (Impératif)
            - Fermer la fenêtre (Impératif)
            - Afficher le chemin Absolu du fichier en premier (Optionnel) # Absolute Path
            - Modifier le contenu du fichier (Optionnel) # Edit
            - Copier le contenu du fichier (Optionnel) # Copy
            - Copier tout le contenu du fichier (Optionnel) # Copy All
            - Coller le contenu du fichier (Optionnel) # Paste
            - Enregistrer les modifications (Optionnel) # Save
            - Vérifier si la typographie est correcte (Optionnel) # Check
        Avec comme outils intégrés: # Dans la 'infobar' 
            - 'Lignes [int], Colonnes [int]' or 'Ln [int], Col [int]'
            - [Encoding]
            - [Language Mode] 
    Outils:
        - nom complet: Files Text Template Views
        - nom de la classe: Files2TV
        - QtPy(PyQt6)
        - logging
        - sys, os, etc...
    Etape 1:
        - Ouvrir et Afficher le contenu du fichier
        - Afficher le numéro de ligne 
"""
from qtpy.QtWidgets import *
import os
from typing import Any, Dict, List, Tuple, Optional

VAR_DOC_FORMAT_LIST: List[str] = [
    "txt", "md", "py", "c", "cpp", "conf", "yml", "yaml", "json", "xml", "html", "css", "js", "ts", "sql", "sh", "log", "csv", "ini", "svg"
]

class Files2TV(QWidget):
    def __init__(
            self,
            file_path: str,
            parent: Optional[QWidget] = None
    ):
        super(Files2TV, self).__init__(parent)

        self.file_path = file_path
        self.layout = QVBoxLayout(self)

        # Barre d'informations (en-tête) -> Chemin Absolu
        self.absolute_path = QWidget()
        # Zone d'affichage du fichier
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        self.text_area = QTextEdit(self.scroll_area)
        self.text_area.setReadOnly(True)
        self.text_area.setLineWrapMode(QTextEdit.NoWrap)
        self.scroll_area.setWidget(self.text_area)

    
    def truePath(self) -> bool:
        return os.path.exists(self.file_path)
    

