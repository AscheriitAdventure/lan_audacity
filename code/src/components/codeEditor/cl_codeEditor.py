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
from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *
import logging
import os
import sys
from typing import Optional
from src.components.codeEditor.cl_line_int_area import LineIntArea


class CodeEditorView(QTextEdit):
    def __init__(
            self, 
            locked: Optional[bool] = False,
            parent: Optional[QWidget] = None):
        super().__init__(parent)

        # Line Number
        self.lineIntArea = LineIntArea(editor=self)
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
