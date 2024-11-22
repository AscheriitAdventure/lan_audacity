""" 
    Commentaires:
        Bon l'objectif de ce code est de créer un environnement d'écriture de fichiers de configurations.
        Pour une meilleur gestion du code et de l'interface, il est préférable de séparer les composants.
        Ici nous allons nous concentrer sur l'amélioration de QTextEdit.
    Outils:
        - nom complet: Code Editor View
        - nom court: CEV
        - nom de la classe: CodeEditorView
        - QtPy(PyQt6)
        - logging
        - os
        - sys
        - typing
    Etapes:
        1. Création de la classe CodeEditorView
            - [_]  
        2. Implémentation de la classe CodeEditorView
        3. Création d'un fichier de test

"""
from qtpy.QtWidgets import * # PyQt6
from qtpy.QtGui import * # PyQt6
from qtpy.QtCore import * # PyQt6
import logging
from typing import Optional
from src.components.codeEditor.cl_line_int_area import LineIntArea, MarginObjectTextEdit


class CodeEditorView(QTextEdit):
    def __init__(
            self, 
            locked: Optional[bool] = False,
            parent: Optional[QWidget] = None):
        super().__init__(parent)

        # Line Number
        self.lineIntArea = LineIntArea(editor=self, parent=self)
        self.blockCountChanged()
        self.textChanged.connect(self.blockCountChanged)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineIntAreaWidth()
        self.highlightCurrentLine()

        # Font de la police, Taille de la police
        font = QFont("Consolas", 11)
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)
        # Tabulation
        self.setTabStopWidth(40)
        # Mise en forme du texte
        self.setLineWrapMode(QTextEdit.NoWrap)

        # Verrouillage
        self.setReadOnly(locked)
        logging.debug(f"CodeEditorView: locked={locked}")
        logging.debug(f"LineIntArea Width: {self.lineIntAreaWidth()}")
   
    def lineIntAreaWidth(self) -> int:
        digits = len(str(max(1, self.document().blockCount())))
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space
    
    def updateLineIntAreaWidth(self):
        self.setViewportMargins(self.lineIntAreaWidth(), 0, 0, 0)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab:  # Gestion de la touche Tab
            cursor = self.textCursor()
            cursor.insertText(" " * 4)  # Insère 4 espaces
        else:
            super().keyPressEvent(event)  # Comportement par défaut pour les autres touches
    
    def updateLineIntArea(self, rect, dy):
        if dy:
            self.lineIntArea.scroll(0, dy)
        else:
            self.lineIntArea.update(0, rect.y(), self.lineIntArea.width(), rect.height())
        
        if rect.contains(self.viewport().rect()):
            self.updateLineIntAreaWidth()

    def blockCountChanged(self):
        # self.updateLineIntAreaWidth()
        # self.updateLineIntArea(self.rect(), 0)
        if self.lineIntArea is not None:
            self.updateLineIntAreaWidth()
            self.lineIntArea.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineIntArea.setGeometry(QRect(cr.left(), cr.top(), self.lineIntAreaWidth(), cr.height()))
        self.updateLineIntAreaWidth()
    
    def rowAreaPaintEvent(self, event):
        logging.info("CodeEditorView: rowAreaPaintEvent")
        painter = QPainter(self.lineIntArea)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.document().firstBlock()
        blockNumber = 0
        top = self.viewport().geometry().top()
        bottom = top + self.fontMetrics().height()
        height = self.fontMetrics().height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = blockNumber + 1
                painter.setPen(Qt.black)
                painter.drawText(
                    0, int(top), self.lineIntArea.width(), int(height),
                    Qt.AlignRight, str(number)
                )

            block = block.next()
            top = bottom
            bottom = top + height
            blockNumber += 1

    def highlightCurrentLine(self):
        extraSelections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor("#F5F5F5")
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)

        self.setExtraSelections(extraSelections)   


"""
    Commentaire:
        Il faut peut être pas tout recommencer mais presque quand même.
        Les bonnes nouvelles:
            - nous avons une idée plus claire de ce que nous voulons
            - la police d'écriture est bonne ainsi que la taille
            - le surlignage du bloc de texte est bon
            - la gestion des tabulations est bonne
            - le verrouillage est bon
    Outils:
        - nom complet: Code Editor View Update 1
        - nom court: CEV
        - nom de la classe: CEVU1
        - QtPy(PyQt6)
        - logging
        - os
        - sys
        - typing
    Etape 1:
        - [OK] Création de la classe CEVU1
        - [OK] Ajout de la police d'écriture et de la taille
        - [OK] Ajout de la tabulation
        - [OK] Ajout de la mise en forme du texte
        - [OK] Ajout du verrouillage
        - [OK] Ajout de la gestion de la touche Tab
    Etape 2:
        - [OK] Ajout de la classe CEVU1 dans le fichier de test
        - [OK] Test de la classe CEVU1
        - [En cours] Correction des erreurs
    Etape 3:
        - [OK] Ajout de la gestion des numéros de lignes
        - [OK] Ajout de la gestion du surlignage de la ligne courante
    Etape 4:
        - [OK] Implémenter la classe au main en dev.
        - [_] Faire les corrections nécessaires (Impératif)
            - [_] Correction de la gestion de la marge

"""

class CEVU1(QPlainTextEdit):
    def __init__(
            self, 
            locked: Optional[bool] = False,
            parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        # Font de la police, Taille de la police
        font = QFont("Consolas", 11)
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)
        # Tabulation
        self.setTabStopWidth(40)

        # Verrouillage
        self.setReadOnly(locked)
        logging.debug(f"CodeEditorView: locked={locked}")

        # Vue de la marge à gauche
        self.marginArea = MarginObjectTextEdit(editor=self, parent=self)
        self.setViewportMargins(40, 0, 0, 0)
        
        # Connecter les signaux nécessaires
        self.blockCountChanged.connect(self.marginArea.update)
        self.updateRequest.connect(self.marginArea.update)
        self.cursorPositionChanged.connect(self.update)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab:
            cursor = self.textCursor()
            cursor.insertText(" " * 4)
        else:
            super().keyPressEvent(event)
    
    def highlightCurrentLine(self):
        extraSelections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor("#F5F5F5")
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)

        self.setExtraSelections(extraSelections)

    def resizeEvent(self, event):
        """Synchroniser la position et la taille du widget marge."""
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.marginArea.setGeometry(QRect(cr.left(), cr.top(), 40, cr.height()))
