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
from qtpy.QtCore import Qt
from qtpy.QtGui import QFontMetrics
import os
import logging
from typing import List, Optional
from src.components.componentsExport import *
from pathlib import Path

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

        self.file_path = ""
        self.setFilePath(file_path)
        self.layout = QVBoxLayout(self)

        # Barre d'informations (en-tête) -> Chemin Absolu
        self.absolute_path = QBreadcrumbs(
            list_objects=self.breadcrumbsList(),
            parent=self
        )
        self.layout.addWidget(self.absolute_path)

        # Zone d'affichage du fichier
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        self.text_area = QTextEdit(self.scroll_area)
        # self.text_area.setReadOnly(True)
        # self.text_area.setLineWrapMode(QTextEdit.NoWrap)
        self.scroll_area.setWidget(self.text_area)

    def setFilePath(self, file_path: str):
        if os.path.exists(file_path):
            self.file_path = os.path.normpath(file_path)
        else:
            self.file_path = ""
            logging.error("Le fichier n'existe pas")
    
    def breadcrumbsList(self) -> List[QPushButton]:
        listBtn = []
        # Divise le chemin en une liste
        list_obj_path = self.file_path.split(os.sep)
        
        # Crée un bouton pour chaque élément de la liste
        for i in range(len(list_obj_path)):
            btn = QPushButton(list_obj_path[i])
            btn.setFlat(True)
            # Ajoute un tooltip indiquant le chemin absolu
            absPath = os.path.abspath(os.sep.join(list_obj_path[:i+1]))
            btn.setToolTip(absPath)
            # Ajoute à la liste des boutons
            listBtn.append(btn)
        
        return listBtn
    

""" 
    Commentaires:
        Il va falloir redéfinir l'étape 1 pour ne pas sauter des étapes.
    Outils:
        - nom complet: Files Text Template Views Update 1
        - nom de la classe: Files2TVU1
        - QtPy(PyQt6)
        - logging
        - sys, os, etc...
    Etape 1:
        - Bien compartimenter les widgets
"""


class Files2TVU1(QWidget):
    def __init__(
            self,
            file_path: str,
            parent: Optional[QWidget] = None
    ):
        super(Files2TVU1, self).__init__(parent)

        self.file_path = ""
        self.setFilePath(file_path)
        self.layout = QVBoxLayout(self)

        self.setAbsolutePathWidget()

        self.textArea = QTableWidget(self)
        self.textArea.setColumnCount(1)
        self.textArea.horizontalHeader().hide()
        self.textArea.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.textArea.setShowGrid(False)
        self.layout.addWidget(self.textArea)

        self.setTextFile()
    
    def setFilePath(self, file_path: str):
        if os.path.exists(file_path):
            self.file_path = Path(os.path.normpath(file_path))
        else:
            self.file_path = ""
            logging.error("Le fichier n'existe pas")
    
    def setAbsolutePathWidget(self):
        # Barre d'informations (en-tête) -> Chemin Absolu
        absolute_path = QBreadcrumbs(
            list_objects=self.breadcrumbsList(),
            parent=self
        )
        self.layout.addWidget(absolute_path, 0, Qt.AlignTop | Qt.AlignLeft)
    
    def breadcrumbsList(self) -> List[QPushButton]:
        listBtn = []
        # Divise le chemin en une liste
        list_obj_path = self.file_path.parts
        
        # Crée un bouton pour chaque élément de la liste
        for i in range(len(list_obj_path)):
            btn = QPushButton(list_obj_path[i])
            fontMetrics = QFontMetrics(btn.font())
            btn.setFlat(True)
            btn.setMaximumWidth(fontMetrics.horizontalAdvance(btn.text())+10)
            # Ajoute un tooltip indiquant le chemin absolu
            absPath = os.path.abspath(os.sep.join(list_obj_path[:i+1]))
            btn.setToolTip(absPath)
            # Ajoute à la liste des boutons
            listBtn.append(btn)
        
        return listBtn
    
    def setTextFile(self):
        self.textArea.clear()

        with self.file_path.open() as file:
            lines = file.readlines()
            self.textArea.setRowCount(len(lines))
            for i, line in enumerate(lines):
                cleanLine = line.rstrip("\n")
                item = QTableWidgetItem(cleanLine)
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable)
                self.textArea.setItem(i, 0, item)

        
    # def  
