from qtpy.QtWidgets import QPlainTextEdit, QWidget, QTextEdit
from qtpy.QtGui import QColor, QTextFormat, QPainter, QFont
from qtpy.QtCore import Qt, QRect, QSize, Signal, QObject
import unicodedata
from typing import Optional, Tuple, ClassVar,List
from enum import Enum


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)


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
        NoAction = 0    # Aucune action
        LineNumber = 1  # Numéro de ligne
        Breakpoint = 2  # Point d'arrêt
        Bookmark = 3    # Marque-page
        Folding = 4     # Pliage
        Litting = 5     # Coloration

    cursorLocationChanged: ClassVar[Signal] = Signal(int, int)  # row, column

    def __init__(self, text: str, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self._debug: bool = False
        self._locked: bool = False
        self._areaActions: List[CodeEditorv2.ActionArea] = [self.ActionArea.LineNumber]

        self._text: str = text
        self._formatText: str = "Unknown"
        
        # Configuration de la police
        font = QFont("Consolas", 11)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.setFont(font)

        # Configuration de l'éditeur
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(' ') * 4)
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setReadOnly(self._locked)
    
    def loadEnvironment(self):
        self.update_line_number_area_width(0)
        self.highlight_current_line()
    
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
    
    