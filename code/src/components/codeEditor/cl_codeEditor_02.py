from qtpy.QtWidgets import QPlainTextEdit, QWidget, QTextEdit
from qtpy.QtGui import QColor, QTextFormat, QPainter, QFont
from qtpy.QtCore import Qt, QRect, QSize, Signal, QObject
import unicodedata
from typing import Optional, Tuple, ClassVar,List
from enum import Enum


class LineNumberArea(QWidget):
    def __init__(self, editor: 'CodeEditorv2'):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        # return QSize(self.editor.line_number_area_width(), 0)
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        # self.editor.line_number_area_paint_event(event)
        self.editor.lineNumberAreaPaintEvent(event)

class CodeEditor(QPlainTextEdit):
    # Nouveaux signaux
    cursorLocationChanged = Signal(int, int)  # row, column
    characterFormatChanged = Signal(str)      # format du caractère

    def __init__(self, locked: bool = False, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        # Configuration de base
        self.line_number_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.cursorPositionChanged.connect(self.emit_cursor_location)
        self.cursorPositionChanged.connect(self.emit_character_format)
        
        # Configuration de la police
        font = QFont("Consolas", 11)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.setFont(font)
        
        # Configuration de l'éditeur
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(' ') * 4)
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setReadOnly(locked)
        
        # Initialisation
        self.update_line_number_area_width(0)
        self.highlight_current_line()

    def get_cursor_position(self) -> Tuple[int, int]:
        """Retourne la position actuelle du curseur (ligne, colonne)"""
        cursor = self.textCursor()
        return (cursor.blockNumber() + 1, cursor.positionInBlock() + 1)

    def get_character_at_cursor(self) -> str:
        """Retourne le caractère à la position du curseur"""
        cursor = self.textCursor()
        block_text = cursor.block().text()
        pos_in_block = cursor.positionInBlock()
        
        if pos_in_block < len(block_text):
            return block_text[pos_in_block]
        return ""

    def get_character_format(self, char: str) -> str:
        """Détermine le format du caractère"""
        if not char:
            return "Unknown"
        
        # Obtenir la catégorie Unicode du caractère
        category = unicodedata.category(char)
        
        # Déterminer le format en fonction de la catégorie
        if ord(char) < 128:
            return "ASCII"
        elif category.startswith('L'):  # Lettres
            if '\u0370' <= char <= '\u03FF':
                return "Greek"
            elif '\u0400' <= char <= '\u04FF':
                return "Cyrillic"
            elif '\u0000' <= char <= '\u007F':
                return "Latin"
            else:
                name = unicodedata.name(char, "Unknown")
                script = name.split()[0]
                return script
        return f"Unicode ({category})"

    def emit_cursor_location(self):
        """Émet le signal de changement de position du curseur"""
        row, col = self.get_cursor_position()
        self.cursorLocationChanged.emit(row, col)

    def emit_character_format(self):
        """Émet le signal de format du caractère sous le curseur"""
        char = self.get_character_at_cursor()
        char_format = self.get_character_format(char)
        self.characterFormatChanged.emit(char_format)

    def line_number_area_width(self):
        digits = max(1, len(str(self.blockCount())))
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(
            QRect(cr.left(), cr.top(),
                  self.line_number_area_width(), cr.height())
        )

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor("#F0F0F0"))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        offset = self.contentOffset()
        top = self.blockBoundingGeometry(block).translated(offset).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.GlobalColor.black)
                painter.drawText(
                    0, int(top), self.line_number_area.width(),
                    self.fontMetrics().height(),
                    Qt.AlignmentFlag.AlignRight, number
                )

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def highlight_current_line(self):
        extra_selections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor("#F8F8F8")
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Tab:
            cursor = self.textCursor()
            cursor.insertText("    ")  # 4 espaces
        else:
            super().keyPressEvent(event)

class CodeEditorv2(QPlainTextEdit):
    class ActionArea(Enum):
        """
        Définit les différentes zones d'action disponibles dans l'éditeur.
        
        Les zones d'action sont des fonctionnalités qui peuvent être activées
        individuellement pour personnaliser l'éditeur.
        """
        NoAction = 0    # Aucune action
        LineNumber = 1  # Numéro de ligne
        Breakpoint = 2  # Point d'arrêt
        Bookmark = 3    # Marque-page
        Folding = 4     # Pliage
        Linting = 5     # Coloration

    cursorLocationChanged: ClassVar[Signal] = Signal(int, int)  # row, column

    def __init__(self, text: Optional[str] = None, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self._debug: bool = False   # Mode débogage
        self._locked: bool = False  # Mode verrouillé
        self._areaActions: List[CodeEditorv2.ActionArea] = []
    
        # Initialiser le texte
        self.setText(text or "")

        self._formatText: str = "Unknown"
        
        # Initialiser la configuration
        self._setupFont()
        self._setupEditor()
        self.loadEnvironment()
    
    def _setupFont(self):
        """Configure la police de l'éditeur"""
        font = QFont("Consolas", 11)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.setFont(font)
    
    def _setupEditor(self):
        """Configure les paramètres de base de l'éditeur"""
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(' ') * 4)
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setReadOnly(self._locked)
    
    def loadEnvironment(self):
        """
        Configure l'environnement de l'éditeur en fonction des zones d'action activées.
        
        Cette méthode initialise toutes les fonctionnalités demandées via les
        ActionArea. Elle est appelée automatiquement lors de l'initialisation
        et après l'ajout de nouvelles zones d'action.
        """
        self.setReadOnly(self._locked)
        self.cursorPositionChanged.connect(self.emitCursorLocation)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        for action in self._areaActions:
            if action == CodeEditorv2.ActionArea.NoAction:
                pass
            elif action == CodeEditorv2.ActionArea.LineNumber:
                self.lineNumberArea = LineNumberArea(self)
                self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
                self.updateRequest.connect(self.updateLineNumberArea)                
            elif action == CodeEditorv2.ActionArea.Breakpoint:
                pass
            elif action == CodeEditorv2.ActionArea.Bookmark:
                pass
            elif action == CodeEditorv2.ActionArea.Folding:
                pass
            elif action == CodeEditorv2.ActionArea.Linting:
                pass
            else:
                pass
    
    def setDebug(self, debug: bool):
        self._debug = debug
    
    def setLockedView(self, locked: bool):
        self._locked = locked
        self.setReadOnly(locked)
    
    def setText(self, text: str):
        self._text = text
        self.setPlainText(text)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Tab:
            cursor = self.textCursor()
            cursor.insertText("    ")  # 4 espaces
        else:
            super().keyPressEvent(event)
    
    def getCursorPosition(self) -> Tuple[int, int]:
        """Retourne la position actuelle du curseur (ligne, colonne)"""
        cursor = self.textCursor()
        return (cursor.blockNumber() + 1, cursor.positionInBlock() + 1)
    
    def getCharacterAtCursor(self) -> str:
        """Retourne le caractère à la position du curseur"""
        cursor = self.textCursor()
        block_text = cursor.block().text()
        pos_in_block = cursor.positionInBlock()
        
        if pos_in_block < len(block_text):
            return block_text[pos_in_block]
        return ""
    
    def emitCursorLocation(self):
        """Émet le signal de changement de position du curseur"""
        row, col = self.getCursorPosition()
        self.cursorLocationChanged.emit(row, col)
    
    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor("#F0F0F0"))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        offset = self.contentOffset()
        top = self.blockBoundingGeometry(block).translated(offset).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.GlobalColor.black)
                painter.drawText(
                    0, int(top), self.lineNumberArea.width(),
                    self.fontMetrics().height(),
                    Qt.AlignmentFlag.AlignRight, number
                )

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def highlightCurrentLine(self):
        extra_selections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor("#F8F8F8")
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    def lineNumberAreaWidth(self):
        digits = max(1, len(str(self.blockCount())))
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _=None):
        """
        Met à jour la largeur de la zone des numéros de ligne.

        Args:
            _ : Paramètre ignoré, présent pour compatibilité avec le signal blockCountChanged
        """
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)
    
    def resizeEvent(self, event):
        """
        Gère le redimensionnement de l'éditeur et de ses zones associées.
        
        Cette méthode est appelée automatiquement lors du redimensionnement de la fenêtre.
        Elle s'assure que toutes les zones (numéros de ligne, etc.) sont correctement
        redimensionnées.
        
        Args:
            event: L'événement de redimensionnement Qt
        """
        super().resizeEvent(event)
        
        if hasattr(self, 'lineNumberArea'):
            cr = self.contentsRect()
            self.lineNumberArea.setGeometry(
                QRect(cr.left(), cr.top(),
                    self.lineNumberAreaWidth(), cr.height())
            )
    
    def addAreaActions(self, obj: 'CodeEditorv2.ActionArea'):
        """
        Ajoute une nouvelle zone d'action à l'éditeur.
        
        Args:
            obj (ActionArea): La zone d'action à ajouter
            
        Note:
            L'ajout d'une zone d'action nécessite un rechargement de l'environnement
            pour être pris en compte.
        """
        if obj not in self._areaActions:
            self._areaActions.append(obj)
            self.loadEnvironment()  # Recharge l'environnement pour appliquer les changements

    

