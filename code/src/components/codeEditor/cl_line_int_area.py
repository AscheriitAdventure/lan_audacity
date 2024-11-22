from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *
from typing import *
import logging


class LineIntArea(QWidget):
    def __init__(
            self, 
            editor, # CodeEditorView
            parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.editor = editor
    
    def sizeHint(self) -> QSize:
        return QSize(self.editor.lineIntAreaWidth(), 0)
    
    def paintEvent(self, event):
        self.editor.rowAreaPaintEvent(event)


class MarginObjectTextEdit(QWidget):
    def __init__(
            self, 
            editor: QPlainTextEdit, # CodeEditorView
            parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.editor = editor
        self.labels: List[QLabel] = []  # Liste pour stocker les QLabel des numéros de ligne

        # Utilisation d'un QVBoxLayout pour organiser les QLabel verticalement
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 4, 0, 4)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignJustify)
    
    def updateLineNumbers(self):
        """Met à jour les numéros de ligne en fonction des blocs visibles."""
        # Effacer les anciens QLabel
        for label in self.labels:
            label.deleteLater()
        self.labels.clear()

        # Obtenir le premier bloc visible
        block = self.editor.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()
        bottom = top + self.editor.blockBoundingRect(block).height()

        # Parcourir les blocs visibles
        while block.isValid() and top <= self.height():
            if block.isVisible() and bottom >= 0:
                # Créer un QLabel pour chaque numéro de ligne
                number = str(block_number + 1)
                label = QLabel(number, self)
                # Définir la hauteur fixe du QLabel correspondant à la hauteur du bloc
                label.setFixedHeight(18)
                label.setAlignment(Qt.AlignRight)  # Alignement à droite
                self.labels.append(label)

                # Ajouter chaque label à la mise en page verticale
                self.layout.addWidget(label)  # L'ajout automatique à la mise en page

            # Passer au bloc suivant
            block = block.next()
            top = bottom
            bottom = top + self.editor.blockBoundingRect(block).height()
            block_number += 1
        
        # self.repaint()  # Forcer un redessin
    
    def paintEvent(self, event):
        """Dessiner le fond de la marge."""
        painter = QPainter(self)
        painter.fillRect(event.rect(), QColor("Gainsboro"))  # Couleur pour le fond
        self.updateLineNumbers()  # Met à jour les numéros de ligne
