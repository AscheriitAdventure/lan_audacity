from qtpy.QtWidgets import QApplication, QTextEdit, QWidget
from qtpy.QtGui import QPainter, QColor, QTextFormat, QFont
from qtpy.QtCore import QRect, Qt, QSize


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)


class CodeEditor(QTextEdit):
    def __init__(self):
        super().__init__()
        self.lineNumberArea = LineNumberArea(self)
        self.blockCountChanged()
        self.textChanged.connect(self.blockCountChanged)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth()
        self.highlightCurrentLine()

        # Définir une police monospace pour l'éditeur
        font = QFont("Consolas", 11)  # Police Consolas à taille 11
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)
        self.setTabStopDistance(40)  # Ajuste la largeur de la tabulation

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab:  # Gestion de la touche Tab
            cursor = self.textCursor()
            cursor.insertText(" " * 4)  # Insère 4 espaces
        else:
            super().keyPressEvent(event)  # Comportement par défaut pour les autres touches

    def lineNumberAreaWidth(self):
        digits = len(str(max(1, self.document().blockCount())))
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def updateLineNumberAreaWidth(self):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def blockCountChanged(self):
        self.updateLineNumberAreaWidth()
        self.updateLineNumberArea(self.rect(), 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.document().firstBlock()
        blockNumber = 0
        top = self.viewport().geometry().top()
        bottom = top + self.fontMetrics().height()
        height = self.fontMetrics().height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, int(top), self.lineNumberArea.width(), int(height), Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + height
            blockNumber += 1

    def highlightCurrentLine(self):
        extraSelections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(Qt.yellow).lighter(160)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)

        self.setExtraSelections(extraSelections)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    editor = CodeEditor()
    editor.setText("Ligne 1\nLigne 2\nLigne 3\nLigne 4")
    editor.resize(400, 300)
    editor.show()
    sys.exit(app.exec_())
